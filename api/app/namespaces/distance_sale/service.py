from typing import List, Dict, BinaryIO
import os
import pandas as pd
from datetime import date, timedelta, datetime
from flask import g, current_app
from app.extensions import (
    db,
    socket_io)

from . import DistanceSale, DistanceSaleHistory
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
    def get_by_arrival_country_seller_firm_id(arrival_country_code, seller_firm_id) -> DistanceSale:
        return DistanceSale.query.filter(
            DistanceSale.arrival_country_code == arrival_country_code,
            DistanceSale.seller_firm_id == seller_firm_id
            ).first()


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
            try:
                db.session.commit()
            except:
                db.session.rollbac()
                raise
            return distance_sale

    @staticmethod
    def create_by_seller_firm_public_id(seller_firm_public_id: str, distance_sale_data: DistanceSaleInterface) -> DistanceSale:
        from ..business.seller_firm.service import SellerFirmService

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if seller_firm:
            arrival_country_code = distance_sale_data['arrival_country_code']
            active = distance_sale_data.get('active')
            valid_from = distance_sale_data.get('valid_from')

            distance_sale = DistanceSaleService.get_by_arrival_country_seller_firm_id(arrival_country_code, seller_firm.id)
            if distance_sale:
                if distance_sale.active == active or active == DistanceSaleHistoryService.get_active(seller_firm_id, arrival_country_code, valid_from):
                    return distance_sale
                else:
                    distance_sale_history = DistanceSaleHistoryService.get_by_ds_id_date(distance_sale.id, valid_from)
                    data_changes = {
                        'active':  active
                    }
                    try:
                        if isinstance(valid_from, date):
                            if distance_sale_history.valid_from != valid_from:
                                distance_sale.update(data_changes, valid_from=valid_from)

                            else:
                                distance_sale.update(data_changes, valid_from=distance_sale_history.valid_from)

                        else:
                            distance_sale.update(data_changes)


                        db.session.commit()
                    except:
                        db.session.rollback()
                        raise

            else:
                distance_sale_data['seller_firm_id'] = seller_firm.id
                distance_sale = DistanceSaleService.create(distance_sale_data)

        else:
            raise

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


        distance_sale = DistanceSaleService.create_by_seller_firm_public_id(seller_firm_public_id, distance_sale_data)

        return distance_sale




    @staticmethod
    def handle_distance_sale_data_upload(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: Dict) -> Dict:
        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_object = DistanceSaleService.create_distance_sales(df, file_path_in, user_id, seller_firm_id)
        tag = TagService.get_by_code('DISTANCE_SALE')
        NotificationService.handle_seller_firm_notification_data_upload(seller_firm_id, user_id, tag, seller_firm_notification_data)
        InputService.move_file_to_out(file_path_in, basepath, file_type)

        return response_object




    @staticmethod
    def create_distance_sales(df: pd.DataFrame, file_path_in: str, user_id: int, seller_firm_id: int) -> List[Dict]:

        total = total_number_distance_sales = len(df.index)
        original_filename = os.path.basename(file_path_in)[:128]
        object_type = 'distance_sale'
        object_type_human_read = 'distance sale'
        distance_sale_socket_list = []
        duplicate_list = []
        duplicate_counter = 0
        arrival_country_list = []


        if not seller_firm_id:
            # send error status via socket
            SocketService.emit_status_error_no_seller_firm(object_type)
            return False

        for i in range(total_number_distance_sales):
            current = i + 1

            try:
                valid_from = InputService.get_date_or_None(df, i, column='valid_from')
                valid_from = valid_from if isinstance(valid_from, date) else current_app.config.SERVICE_START_DATE

            except:
                # send error status via socket
                SocketService.emit_status_error_column_read(current, object_type, column_name='valid_from')
                return False

            try:
                arrival_country_code = InputService.get_str(df, i, column='arrival_country_code')
            except:
                # send error status via socket
                SocketService.emit_status_error_column_read(current, object_type, column_name='arrival_country_code')
                return False

            if arrival_country_code not in arrival_country_list:
                arrival_country_list.append(arrival_country_code)

            try:
                active = InputService.get_bool(df, i, column='active', value_true=True)
            except:
                # send error status via socket
                SocketService.emit_status_error_column_read(current, object_type, column_name='active')
                return False

            distance_sale = DistanceSaleService.get_by_arrival_country_seller_firm_id(arrival_country_code, seller_firm_id)
            if distance_sale:
                if distance_sale.active == active or active == DistanceSaleHistoryService.get_active(seller_firm_id, arrival_country_code, valid_from):
                    active_human_read = 'active' if active else 'inactive'
                    if not duplicate_counter > 2:
                        message = 'The {} registration for {} (state: {}) is already in the database. Registration has been skipped.'.format(object_type_human_read, distance_sale.arrival_country_code, active_human_read)
                        SocketService.emit_status_info(object_type, message)
                    total -= 1
                    duplicate_list.append('{}-{}'.format(distance_sale.arrival_country_code, active_human_read))
                    duplicate_counter += 1
                    continue

                else:

                    distance_sale_history = DistanceSaleHistoryService.get_by_ds_id_date(distance_sale.id, valid_from)

                    data_changes = {
                        'active': active
                    }

                    try:
                        if distance_sale_history.valid_from != valid_from:
                            distance_sale.update(data_changes, valid_from=valid_from)
                        else:
                            distance_sale.update(data_changes, valid_from=distance_sale_history.valid_from)
                        db.session.commit()

                    except:
                        db.session.rollback()
                        message = 'Error at {} registration for "{}" (file: {}). Please recheck.'.format(object_type_human_read, arrival_country_code, original_filename)
                        SocketService.emit_status_error(object_type, message)
                        return False

            else:
                distance_sale_data = {
                    'created_by': user_id,
                    'valid_from': valid_from,
                    'original_filename': original_filename,
                    'seller_firm_id': seller_firm_id,
                    'arrival_country_code': arrival_country_code,
                    'active': active
                }

                try:
                    new_distance_sale = DistanceSaleService.create(distance_sale_data)

                except:
                    db.session.rollback()

                    # send error status via socket
                    message = 'Error at {} arrival country "{}" (file: {}). Please recheck.'.format(object_type_human_read, arrival_country_code, original_filename)
                    SocketService.emit_status_error(object_type, message)
                    return False

                # send status update via socket
                SocketService.emit_status_success(current, total, original_filename, object_type)


        # push new distance sale to vuex via socket
        for arrival_country_code in arrival_country_list:
            distance_sale = DistanceSaleService.get_by_arrival_country_seller_firm_id(arrival_country_code, seller_firm_id)
            distance_sale_json = DistanceSaleSubSchema.get_distance_sale_sub(distance_sale)

            distance_sale_socket_list.append(distance_sale_json)

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
            seller_firm_id=distance_sale_data.get('seller_firm_id'),
            arrival_country_code = distance_sale_data.get('arrival_country_code'),
            active = distance_sale_data.get('active')
        )

        #add seller firm to db
        db.session.add(new_distance_sale)
        db.session.commit()

        try:
            DistanceSaleHistoryService.create(distance_sale_data, new_distance_sale.id)
        except:
            raise #!!!


        return new_distance_sale




class DistanceSaleHistoryService:

    @staticmethod
    def get_by_ds_id_date(distance_sale_id: int, date: date) -> DistanceSaleHistory:
        return DistanceSaleHistory.query.filter(
            DistanceSaleHistory.distance_sale_id==distance_sale_id,
            DistanceSaleHistory.valid_from<=date,
            DistanceSaleHistory.valid_to>=date
            ).first()


    @staticmethod
    def create(distance_sale_data, distance_sale_id):

        # create new distance_sale history
        new_distance_sale_history = DistanceSaleHistory(
            valid_from=distance_sale_data.get('valid_from'),
            arrival_country_code = distance_sale_data.get('arrival_country_code'),
            active=distance_sale_data.get('active'),
            distance_sale_id=distance_sale_id
        )

        db.session.add(new_distance_sale_history)
        db.session.commit()

    @staticmethod
    def get_active(seller_firm_id: int, arrival_country_code: str, date: date) -> bool:
        distance_sale_history=DistanceSaleHistory.query.filter(
            DistanceSaleHistory.arrival_country_code==arrival_country_code,
            DistanceSaleHistory.valid_from<=date, DistanceSaleHistory.valid_to>=date
            ).join(
                DistanceSaleHistory.distance_sale, aliased=True).filter_by(seller_firm_id=seller_firm_id
                ).first()
        try:
            return distance_sale_history.active
        except:
            raise
