from datetime import date, timedelta
import os
import datetime
from uuid import UUID

from typing import List, BinaryIO, Dict
import pandas as pd

from werkzeug.exceptions import Conflict, NotFound, Unauthorized, UnsupportedMediaType
from flask import g, current_app
from app.extensions import db

from .model import SellerFirm
from .interface import SellerFirmInterface
from .schema import seller_firm_dto

from ...utils.service import InputService, NotificationService


class SellerFirmService:
    @staticmethod
    def get_all() -> List[SellerFirm]:
        seller_firms = SellerFirm.query.all()
        return seller_firms

    @staticmethod
    def get_by_accounting_firm_id(accounting_firm_id) -> List[SellerFirm]:
        seller_firms = SellerFirm.query.filter_by(accounting_firm_id=accounting_firm_id).all()
        return seller_firms


    @staticmethod
    def get_by_public_id(public_id: UUID) -> SellerFirm:
        return SellerFirm.query.filter_by(public_id = public_id).first()

    @staticmethod
    def get_by_id(seller_firm_id: int) -> SellerFirm:
        return SellerFirm.query.filter_by(id=seller_firm_id).first()


    @staticmethod
    def update(seller_firm_id: int, data_changes: SellerFirmInterface) -> SellerFirm:
        seller_firm = SellerFirmService.get_by_id(seller_firm_id)
        seller_firm.update(data_changes)
        db.session.commit()
        return seller_firm

    @staticmethod
    def delete_by_id(seller_firm_id: int) -> Dict:
        #check if accounting business exists in db
        seller_firm = SellerFirm.query.filter_by(id = seller_firm_id).first()
        if seller_firm:
            db.session.delete(seller_firm)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Seller firm (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This accounting firm does not exist.')


    @staticmethod
    def create(seller_firm_data: SellerFirmInterface) -> SellerFirm:

        new_seller_firm = SellerFirm(
            claimed = seller_firm_data.get('claimed'),
            created_by = seller_firm_data.get('created_by'),
            name = seller_firm_data.get('name'),
            address = seller_firm_data.get('address'),
            establishment_country_code = seller_firm_data.get('establishment_country_code'),
            accounting_firm_id = seller_firm_data.get('accounting_firm_id'),
            accounting_firm_client_id = seller_firm_data.get('accounting_firm_client_id')
        )

        #add seller firm to db
        db.session.add(new_seller_firm)
        db.session.commit()

        return new_seller_firm


    @staticmethod
    def get_seller_firm_id(**kwargs) -> int:
        """
        Function may take either:
            - a pd.Dataframe kwargs['df'] and an integer kwargs['i'] as the row index
        or  - a UUID kwargs['seller_firm_public_id']
        If both, the later one is prioritized.
        """
        if isinstance(kwargs.get('seller_firm_public_id'), UUID):
            seller_firm_public_id = kwargs['seller_firm_public_id']

        elif ('df' and 'i') in kwargs and isinstance(kwargs['df'], pd.DataFrame) and isinstance(kwargs['i'], int):
            seller_firm_public_id = InputService.get_str_or_None(df, i, column='seller_firm_public_id')

        else:
            raise

        seller_firm = SellerFirm.query.filter_by(public_id=seller_firm_public_id).first()

        if seller_firm:
            seller_firm_id = seller_firm.id
            return seller_firm_id


    @staticmethod
    #kwargs can contain: seller_firm_public_id
    def process_seller_firm_information_files_upload(seller_firm_information_files: List[BinaryIO], claimed: bool, **kwargs: Dict[str, UUID]) -> Dict:
        BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config['BASE_PATH_STATIC_DATA_SELLER_FIRM']

        file_type = 'seller_firm'
        df_encoding = 'utf-8'
        delimiter = None
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM
        user_id = g.user.id
        accounting_firm_id = g.user.employer_id


        for file in seller_firm_information_files:
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            SellerFirmService.process_seller_firm_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, claimed=claimed, accounting_firm_id=accounting_firm_id, **kwargs)

        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(seller_firm_information_files)))
        }

        return response_object


    # celery task !!
    @staticmethod
    def process_seller_firm_information_file(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, **kwargs) -> List[Dict]:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_objects = SellerFirmService.create_seller_firms(df, file_path_in, user_id, **kwargs)

        InputService.move_file_to_out(file_path_in, file_type)


        return response_objects




    @staticmethod
    def create_seller_firms(df: pd.DataFrame, file_path_in: str, user_id: int, **kwargs) -> List[Dict]: #upload only for tax auditors
        error_counter = 0
        total_number_items = len(df.index)
        input_type = 'seller firm'  # only used for response objects

        for i in range(total_number_items):

            seller_firm_data = {
                'claimed': kwargs['claimed'],
                'created_by': user_id,
                'name': InputService.get_str_or_None(df, i, column='seller_firm_name'),
                'address': InputService.get_str_or_None(df, i, column='address'),
                'establishment_country_code': InputService.get_str(df, i, column='establishment_country_code'),
                'accounting_firm_id': kwargs['accounting_firm_id'],
                'accounting_firm_client_id': InputService.get_str(df, i, column='accounting_firm_client_id'),
            }

            try:
                SellerFirmService.create(seller_firm_data)

            except:
                db.session.rollback()
                error_counter += 1

            db.session.commit()

        response_objects = InputService.create_input_response_objects(file_path_in, input_type, total_number_items, error_counter)

        return response_objects
