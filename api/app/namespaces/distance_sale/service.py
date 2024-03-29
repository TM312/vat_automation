from typing import List, Dict, BinaryIO
import os
import pandas as pd
from datetime import date, timedelta, datetime
from flask import g, current_app
from werkzeug.exceptions import UnprocessableEntity, ExpectationFailed
from app.extensions import (
    db,
    socket_io)

from . import DistanceSale, DistanceSaleHistory
from .interface import DistanceSaleInterface
from .schema import DistanceSaleSubSchema

from app.namespaces.utils.service import InputService, NotificationService, TemplateService
from app.namespaces.tag.service import TagService

from app.extensions.socketio.emitters import SocketService


class DistanceSaleService:
    @staticmethod
    def get_all() -> List[DistanceSale]:
        return DistanceSale.query.all()

    @staticmethod
    def get_all_by_seller_firm_id(seller_firm_id: int) -> List[DistanceSale]:
        return DistanceSale.query.filter_by(seller_firm_id = seller_firm_id).all()

    @staticmethod
    def get_by_id(distance_sale_id: int) -> DistanceSale:
        return DistanceSale.query.get(distance_sale_id)

    @staticmethod
    def get_by_public_id(distance_sale_public_id: str) -> DistanceSale:
        return DistanceSale.query.filter_by(public_id = distance_sale_public_id).first()


    @staticmethod
    def get_by_arrival_country_seller_firm_id(arrival_country_code: str, seller_firm_id: int) -> DistanceSale:
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
        from app.namespaces.business.seller_firm.service import SellerFirmService

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if seller_firm:
            arrival_country_code = distance_sale_data['arrival_country_code']
            active = distance_sale_data.get('active')
            valid_from = distance_sale_data.get('valid_from')

            distance_sale = DistanceSaleService.get_by_arrival_country_seller_firm_id(arrival_country_code, seller_firm.id)
            if distance_sale:
                distance_sale_history = DistanceSaleHistoryService.get_by_relationship_date(distance_sale.id, valid_from)
                if active == distance_sale_history.active:
                    return distance_sale
                else:
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
        InputService.move_file_to_out(file_path_in, basepath, file_type, business_id=seller_firm_id)

        return response_object

    @staticmethod
    def get_df_vars(df: pd.DataFrame, i: int, current: int, object_type: str, seller_firm_id: int) -> List:

        try:
            arrival_country_code = InputService.get_str(df, i, column='arrival_country_code')
        except:
            raise UnprocessableEntity('arrival_country_code')

        distance_sale = DistanceSaleService.get_by_arrival_country_seller_firm_id(arrival_country_code, seller_firm_id)
        try:
            valid_from = TemplateService.get_valid_from(df, i, distance_sale, DistanceSale)

        except:
            raise UnprocessableEntity('valid_from')

        try:
            active = InputService.get_bool(df, i, column='active', value_true=True)
        except:
            raise UnprocessableEntity('active')

        try:
            ship_from_rule = InputService.get_bool(df, i, column='ship_from_rule', value_true=True)
        except:
            raise UnprocessableEntity('ship_from_rule')

        if not isinstance(arrival_country_code, str):
            raise ExpectationFailed('arrival_country_code')

        if not isinstance(active, bool):
            raise ExpectationFailed('active')

        if not isinstance(valid_from, date):
            raise ExpectationFailed('valid_from')

        return valid_from, arrival_country_code, active, ship_from_rule


    @staticmethod
    def update_taxable_turnover_amount_365d_all_ds(seller_firm_id: int, end_date: date, original_filename: str):
        distance_sales = DistanceSaleService.get_all_by_seller_firm_id(seller_firm_id)
        for distance_sale in distance_sales:
            DistanceSaleService.update_taxable_turnover_amount_365d_single(seller_firm_id, distance_sale.arrival_country_code, end_date, original_filename)

         # first cleared
        SocketService.emit_clear_objects('distance_sale')
        # then refilled
        DistanceSaleService.push_all_by_seller_firm_id(seller_firm_id, 'distance_sale')


    @staticmethod
    def update_taxable_turnover_amount_365d_single(seller_firm_id: int, arrival_country_code: str, end_date: date, original_filename: str):
        from app.namespaces.tax_record.service import TaxRecordService
        from app.namespaces.transaction.service import TransactionService


        start_date = end_date - timedelta(days=365) #check if 365 or beginning of year
        transactions = TransactionService.get_by_validity_tax_jurisdiction_seller_firm(start_date, end_date, seller_firm_id, arrival_country_code)

        if len(transactions) == 0:
            return False

        taxable_turnover_amount = TaxRecordService.get_taxable_turnover_amount_365d(seller_firm_id, arrival_country_code, end_date, transactions)
        last_tax_date = max(transaction.tax_date for transaction in transactions)

        distance_sale = DistanceSaleService.get_by_arrival_country_seller_firm_id(arrival_country_code, seller_firm_id)


        if not isinstance(distance_sale, DistanceSale):
            raise

        if taxable_turnover_amount == 0 or taxable_turnover_amount == distance_sale.taxable_turnover_amount:
            return False

        else:
            data_changes = {
                'valid_from': end_date,
                'taxable_turnover_amount': taxable_turnover_amount,
                'last_tax_date': last_tax_date,
                'original_filename': original_filename
            }

            try:
                distance_sale.update(data_changes)
                db.session.commit()
            except:
                db.session.rollback()
                raise

            return True



    @staticmethod
    def create_inactive_ds_from_thresholds(seller_firm_id: int) -> None:
        from app.namespaces.tax.vat_threshold.service import VatThresholdService
        vat_thresholds = VatThresholdService.get_all()
        vat_threshold_country_codes = [vat_threshold.country_code for vat_threshold in vat_thresholds]

        distance_sale_data = {
            'valid_from': datetime.strptime('01-01-2000', '%d-%m-%Y').date(),
            'seller_firm_id': seller_firm_id
        }

        for vat_threshold in vat_thresholds:
            distance_sale_data['arrival_country_code'] = vat_threshold.country_code
            try:
                DistanceSaleService.create(distance_sale_data)
            except:
                db.session.rollback()
                raise



    @staticmethod
    def create_distance_sales(df: pd.DataFrame, file_path_in: str, user_id: int, seller_firm_id: int) -> List[Dict]:

        total = total_number_distance_sales = len(df.index)
        original_filename = os.path.basename(file_path_in)[:128]
        object_type = 'distance_sale'
        object_type_human_read = 'distance sale'
        duplicate_list = []
        duplicate_counter = 0


        if not seller_firm_id:
            SocketService.emit_status_error_no_seller_firm(object_type)
            return False

        SocketService.emit_status_success(0, total, original_filename, object_type)

        for i in range(total_number_distance_sales):
            current = i + 1

            try:
                valid_from, arrival_country_code, active, ship_from_rule = DistanceSaleService.get_df_vars(df, i, current, object_type, seller_firm_id)
            except UnprocessableEntity as e:
                SocketService.emit_status_error_column_read(current, object_type, column_name=e.description)
                return False
            except ExpectationFailed as e:
                SocketService.emit_status_error_invalid_value(object_type, e.description)
                return False


            distance_sale = DistanceSaleService.get_by_arrival_country_seller_firm_id(arrival_country_code, seller_firm_id)

            distance_sale_data = {
                'valid_from': valid_from,
                'created_by': user_id,
                'original_filename': original_filename,
                'seller_firm_id': seller_firm_id,
                'arrival_country_code': arrival_country_code,
                'active': active,
                'ship_from_rule': ship_from_rule
            }

            # handling distance sale update
            if isinstance(distance_sale, DistanceSale):
                distance_sale_history = DistanceSaleHistoryService.get_by_relationship_date(distance_sale.id, valid_from)

                # handling exact duplicates
                # since a distance sale history is created by default when creating a seller firm, the history needs to be longer than 1 for the user to be notified
                if active == distance_sale_history.active and ship_from_rule == distance_sale_history.ship_from_rule and len(distance_sale.distance_sale_history) > 1:
                    active_human_read = 'active' if active else 'inactive'
                    if not duplicate_counter > 2:
                        message = 'The {} registration for {} (state: {}) is already in the database. Registration has been skipped.'.format(object_type_human_read, distance_sale.arrival_country_code, active_human_read)
                        SocketService.emit_status_info(object_type, message)

                    total -= 1
                    duplicate_list.append('{}-{}'.format(distance_sale.arrival_country_code, active_human_read))
                    duplicate_counter += 1
                    continue

                # updating distance_sale
                else:
                    data_changes = distance_sale_data
                    try:
                        distance_sale.update(data_changes)
                        db.session.commit()

                    except:
                        db.session.rollback()
                        message = 'Error at {} registration for "{}" (file: {}). Please recheck.'.format(object_type_human_read, arrival_country_code, original_filename)
                        SocketService.emit_status_error(object_type, message)
                        return False

            # handling new distance sale
            else:
                try:
                    new_distance_sale = DistanceSaleService.create(distance_sale_data)
                except:
                    db.session.rollback()
                    message = 'Error at {} arrival country "{}" (file: {}). Please recheck.'.format(object_type_human_read, arrival_country_code, original_filename)
                    SocketService.emit_status_error(object_type, message)
                    return False

                # send status update via socket
                SocketService.emit_status_success(current, total, original_filename, object_type)



        # following the succesful processing, the vuex store is being reset
        # first cleared
        SocketService.emit_clear_objects(object_type)
        # then refilled
        DistanceSaleService.push_all_by_seller_firm_id(seller_firm_id, object_type)

        # send final status via socket
        SocketService.emit_status_final(total, original_filename, object_type, object_type_human_read, duplicate_list=duplicate_list)

        return True


    # List all files in a directory using scandir(): Returns an iterator of all the objects in a directory including file attribute information

    @staticmethod
    def push_all_by_seller_firm_id(seller_firm_id: int, object_type: str) -> None:
        socket_list = []
        distance_sales = DistanceSaleService.get_all_by_seller_firm_id(seller_firm_id)
        for distance_sale in distance_sales:
            # push new distance sale to vuex via socket
            distance_sale_json = DistanceSaleSubSchema.get_distance_sale_sub(distance_sale)

            if len(distance_sales) < 10:
                SocketService.emit_new_object(distance_sale_json, object_type)
            else:
                socket_list.append(distance_sale_json)

        if len(socket_list) > 0:
            SocketService.emit_new_objects(socket_list, object_type)




    @staticmethod
    def create(distance_sale_data: DistanceSaleInterface) -> DistanceSale:

        new_distance_sale = DistanceSale(
            created_by = distance_sale_data.get('created_by'),
            original_filename = distance_sale_data.get('original_filename'),
            seller_firm_id=distance_sale_data.get('seller_firm_id'),
            arrival_country_code = distance_sale_data.get('arrival_country_code'),
            active = distance_sale_data.get('active'),
            ship_from_rule=distance_sale_data.get('ship_from_rule')
        )

        #add seller firm to db
        db.session.add(new_distance_sale)
        db.session.commit()

        distance_sale_data['distance_sale_id'] = new_distance_sale.id
        try:
            DistanceSaleHistoryService.create(distance_sale_data)
        except:
            db.session.rollback()
            raise

        return new_distance_sale




class DistanceSaleHistoryService:

    @staticmethod
    def get_oldest(distance_sale_id: int) -> DistanceSaleHistory:
        return DistanceSaleHistory.query.filter_by(distance_sale_id=distance_sale_id).order_by(DistanceSaleHistory.valid_from.asc()).first()

    @staticmethod
    def get_current(distance_sale_id: int) -> DistanceSaleHistory:
        return DistanceSaleHistory.query.filter_by(distance_sale_id=distance_sale_id).order_by(DistanceSaleHistory.valid_from.desc()).first()


    @staticmethod
    def get_by_relationship_date(distance_sale_id: int, date: date) -> DistanceSaleHistory:
        return DistanceSaleHistory.query.filter(
            DistanceSaleHistory.distance_sale_id == distance_sale_id,
            DistanceSaleHistory.valid_from <= date,
            DistanceSaleHistory.valid_to >= date
        ).first()


    @staticmethod
    def create(distance_sale_data) -> DistanceSaleHistory:

        # create new distance_sale history
        new_distance_sale_history = DistanceSaleHistory(
            distance_sale_id=distance_sale_data.get('distance_sale_id'),
            valid_from=distance_sale_data.get('valid_from'),
            valid_to=distance_sale_data.get('valid_to'),

            # mirrored attributes (no relationships)
            seller_firm_id=distance_sale_data.get('seller_firm_id'),
            created_by=distance_sale_data.get('created_by'),
            original_filename=distance_sale_data.get('original_filename'),
            arrival_country_code = distance_sale_data.get('arrival_country_code'),
            active=distance_sale_data.get('active'),
            ship_from_rule=distance_sale_data.get('ship_from_rule')
        )

        db.session.add(new_distance_sale_history)
        db.session.commit()

        return new_distance_sale_history

    @staticmethod
    def create_empty(distance_sale_id: int) -> DistanceSaleHistory:
        # create new distance_sale history
        new_distance_sale_history = DistanceSaleHistory(distance_sale_id=distance_sale_id)
        db.session.add(new_distance_sale_history)
        db.session.commit()

        return new_distance_sale_history
