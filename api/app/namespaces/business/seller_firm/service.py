from datetime import date, timedelta
import os
import datetime
import uuid
from typing import List

from werkzeug.exceptions import Conflict, NotFound, Unauthorized, UnsupportedMediaType
from flask import g, current_app
from app.extensions import db

from .model import SellerFirm
from .schema import seller_firm_dto

from ...utils.service import InputService


class SellerFirmService:
    @staticmethod
    def get_all() -> List[SellerFirm]:
        seller_firms = SellerFirm.query.all()
        return seller_firms

    @staticmethod
    def get_by_id(public_id: str) -> SellerFirm:
        seller_firm = SellerFirm.query.filter_by(public_id = public_id).first()
        if seller_firm:
            return seller_firm



    @staticmethod
    def update(public_id: str, data_changes: dict) -> SellerFirm:
        seller_firm = SellerFirmService.get_by_id(public_id)
        seller_firm.update(data_changes)
        db.session.commit()
        return seller_firm

    @staticmethod
    def delete_by_id(public_id: str):
        #check if accounting business exists in db
        seller_firm = SellerFirm.query.filter(SellerFirm.public_id == public_id).first()
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
    def create_seller_firm(seller_firm_data: dict) -> SellerFirm:

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
    def get_seller_firm_id(df, i, **kwargs) -> list:
        if not 'seller_firm_id' in kwargs:
            seller_firm_public_id = InputService.get_str_or_None(df, i, column='seller_firm_id')
        else:
            seller_firm_public_id = kwargs['seller_firm_id']

        seller_firm = SellerFirm.query.filter_by(public_id=seller_firm_public_id).first()

        if seller_firm:
            seller_firm_id = seller_firm.id
            return seller_firm_id_list


    @staticmethod
    #kwargs can contain: seller_firm_id
    def process_seller_firm_information_files_upload(seller_firm_information_files: list, claimed: bool, **kwargs):
        BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config['BASE_PATH_STATIC_DATA_SELLER_FIRM']

        file_type = 'seller_firm'
        df_encoding = None
        delimiter = None
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM
        user_id = g.user.id
        accounting_firm_id = g.user.employer_id


        for file in seller_firm_information_files:
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            SellerFirmService.process_seller_firm_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, claimed=claimed, user_id=user_id, accounting_firm_id=accounting_firm_id, **kwargs)

        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(seller_firm_information_files)))
        }

        return response_object


    # celery task !!
    @staticmethod
    def process_seller_firm_information_file(file_path_in: str, file_type: str, df_encoding, delimiter, basepath: str, **kwargs) -> list:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_objects = SellerFirmService.create_seller_firms(df, file_path_in, **kwargs)

        InputService.move_file_to_out(file_path_in, file_type)


        return response_objects




    @staticmethod
    def create_seller_firms(df, file_path_in: str, **kwargs): #upload only for tax auditors
        error_counter = 0
        total_number_items = len(df.index)
        input_type = 'seller firm'  # only used for response objects

        for i in range(total_number_items):

            seller_firm_data = {
                'claimed': kwargs['claimed'],
                'created_by': kwargs['user_id'],
                'name': InputService.get_str_or_None(df, i, column='seller_firm_name'),
                'address': InputService.get_str_or_None(df, i, column='address'),
                'establishment_country_code': InputService.get_str(df, i, column='establishment_country_code'),
                'accounting_firm_id': kwargs['accounting_firm_id'],
                'accounting_firm_client_id': InputService.get_str(df, i, column='accounting_firm_client_id'),
            }

            try:
                SellerFirmService.create_seller_firm(seller_firm_data)

            except:
                db.session.rollback()
                error_counter += 1

            db.session.commit()

        response_objects = InputService.create_input_response_objects(file_path_in, input_type, total_number_items, error_counter)

        return response_objects
