from typing import List, Dict, BinaryIO
import os
import pandas as pd
from datetime import date, timedelta, datetime
from flask import g, current_app
from app.extensions import (
    db,
    socket_io)

from . import DistanceSale
from .interface import DistanceSaleInterface
from .schema import DistanceSaleSubSchema

from ..utils.service import InputService, NotificationService
from ..tag.service import TagService

from app.extensions.socketio.emitters import SocketService


class DistanceSaleService:
    @staticmethod
    def get_all() -> List[DistanceSale]:
        return DistanceSale.query.all()

    @staticmethod
    def get_by_id(distance_sale_id: int) -> DistanceSale:
        return DistanceSale.query.get(distance_sale_id)

    @staticmethod
    def get_by_public_id(distance_sale_public_id: str) -> DistanceSale:
        return DistanceSale.query.filter_by(public_id = distance_sale_public_id).first()

    @staticmethod
    def get_by_arrival_country_seller_firm_id_date(arrival_country_code, seller_firm_id, date) -> DistanceSale:
        return DistanceSale.query.filter(
            DistanceSale.arrival_country_code == arrival_country_code,
            DistanceSale.seller_firm_id == seller_firm_id,
            DistanceSale.valid_from <= date,
            DistanceSale.valid_to >= date).first()


    @staticmethod
    def update(distance_sale_public_id: DistanceSale, data_changes: DistanceSaleInterface) -> DistanceSale:
        distance_sale.update(data_changes)
        db.session.commit()
        return distance_sale

    @staticmethod
    def update_by_public_id(distance_sale_public_id: str, data_changes: DistanceSaleInterface) -> DistanceSale:
        distance_sale = DistanceSaleService.get_by_public_id(distance_sale_public_id)
        if distance_sale:
            distance_sale.update(data_changes)
            db.session.commit()
            return distance_sale

    @staticmethod
    def create_by_seller_firm_public_id(seller_firm_public_id: str, distance_sale_data: DistanceSaleInterface) -> DistanceSale:
        from ..business.seller_firm.service import SellerFirmService

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if seller_firm:
            distance_sale = DistanceSaleService.get_by_arrival_country_seller_firm_id_date(distance_sale_data['arrival_country_code'], seller_firm.id, distance_sale_data['valid_from'])
            if distance_sale:
                if distance_sale.active == distance_sale_data['active']:
                    return distance_sale
                else:
                    data_changes = {
                        'valid_to': valid_from - timedelta(days=1)
                    }
                    distance_sale.update(data_changes)
                    db.session.commit()

            distance_sale_data['seller_firm_id'] = seller_firm.id
            distance_sale = DistanceSaleService.create(distance_sale_data)

        return distance_sale




    @staticmethod
    def delete_by_id(distance_sale_id: int) -> List[int]:
        distance_sale = DistanceSaleService.get_by_id(distance_sale_id)
        if not distance_sale:
            return []
        db.session.delete(distance_sale)
        db.session.commit()
        return [distance_sale_id]

    @staticmethod
    def delete_by_public_id(distance_sale_public_id: str) -> List[int]:
        distance_sale = DistanceSaleService.get_by_public_id(distance_sale_public_id)
        if not distance_sale:
            return []
        db.session.delete(distance_sale)
        db.session.commit()
        return [distance_sale_public_id]

    @staticmethod
    def process_single_submit(seller_firm_public_id: str, distance_sale_data: DistanceSaleInterface):

        distance_sale_data['created_by'] = g.user.id
        distance_sale_data['valid_from'] = datetime.strptime(distance_sale_data['valid_from'], "%Y-%m-%d").date()

        if not 'valid_to' in distance_sale_data:
            TAX_DEFAULT_VALIDITY = current_app.config.TAX_DEFAULT_VALIDITY
            distance_sale_data['valid_to'] = TAX_DEFAULT_VALIDITY

        else:
            distance_sale_data['valid_to'] = datetime.strptime(distance_sale_data['valid_to'], "%Y-%m-%d").date()

        distance_sale = DistanceSaleService.create_by_seller_firm_public_id(seller_firm_public_id, distance_sale_data)

        return distance_sale



    @staticmethod
    def process_distance_sale_files_upload(distance_sale_information_files: List[BinaryIO], seller_firm_public_id: str) -> Dict:
        from ..business.seller_firm.service import SellerFirmService

        BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config.BASE_PATH_STATIC_DATA_SELLER_FIRM

        file_type = 'distance_sale_list'
        df_encoding = 'utf-8'
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM
        user_id = g.user.id
        delimiter = ';'
        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)

        for file in distance_sale_information_files:
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            DistanceSaleService.process_distance_sale_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm.id)

        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(distance_sale_information_files)))
        }

        return response_object


    @staticmethod
    def handle_distance_sale_data_upload(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: Dict) -> Dict:
        response_object = DistanceSaleService.process_distance_sale_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm_id)
        tag = TagService.get_by_code('DISTANCE_SALE')
        NotificationService.handle_seller_firm_notification_data_upload(seller_firm_id, user_id, tag, seller_firm_notification_data)

        return response_object




    @staticmethod
    def process_distance_sale_information_file(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int) -> List[Dict]:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_objects = DistanceSaleService.create_distance_sales(df, file_path_in, user_id, seller_firm_id)

        InputService.move_file_to_out(file_path_in, basepath, file_type)


        return response_objects




    @staticmethod
    def create_distance_sales(df: pd.DataFrame, file_path_in: str, user_id: int, seller_firm_id: int) -> List[Dict]:

        total = total_number_distance_sales = len(df.index)
        original_filename = os.path.basename(file_path_in)[:128]
        object_type = 'distance_sale'
        object_type_human_read = 'distance sale'
        distance_sale_socket_list = []
        duplicate_list = []
        duplicate_counter = 0


        if not seller_firm_id:
            # send error status via socket
            SocketService.emit_status_error_no_seller_firm(object_type)
            return False

        for i in range(total_number_distance_sales):
            current = i + 1

            try:
                valid_from = InputService.get_date_or_None(df, i, column='valid_from')
            except:
                # send error status via socket
                SocketService.emit_status_error_column_read(current, object_type, column_name='valid_from')
                return False

            try:
                valid_to = InputService.get_date_or_None(df, i, column='valid_to')
            except:
                # send error status via socket
                SocketService.emit_status_error_column_read(current, object_type, column_name='valid_to')
                return False

            try:
                arrival_country_code = InputService.get_str(df, i, column='arrival_country_code')
            except:
                # send error status via socket
                SocketService.emit_status_error_column_read(current, object_type, column_name='arrival_country_code')
                return False

            try:
                active = InputService.get_bool(df, i, column='active', value_true=True)
            except:
                # send error status via socket
                SocketService.emit_status_error_column_read(current, object_type, column_name='active')
                return False

            if not valid_from:
                valid_from = date.today()
            if not valid_to:
                TAX_DEFAULT_VALIDITY = current_app.config.TAX_DEFAULT_VALIDITY
                valid_to = TAX_DEFAULT_VALIDITY



            distance_sale = DistanceSaleService.get_by_arrival_country_seller_firm_id_date(arrival_country_code, seller_firm_id, valid_from)
            if distance_sale:
                if distance_sale.active == active:
                    active_human_read = 'active' if active else 'inactive'
                    if not duplicate_counter > 2:
                        message = 'The distance sale for {} ({}). Registration has been skipped.'.format(distance_sale.arrival_country_code, active_human_read)
                        SocketService.emit_status_info(object_type, message)
                    total -= 1
                    duplicate_list.append('{}-{}'.format(distance_sale.arrival_country_code, active_human_read))
                    duplicate_counter += 1
                    continue

                else:
                    data_changes = {
                        'valid_to': valid_from - timedelta(days=1)
                    }
                    distance_sale.update(data_changes)
                    db.session.commit()


            distance_sale_data = {
                'created_by': user_id,
                'original_filename': original_filename,
                'seller_firm_id': seller_firm_id,
                'valid_from': valid_from,
                'valid_to': valid_to,
                'arrival_country_code': arrival_country_code,
                'active': active
            }

            try:
                new_distance_sale = DistanceSaleService.create(distance_sale_data)

            except:
                db.session.rollback()

                # send error status via socket
                message = 'Error at {} arrival country "{}" (file: {}). Please recheck.'.format(object_type_human_read, arrival_country_code, original_filename)
                SocketService.emit_status_error(current, total, object_type, message)
                return False

            # send status update via socket
            SocketService.emit_status_success(current, total, original_filename, object_type)

            # push new distance sale to vuex via socket
            distance_sale_json = DistanceSaleSubSchema.get_distance_sale_sub(new_distance_sale)

            if total < 10:
                SocketService.emit_new_object(distance_sale_json, object_type)

            else:
                distance_sale_socket_list.append(distance_sale_json)
                if current % 10 == 0 or current == total:
                    SocketService.emit_new_objects(distance_sale_socket_list, object_type)
                    distance_sale_socket_list = []



        # send final status via socket
        SocketService.emit_status_final(total, original_filename, object_type, object_type_human_read, duplicate_list=duplicate_list)

        return True


    @staticmethod
    def create(distance_sale_data: DistanceSaleInterface) -> DistanceSale:

        new_distance_sale = DistanceSale(
            created_by = distance_sale_data.get('created_by'),
            original_filename = distance_sale_data.get('original_filename'),
            valid_from = distance_sale_data.get('valid_from'),
            valid_to = distance_sale_data.get('valid_to'),
            seller_firm_id=distance_sale_data.get('seller_firm_id'),
            arrival_country_code = distance_sale_data.get('arrival_country_code'),
            active = distance_sale_data.get('active')
        )

        #add seller firm to db
        db.session.add(new_distance_sale)

        db.session.commit()

        return new_distance_sale



    @staticmethod
    def get_active(seller_firm_id: int, arrival_country_code: str, tax_date: date) -> bool:
        distance_sale=DistanceSale.query.filter(
            DistanceSale.seller_firm_id==seller_firm_id,
            DistanceSale.arrival_country_code==arrival_country_code,
            DistanceSale.valid_from<=tax_date, DistanceSale.valid_to>=tax_date
        ).first()
        if distance_sale:
            return distance_sale.active
