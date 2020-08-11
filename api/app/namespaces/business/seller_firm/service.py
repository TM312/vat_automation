import os

from typing import List, BinaryIO, Dict
import pandas as pd
from datetime import datetime

from werkzeug.exceptions import Conflict, NotFound, Unauthorized, UnsupportedMediaType
from flask import g, current_app
from app.extensions import db

from .model import SellerFirm
from .interface import SellerFirmInterface

from ...utils.service import InputService, NotificationService
from ...utils import SellerFirmNotification
from ...tag.service import TagService


class SellerFirmService:
    @staticmethod
    def get_all() -> List[SellerFirm]:
        return SellerFirm.query.all()


    @staticmethod
    def get_by_identifiers(seller_firm_name: str,
                           address: str,
                           establishment_country_code: str
        ):
        seller_firm = SellerFirm.query.filter_by(name=seller_firm_name).first()
        if not seller_firm:
            seller_firm = SellerFirm.query.filter(
                SellerFirm.address == address,
                SellerFirm.establishment_country_code == establishment_country_code,
                ).first()

        return seller_firm


    @staticmethod
    def get_by_public_id(public_id: str) -> SellerFirm:
        return SellerFirm.query.filter_by(public_id = public_id).first()

    @staticmethod
    def get_by_id(seller_firm_id: int) -> SellerFirm:
        return SellerFirm.query.filter_by(id=seller_firm_id).first()


    @staticmethod
    def update(seller_firm_id: int, data_changes: SellerFirmInterface) -> SellerFirm:
        seller_firm = SellerFirmService.get_by_id(seller_firm_id)
        if isinstance(seller_firm, SellerFirm):
            seller_firm.update(data_changes)
            db.session.commit()
        return seller_firm

    @staticmethod
    def delete_by_public_id(seller_firm_public_id: str) -> Dict:
        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if seller_firm:
            db.session.delete(seller_firm)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Seller firm (Public ID: {}) has been successfully deleted.'.format(seller_firm_public_id)
            }
            return response_object
        else:
            raise NotFound('This accounting firm does not exist.')

    @staticmethod
    def delete_by_id(seller_firm_id: int) -> Dict:
        #check if accounting business exists in db
        seller_firm = SellerFirmService.get_by_id(seller_firm_id)
        if seller_firm:
            db.session.delete(seller_firm)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Seller firm (Public ID: {}) has been successfully deleted.'.format(seller_firm_id)
            }
            return response_object
        else:
            raise NotFound('This accounting firm does not exist.')


    @staticmethod
    def create_as_client(seller_firm_data_as_client: SellerFirmInterface) -> SellerFirm:

        name = seller_firm_data_as_client.get('name')
        establishment_country_code = seller_firm_data_as_client.get('establishment_country_code')

        if (name != None and establishment_country_code != None):
            seller_firm = SellerFirm.query.filter_by(name=name, establishment_country_code=establishment_country_code).first()

        if seller_firm:

            data_changes = {k:v for k,v in seller_firm_data_as_client.items() if (v is not None or k != 'name')}

            seller_firm.update(data_changes)
            db.session.commit()

            return seller_firm

        else:
            seller_firm_data = {
                'claimed': False,
                'created_by': g.user.id,
                'name': name,
                'address': seller_firm_data_as_client.get('address'),
                'establishment_country_code': establishment_country_code,
            }

            try:
                new_seller_firm = SellerFirmService.create(seller_firm_data)
                new_seller_firm.accounting_firms.append(g.user.employer)
                db.session.commit()
                return new_seller_firm

            except:
                db.session.rollback()
                raise



    @staticmethod
    def create(seller_firm_data: SellerFirmInterface) -> SellerFirm:

        new_seller_firm = SellerFirm(
            claimed = seller_firm_data.get('claimed'),
            created_by = seller_firm_data.get('created_by'),
            name = seller_firm_data.get('name'),
            address = seller_firm_data.get('address'),
            establishment_country_code = seller_firm_data.get('establishment_country_code')
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
        or  - a str kwargs['seller_firm_public_id']
        If both, the later one is prioritized.
        """
        if isinstance(kwargs.get('seller_firm_public_id'), str):
            seller_firm_public_id = kwargs['seller_firm_public_id']

        elif ('df' and 'i') in kwargs and isinstance(kwargs['df'], pd.DataFrame) and isinstance(kwargs['i'], int):
            seller_firm_public_id = InputService.get_str_or_None(df=kwargs['df'], i=kwargs['i'], column='seller_firm_public_id')

        else:
            raise

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)

        if seller_firm:
            seller_firm_id = seller_firm.id
            return seller_firm_id


    @staticmethod
    def process_data_upload(seller_firm_public_id, file: BinaryIO):
        DATA_ALLOWED_EXTENSIONS = current_app.config['DATA_ALLOWED_EXTENSIONS']
        BASE_PATH_DATA_SELLER_FIRM = current_app.config['BASE_PATH_DATA_SELLER_FIRM']
        user_id = g.user.id

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)

        # for file in seller_firm_files:
        file_path_tbd = InputService.store_file(file=file, allowed_extensions=DATA_ALLOWED_EXTENSIONS, basepath=BASE_PATH_DATA_SELLER_FIRM, file_type='tbd')

        df_encoding = 'utf-8'
        delimiter = ';' if InputService.infer_delimiter(file_path_tbd) != '\t' else '\t'
        df = InputService.read_file_path_into_df(file_path_tbd, df_encoding, delimiter)
        file_type = InputService.determine_file_type(df)
        data_type = InputService.determine_data_type(file_type)

        file_path_in = InputService.move_data_to_file_type(file_path_tbd, data_type, file_type)

        #Prepare SellerFirmNotification
        seller_firm_notification_data = {
            'subject': 'Data Upload',
            'status': 'success',
            'seller_firm_id': seller_firm.id,
            'created_by': user_id
        }

        if data_type == 'static':
            basepath = current_app.config['BASE_PATH_STATIC_DATA_SELLER_FIRM']

            if file_type == 'account_list':
                from ...account.service import AccountService
                response_object = AccountService.process_account_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm.id)
                tag = TagService.get_by_code('ACCOUNT')

            elif file_type == 'distance_sale_list':
                from ...distance_sale.service import DistanceSaleService
                response_object = DistanceSaleService.process_distance_sale_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm.id)
                tag = TagService.get_by_code('DISTANCE_SALE')

            elif file_type == 'item_list':
                from ...item.service import ItemService
                response_object = ItemService.process_item_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm.id)
                tag = TagService.get_by_code('ITEM')

            elif file_type == 'vat_numbers':
                from ...tax.vatin.service import VATINService
                response_object = VATINService.process_vat_numbers_file(file_path_in, file_type, df_encoding, delimiter, basepath, seller_firm.id)
                tag = TagService.get_by_code('VAT_NUMBER')

        elif data_type == 'recurring':
            basepath = current_app.config['BASE_PATH_TRANSACTION_DATA_SELLER_FIRM']

            if file_type == 'transactions_amazon':

                from ...transaction_input.service import TransactionInputService
                try:
                    response_object = TransactionInputService.process_transaction_input_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id)
                except:
                    db.session.rollback()
                    raise
                tag = TagService.get_by_code('TRANSACTION')


        else:
            raise

        seller_firm_notification = NotificationService.get_seller_firm_shared(seller_firm.id, g.user.id, datetime.utcnow(), subject='Data Upload')
        if isinstance(seller_firm_notification, SellerFirmNotification):
            if not tag in seller_firm_notification.tags:
                seller_firm_notification.tags.append(tag)
                seller_firm_notification.modify()
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
        else:
            seller_firm_notification = NotificationService.create_seller_firm_notification(seller_firm_notification_data)
            seller_firm_notification.tags.append(tag)
            seller_firm_notification.modify()
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise

        return response_object


    @staticmethod
    #kwargs can contain: seller_firm_public_id
    def process_seller_firm_information_files_upload(file: BinaryIO, claimed: bool, **kwargs: Dict[str, str]) -> Dict:
        BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config['BASE_PATH_STATIC_DATA_SELLER_FIRM']

        file_type = 'seller_firm'
        df_encoding = 'utf-8'
        delimiter = ';'
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM
        user_id = g.user.id


        # for file in seller_firm_information_files:
        file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
        response_objects = SellerFirmService.process_seller_firm_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, claimed=claimed, **kwargs)

        # response_object = {
        #     'status': 'success',
        #     'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(seller_firm_information_files)))
        # }

        return response_objects


    # celery task !!
    @staticmethod
    def process_seller_firm_information_file(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, **kwargs) -> List[Dict]:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_objects = SellerFirmService.create_seller_firms(df, file_path_in, user_id, **kwargs)

        InputService.move_file_to_out(file_path_in, basepath, file_type)


        return response_objects




    @staticmethod
    def create_seller_firms(df: pd.DataFrame, file_path_in: str, user_id: int, **kwargs) -> List[Dict]: #upload only for tax auditors
        error_counter = 0
        total_number_items = len(df.index)
        input_type = 'seller firm'  # only used for response objects

        for i in range(total_number_items):

            seller_firm_name = InputService.get_str_or_None(df, i, column='seller_firm_name')
            address = InputService.get_str_or_None(df, i, column='address')
            establishment_country_code = InputService.get_str(df, i, column='establishment_country_code')

            seller_firm_data = {
                'claimed': kwargs.get('claimed'),
                'created_by': user_id,
                'name': seller_firm_name,
                'address': address,
                'establishment_country_code': establishment_country_code
            }

            seller_firm = SellerFirmService.get_by_identifiers(seller_firm_name, address, establishment_country_code)
            if not seller_firm:
                try:
                    new_seller_firm = SellerFirmService.create(seller_firm_data)
                    new_seller_firm.accounting_firms.append(g.user.employer)
                    db.session.commit()

                except:
                    db.session.rollback()
                    error_counter += 1
                    db.session.commit()

            else:
                error_counter += 1

        response_objects = InputService.create_input_response_objects(file_path_in, input_type, total_number_items, error_counter)

        return response_objects
