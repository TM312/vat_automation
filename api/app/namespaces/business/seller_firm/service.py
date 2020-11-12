import os

from typing import List, BinaryIO, Dict
import pandas as pd
from datetime import datetime

from werkzeug.exceptions import Conflict, NotFound, Unauthorized, UnsupportedMediaType, UnprocessableEntity
from werkzeug.utils import secure_filename

from flask import g, current_app
from app.extensions import (
    db,
    socket_io)

from .model import SellerFirm
from .interface import SellerFirmInterface
#from .schema import SellerFirmSubSchema

from app.namespaces.utils.service import InputService, NotificationService
from app.namespaces.utils import SellerFirmNotification
from app.namespaces.tag.service import TagService

from app.extensions.socketio.emitters import SocketService


class SellerFirmService:
    @staticmethod
    def get_all() -> List[SellerFirm]:
        return SellerFirm.query.all()

    @staticmethod
    def get_by_name_establishment_country(seller_firm_name: str, establishment_country_code: str) -> SellerFirm:
        return SellerFirm.query.filter(
            SellerFirm.name == seller_firm_name,
            SellerFirm.establishment_country_code == establishment_country_code
            ).first()


    @staticmethod
    def get_by_identifiers(seller_firm_name: str, address: str, establishment_country_code: str ) -> SellerFirm:
        seller_firm = SellerFirmService.get_by_name_establishment_country(seller_firm_name, establishment_country_code)
        if not isinstance(seller_firm, SellerFirm):
            seller_firm = SellerFirm.query.filter(
                SellerFirm.address == address,
                SellerFirm.establishment_country_code == establishment_country_code
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


    # @staticmethod
    # def create_as_client(seller_firm_data_as_client: SellerFirmInterface) -> SellerFirm:

    #     name = seller_firm_data_as_client.get('name')
    #     establishment_country_code = seller_firm_data_as_client.get('establishment_country_code')

    #     if (
    #         isinstance(name, str) and
    #         isinstance(establishment_country_code, str)
    #         ):
    #         seller_firm = SellerFirmService.get_by_name_establishment_country(name, establishment_country_code)

    #         # !!! need to be handled differently
    #         if seller_firm:
    #             data_changes = {k:v for k,v in seller_firm_data_as_client.items() if (v is not None or k != 'name')}

    #             seller_firm.update(data_changes)
    #             db.session.commit()

    #             return seller_firm

    #     else:
    #         seller_firm_data = {
    #             'claimed': False,
    #             'created_by': g.user.id,
    #             'name': name,
    #             'address': seller_firm_data_as_client.get('address'),
    #             'establishment_country_code': establishment_country_code,
    #         }

    #         try:
    #             new_seller_firm = SellerFirmService.create(seller_firm_data)
    #             new_seller_firm.accounting_firms.append(g.user.employer)
    #             db.session.commit()
    #             return new_seller_firm

    #         except:
    #             db.session.rollback()
    #             raise




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
        If both, the latter one is prioritized.
        """
        if isinstance(kwargs.get('seller_firm_public_id'), str):
            seller_firm_public_id = kwargs['seller_firm_public_id']

        elif ('df' and 'i') in kwargs and isinstance(kwargs['df'], pd.DataFrame) and isinstance(kwargs['i'], int):
            seller_firm_public_id = InputService.get_str_or_None(df=kwargs['df'], i=kwargs['i'], column='seller_firm_public_id')

        else:
            raise

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)

        if isinstance(seller_firm, SellerFirm):
            seller_firm_id = seller_firm.id
            return seller_firm_id


    @staticmethod
    def process_data_upload(seller_firm_public_id, file: BinaryIO):

        """
        This function is the main entry point for any file uploaded that relate to a seller firm's data,
        i.e. account data,
            item data,
            distance sale data,
            vat numbers,
            transaction reports

        The processing of these functions is handled asynchronously as a celery task.

        A SellerFirmNotification is created/updated in the course of processing.

        """
        DATA_ALLOWED_EXTENSIONS = current_app.config.DATA_ALLOWED_EXTENSIONS
        DATAPATH = current_app.config.DATAPATH
        user_id = g.user.id

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        seller_firm_id = seller_firm.id

        # each file is initially stored in a temp folder and undergoes sanitizing
        try:
            file_path_tbd = InputService.store_file(file=file, allowed_extensions=DATA_ALLOWED_EXTENSIONS, basepath=DATAPATH, file_type='tbd')
        except Exception as e:
            print(e, flush=True)
            SocketService.emit_status_error_invalid_file(message = e.description)
            return False

        original_filename = InputService.get_secure_filename(file)

        # setting vars
        df_encoding = 'utf-8'
        delimiter = ';' if InputService.infer_delimiter(file_path_tbd) != '\t' else '\t'

        try:
            df = InputService.read_file_path_into_df(file_path_tbd, df_encoding, delimiter)
        except:
            message = 'Can not read file. Make sure not to change the file encoding ("{}") and delimiter ("{}") of the template.'.format(df_encoding, delimiter)
            SocketService.emit_status_error_invalid_file(message)
            return False

        try:
            file_type = InputService.determine_file_type(df)
        except:
            message = 'Can not identify the type of the uploaded file "{}". Make sure to use one of the templates when uploading data.'.format(os.path.basename(file_path_tbd)[:128])
            SocketService.emit_status_error_invalid_file(message)
            return False

        try:
            data_type = InputService.determine_data_type(file_type)
        except:
            message = 'Can not identify the type of the uploaded file "{}". Make sure to use one of the templates when uploading data.'.format(os.path.basename(file_path_tbd)[:128])
            SocketService.emit_status_error_invalid_file(message)
            return False

        #Prepare SellerFirmNotification
        seller_firm_notification_data = {
            'subject': 'Data Upload',
            'status': 'success',
            'seller_firm_id': seller_firm_id,
            'created_by': user_id
        }


        # processing starts here
        file_path_in = InputService.move_data_to_file_type(file_path_tbd, data_type, file_type, seller_firm_id=seller_firm_id)

        if data_type == 'static':
            basepath = current_app.config.BASE_PATH_STATIC_DATA_SELLER_FIRM

            if file_type == 'account_list':
                from app.tasks.asyncr import async_handle_account_data_upload

                response_object = async_handle_account_data_upload.apply_async(
                    retry=True,
                    args=[file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm_id, seller_firm_notification_data]
                    )


            elif file_type == 'distance_sale_list':
                from app.tasks.asyncr import async_handle_distance_sale_data_upload
                response_object = async_handle_distance_sale_data_upload.apply_async(
                    retry=True,
                    args=[file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm_id, seller_firm_notification_data]
                    )


            elif file_type == 'item_list':
                from app.tasks.asyncr import async_handle_item_data_upload
                response_object = async_handle_item_data_upload.apply_async(
                    retry=True,
                    args=[file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm_id, seller_firm_notification_data]
                    )

            elif file_type == 'vat_numbers':
                from app.tasks.asyncr import async_handle_vatin_data_upload
                response_object = async_handle_vatin_data_upload.apply_async(
                    retry=True,
                    args=[file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm_id, seller_firm_notification_data]
                    )



        elif data_type == 'recurring':
            basepath = current_app.config.BASE_PATH_TRANSACTION_DATA_SELLER_FIRM

            if file_type == 'transactions_amazon':
                from app.tasks.asyncr import async_handle_transaction_input_data_upload
                response_object = async_handle_transaction_input_data_upload.apply_async(
                    retry=True,
                    args=[file_path_in, file_type, df_encoding, delimiter, basepath,
                          user_id, seller_firm_id, seller_firm_notification_data]
                )

        else:
            current_app.logger.warning('Unrecogizable Seller Firm Data has been uploaded by {} ({})'.format(g.user.name, user_id))
            message = 'Can not identify the type of the uploaded file "{}". Make sure to use one of the templates when uploading data.'.format(os.path.basename(file_path_in)[:128])
            original_filename = InputService.get_secure_filename(file)
            SocketService.emit_status_error_invalid_file(message)
            return False



        return {
            "task_id": response_object.id,
        }




    @staticmethod
    #kwargs can contain: seller_firm_public_id
    def process_seller_firm_information_file_upload(file: BinaryIO) -> Dict:
        """
        This function is the entry point for files uploaded to create new seller firms.

        The processing of these functions is handled asynchronously as a celery task.

        A SellerFirmNotification is created/updated in the course of processing.

        """

        user_id = g.user.id
        if g.user.u_type == 'seller':
            claimed = True
        else:
            claimed = False

        DATA_ALLOWED_EXTENSIONS = current_app.config.DATA_ALLOWED_EXTENSIONS
        DATAPATH = current_app.config.DATAPATH

        # each file is initially stored in a temp folder and undergoes sanitizing
        try:
            file_path_tbd = InputService.store_file(file=file, allowed_extensions=DATA_ALLOWED_EXTENSIONS, basepath=DATAPATH, file_type='tbd')
        except Exception as e:
            SocketService.emit_status_error_invalid_file(message = e.description)
            return False


        df_encoding = 'utf-8'
        delimiter = ';'

        #Prepare SellerFirmNotification
        seller_firm_notification_data = {
            'status': 'success',
            'created_by': user_id
        }

        # setting vars
        try:
            df = InputService.read_file_path_into_df(file_path_tbd, df_encoding, delimiter)
        except:
            message = 'Can not read file. Make sure not to change the file encoding ("{}") and delimiter ("{}") of the template.'.format(df_encoding, delimiter)
            SocketService.emit_status_error_invalid_file(message)
            return False

        try:
            file_type = InputService.determine_file_type(df)
        except:
            message = 'Can not identify the type of the uploaded file "{}". Make sure to use one of the templates when uploading data.'.format(os.path.basename(file_path_tbd)[:128])
            SocketService.emit_status_error_invalid_file(message)
            return False

        try:
            data_type = InputService.determine_data_type(file_type)
        except:
            message = 'Can not identify the type of the uploaded file "{}". Make sure to use one of the templates when uploading data.'.format(os.path.basename(file_path_tbd)[:128])
            SocketService.emit_status_error_invalid_file(message)
            return False

        # processing starts here
        file_path_in = InputService.move_data_to_file_type(file_path_tbd, data_type, file_type)

        if data_type == 'business':
            basepath = current_app.config.BASE_PATH_BUSINESS_DATA

            from app.tasks.asyncr import async_handle_seller_firm_data_upload

            response_object = async_handle_seller_firm_data_upload.apply_async(
                retry=True,
                args=[file_path_in, file_type, df_encoding, delimiter, basepath, user_id, claimed, seller_firm_notification_data]
                )


        else:
            current_app.logger.warning('Unrecogizable Seller Firm Data has been uploaded by {} (id: {})'.format(g.user.name, user_id))
            message = 'Can not identify the type of the uploaded file "{}". Make sure to use one of the templates when uploading data.'.format(os.path.basename(file_path_in)[:128])
            SocketService.emit_status_error_invalid_file(message)
            return False

        return {
            "task_id": response_object.id,
        }


    @staticmethod
    def handle_seller_firm_data_upload(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, claimed: bool, seller_firm_notification_data: Dict) -> Dict:
        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_object = SellerFirmService.create_seller_firms(df, file_path_in, user_id, claimed, seller_firm_notification_data)

        InputService.move_file_to_out(file_path_in, basepath, file_type)

        return response_object



    @staticmethod
    # upload only for tax auditors
    def create_seller_firms(df: pd.DataFrame, file_path_in: str, user_id: int, claimed: bool, seller_firm_notification_data: Dict) -> List[Dict]:
        from app.namespaces.user.service_parent import UserService
        from app.namespaces.distance_sale.service import DistanceSaleService

        total = total_number_items = len(df.index)
        original_filename = os.path.basename(file_path_in)[:128]
        object_type = 'seller_firm'  # only used for response objects
        object_type_human_read = 'seller firm'
        seller_firm_socket_list = []
        duplicate_list = []
        duplicate_counter = 0

        user = UserService.get_by_id(user_id)

        for i in range(total_number_items):
            current = i + 1

            try:
                seller_firm_name = InputService.get_str_or_None(df, i, column='seller_firm_name')
            except:
                # send error status via socket
                SocketService.emit_status_error_column_read(current, object_type, column_name='seller_firm_name')
                return False

            try:
                address = InputService.get_str_or_None(df, i, column='address')
            except:
                # send error status via socket
                SocketService.emit_status_error_column_read(current, object_type, column_name='address')
                return False

            try:
                establishment_country_code = InputService.get_str(df, i, column='establishment_country_code')
            except:
                # send error status via socket
                SocketService.emit_status_error_column_read(current, object_type, column_name='establishment_country_code')
                return False

            if len(establishment_country_code) > 2:
                # send error status via socket
                message = 'Invalid country code in column "establishment_country_code", row {}. Make sure to use the country code as defined in "ISO 3166-1 alpha-2"'.format(current)
                SocketService.emit_status_error_invalid_value(object_type, message)
                return False


            seller_firm_data = {
                'claimed': claimed,
                'created_by': user_id,
                'name': seller_firm_name,
                'address': address,
                'establishment_country_code': establishment_country_code
            }

            seller_firm = SellerFirmService.get_by_identifiers(seller_firm_name, address, establishment_country_code)
            if isinstance(seller_firm, SellerFirm):
                if not duplicate_counter > 2:
                    message = 'The uploaded seller firm "{}" (row: {}) is already in the database. Registration has been skipped.'.format(seller_firm.name, current+1)
                    SocketService.emit_status_info(object_type, message)

                total -= 1
                duplicate_list.append('Row {}: {}'.format(current, seller_firm.name))
                duplicate_counter += 1
                continue


            else:
                try:
                    seller_firm = SellerFirmService.create(seller_firm_data)

                    if user.u_type == 'tax_auditor':
                        seller_firm.accounting_firms.append(user.employer)
                    db.session.commit()

                except:
                    db.session.rollback()
                    message = 'Error at seller firm in row {}. Please recheck or get in contact with one of the admins.'.format(current+1)
                    SocketService.emit_status_error(object_type, message)
                    return False

                # create deactivated distance sales for seller firm
                DistanceSaleService.create_inactive_ds_from_thresholds(seller_firm.id)



                # send status update via socket
                SocketService.emit_status_success(current, total, original_filename, object_type)


        # send final status via socket
        SocketService.emit_status_final(total, original_filename, object_type, object_type_human_read, duplicate_list=duplicate_list)

        if total == 1:
            seller_firm_notification_data['subject'] = 'New Seller Firm'
            seller_firm_notification_data['seller_firm_id'] = seller_firm.id

        elif total > 1:
            seller_firm_notification_data['subject'] = 'New Seller Firms'
            message = '{} new seller firms'.format(total)
            seller_firm_notification_data['message'] = message

        NotificationService.create_seller_firm_notification(seller_firm_notification_data)


        return True
