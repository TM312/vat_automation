import os
from datetime import date, timedelta, datetime
from typing import List, BinaryIO, Dict
import pandas as pd

from flask import g, current_app
from werkzeug.exceptions import NotFound, UnsupportedMediaType
from app.extensions import (
    db,
    socket_io)

from . import Item, ItemHistory
from .schema import ItemSubSchema
from .interface import ItemInterface

from ..account import Account
from ..utils.service import InputService, NotificationService
from ..transaction_input import TransactionInput
from ..tag.service import TagService

from app.extensions.socketio.emitters import SocketService



class ItemService:
    @staticmethod
    def get_all() -> List[Item]:
        items = Item.query.all()
        return items

    @staticmethod
    def get_by_id(item_id: int) -> Item:
        return Item.query.filter_by(id = item_id).first()

    @staticmethod
    def get_by_public_id(item_public_id: str) -> Item:
        return Item.query.filter_by(public_id = item_public_id).first()

    @staticmethod
    def get_by_sku_account(item_sku: str, account: Account) -> Item:
        return Item.query.filter(
            Item.sku==item_sku,
            Item.seller_firm_id==account.seller_firm_id
            ).first()

    @staticmethod
    def get_by_sku_seller_firm_id(sku: str, seller_firm_id: int) -> Item:
        return Item.query.filter(
            Item.sku == sku,
            Item.seller_firm_id == seller_firm_id
            ).first()


    @staticmethod
    def update(item_id: int, data_changes: ItemInterface) -> Item:
        item = ItemService.get_by_id(item_id)
        item.update(data_changes)
        db.session.commit()
        return item

    @staticmethod
    def update_by_public_id(item_public_id: str, data_changes: ItemInterface) -> Item:
        item = ItemService.get_by_public_id(item_public_id)
        if item:
            item.update(data_changes)
            db.session.commit()
            return item

    @staticmethod
    def delete_by_id(item_id: int):
        item = ItemService.get_by_id(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Item (code: {}) has been successfully deleted.'.format(item_id)
            }
            return response_object
        else:
            raise NotFound('This item does not exist.')

    @staticmethod
    def delete_by_public_id(item_public_id: str):
        item = ItemService.get_by_public_id(item_public_id)
        if item:
            db.session.delete(item)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Item (code: {}) has been successfully deleted.'.format(item_public_id)
            }
            return response_object
        else:
            raise NotFound('This item does not exist.')



    @staticmethod
    def process_single_submit(seller_firm_public_id: str, item_data: ItemInterface):

        item_data['created_by'] = g.user.id
        try:
            item_data['weight_kg'] = float(item_data['weight_kg'])
            item_data['unit_cost_price_net'] = float(item_data['unit_cost_price_net'])

        except:
            raise

        item = ItemService.create_by_seller_firm_public_id(seller_firm_public_id, item_data)

        return item

    @staticmethod
    def create_by_seller_firm_public_id(seller_firm_public_id: str, item_data: ItemInterface) -> Item:
        from ..business.seller_firm.service import SellerFirmService

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if seller_firm:
            item_data['seller_firm_id'] = seller_firm.id
            item = ItemService.get_by_sku_account(item_data['sku'], item_data['seller_firm_id'])
            if isinstance(item, Item):
                return item
            else:
                try:
                    new_item = ItemService.create(item_data)
                except:
                    db.session.rollback()
                    raise

        return new_item





    @staticmethod
    def compare_calculation_reference(transaction_id: int, transaction_input: TransactionInput, item: Item):
        notification_data_list = []
        if item.name and transaction_input.item_name and item.name != transaction_input.item_name:
            notification_data = NotificationService.create_transaction_notification_data(
                main_subject='Item Name',
                original_filename=transaction_input.original_filename,
                status='info',
                reference_value=transaction_input.item_name,
                calculated_value=item.name,
                transaction_id=transaction_id)
            notification_data_list.append(notification_data)

        if item.weight_kg and transaction_input.item_weight_kg and item.weight_kg != transaction_input.item_weight_kg:
            notification_data = NotificationService.create_transaction_notification_data(
                main_subject='Item Weight',
                original_filename=transaction_input.original_filename,
                status='info',
                reference_value='{}kg'.format(transaction_input.item_weight_kg),
                calculated_value='{}kg'.format(item.weight_kg),
                transaction_id=transaction_id)
            notification_data_list.append(notification_data)


        if item.asin and transaction_input.asin and item.asin != transaction_input.asin:
            notification_data = NotificationService.create_transaction_notification_data(
                main_subject='ASIN',
                original_filename=transaction_input.original_filename,
                status='info',
                reference_value=transaction_input.asin,
                calculated_value=item.asin,
                transaction_id=transaction_id)
            notification_data_list.append(notification_data)

        try:
            for notification_data in notification_data_list:
                NotificationService.create_transaction_notification(notification_data)

        except:
            raise






    @staticmethod
    def handle_item_data_upload(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: Dict) -> Dict:
        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_object = ItemService.create_items(df, file_path_in, user_id, seller_firm_id)
        tag = TagService.get_by_code('ITEM')
        NotificationService.handle_seller_firm_notification_data_upload(seller_firm_id, user_id, tag, seller_firm_notification_data)
        InputService.move_file_to_out(file_path_in, basepath, file_type)

        return response_object

    @staticmethod
    def get_df_vars(df: pd.DataFrame, i: int, current: int, object_type: str) -> List:
        try:
            sku = InputService.get_str(df, i, column='SKU')
        except:
            SocketService.emit_status_error_column_read(current, object_type, column_name='SKU')
            return False

        if not sku or sku == '':
            message = 'No SKU was provided for at least one of the items (row {}). In order to avoid processing errors, please make sure to add SKUs for all items before uploading any transaction file.'.format(current)
            SocketService.emit_status_info(object_type, message)
            return False

        try:
            name = InputService.get_str_or_None(df, i, column='name')
        except:
            SocketService.emit_status_error_column_read(current, object_type, column_name='name')
            return False

        try:
            unit_cost_price_net = InputService.get_float(df, i, column='unit_cost_price_net')
        except:
            SocketService.emit_status_error_column_read(current, object_type, column_name='unit_cost_price_net')
            return False

        try:
            unit_cost_price_currency_code = InputService.get_str_or_None(df, i, column='unit_cost_price_currency_code')
        except:
            SocketService.emit_status_error_column_read(current, object_type, column_name='unit_cost_price_currency_code')
            return False

        try:
            service_start_date = current_app.config.SERVICE_START_DATE
            valid_from = InputService.get_date_or_None(df, i, column='valid_from')
            if isinstance(valid_from, date):
                valid_from = valid_from if valid_from >= service_start_date else service_start_date
            else:
                valid_from = date.today()

        except:
            # send error status via socket
            SocketService.emit_status_error_column_read(current, object_type, column_name='valid_from')
            return False

        try:
            brand_name = InputService.get_str_or_None(df, i, column='brand_name')
        except:
            SocketService.emit_status_error_column_read(current, object_type, column_name='brand_name')
            return False

        try:
            weight_kg = InputService.get_str_or_None(df, i, column='weight_kg')
        except:
            SocketService.emit_status_error_column_read(current, object_type, column_name='weight_kg')
            return False

        try:
            tax_code_code = InputService.get_str_or_None(df, i, column='tax_code')
        except:
            SocketService.emit_status_error_column_read(current, object_type, column_name='tax_code')
            return False

        return sku, name, unit_cost_price_net, unit_cost_price_currency_code, valid_from, brand_name, weight_kg, tax_code_code





    @staticmethod
    def create_items(df: pd.DataFrame, file_path_in: str, user_id: int, seller_firm_id: int) -> List[Dict]:

        total = total_number_items = len(df.index)
        original_filename = os.path.basename(file_path_in)[:128]
        object_type = object_type_human_read = 'item'
        item_socket_list = []
        duplicate_list = []
        duplicate_counter = 0
        sku_list = []



        if not seller_firm_id:
            SocketService.emit_status_error_no_seller_firm(object_type)
            return False

        for i in range(total_number_items):
            current = i + 1

            sku, name, unit_cost_price_net, unit_cost_price_currency_code, valid_from, brand_name, weight_kg, tax_code_code = ItemService.get_df_vars(df, i, current, object_type)

            item = ItemService.get_by_sku_seller_firm_id(sku, seller_firm_id)
            if isinstance(item, Item):
                if item.name == name and item.unit_cost_price_net == unit_cost_price_net:
                    if item.brand_name != brand_name or item.weight_kg != weight_kg or item.tax_code_code != tax_code_code:
                        data_changes = {
                            'brand_name': brand_name,
                            'weight_kg': weight_kg,
                            'tax_code_code': tax_code_code
                        }
                        try:
                            item.update(data_changes)

                        except:
                            db.session.rollback()
                            message = 'Error at updating {} with sku "{}" (file: {}). Please recheck.'.format(object_type_human_read, sku, original_filename)
                            SocketService.emit_status_error(object_type, message)
                            return False

                    else:
                        if not duplicate_counter > 2:
                            message = 'An item with the given sku "{}" already exists. Registration has been skipped consequently.'.format(sku)
                            SocketService.emit_status_info(object_type, message)

                        total -= 1
                        duplicate_list.append(sku)
                        duplicate_counter += 1
                        continue

                else:
                    item_history = ItemHistoryService.get_by_item_id_date(item.id, valid_from)
                    data_changes = {
                        'name': name,
                        'unit_cost_price_net': unit_cost_price_net,
                        'unit_cost_price_currency_code': unit_cost_price_currency_code
                    }

                    try:
                        if item_history.valid_from != valid_from:
                            item.update(data_changes, valid_from=valid_from)

                        else:
                            item.update(data_changes, valid_from=item_history.valid_from)
                        db.session.commit()

                    except:
                        db.session.rollback()
                        message = 'Error at {} with sku "{}" (file: {}). Please recheck.'.format(object_type_human_read, sku, original_filename)
                        SocketService.emit_status_error(object_type, message)
                        return False


            else:
                if sku not in sku_list:
                    sku_list.append(sku)

                item_data = {
                    'created_by': user_id,
                    'original_filename': original_filename,
                    'sku': sku,
                    'seller_firm_id': seller_firm_id,
                    'brand_name': brand_name,
                    'name': name,
                    # 'ean': InputService.get_str_or_None(df, i, column='ean'),
                    # 'asin': InputService.get_str_or_None(df, i, column='asin'),
                    # 'fnsku': InputService.get_str_or_None(df, i, column='fnsku'),
                    'weight_kg': weight_kg,
                    'tax_code_code': tax_code_code,
                    'unit_cost_price_currency_code': unit_cost_price_currency_code,
                    'unit_cost_price_net': unit_cost_price_net
                }

                try:
                    new_item = ItemService.create(item_data)

                except:
                    db.session.rollback()

                    # send error status via socket
                    message = 'Error at {} with sku "{}" (file: {}). Please recheck.'.format(object_type_human_read, sku, original_filename)
                    SocketService.emit_status_error(object_type, message)
                    return False

                # send status update via socket
                SocketService.emit_status_success(current, total, original_filename, object_type)


        for sku in sku_list:
            # push new distance sale to vuex via socket
            item = ItemService.get_by_sku_seller_firm_id(sku, seller_firm_id)
            item_schema_sub = ItemSubSchema.get_item_sub(item   )

            if len(sku_list) < 10:
                SocketService.emit_new_object(item_schema_sub, object_type)
            else:
                item_socket_list.append(item_schema_sub)

        if len(item_socket_list) > 0:
            SocketService.emit_new_objects(item_socket_list, object_type)
            item_socket_list = []

        # send final status via socket
        SocketService.emit_status_final(total, original_filename, object_type, object_type_human_read, duplicate_list=duplicate_list)

        return True


    # List all files in a directory using scandir(): Returns an iterator of all the objects in a directory including file attribute information


    @staticmethod
    def create(item_data: ItemInterface) -> Item:
        new_item = Item(
            created_by = item_data.get('created_by'),
            active=item_data.get('active'),
            category_id=item_data.get('category_id'),
            original_filename = item_data.get('original_filename'),
            sku = item_data.get('sku'),
            seller_firm_id = item_data.get('seller_firm_id'),
            brand_name = item_data.get('brand_name'),
            name = item_data.get('name'),
            ean = item_data.get('ean'),
            asin = item_data.get('asin'),
            fnsku = item_data.get('fnsku'),
            weight_kg = item_data.get('weight_kg'),
            tax_code_code = item_data.get('tax_code_code'),
            unit_cost_price_currency_code = item_data.get('unit_cost_price_currency_code'),
            unit_cost_price_net = item_data.get('unit_cost_price_net')
        )

        db.session.add(new_item)
        db.session.commit()

        ItemHistoryService.create(item_data, new_item.id)

        return new_item




class ItemHistoryService:

    @staticmethod
    def get_by_item_id_date(item_id: int, date: date):
        return ItemHistory.query.filter(
            ItemHistory.item_id == item_id,
            ItemHistory.valid_from <= date,
            ItemHistory.valid_to >= date
            ).first()

    @staticmethod
    def create(item_data, item_id):

        # create new item history
        new_item_history = ItemHistory(
            valid_from=item_data.get('valid_from'),
            unit_cost_price_currency_code = item_data.get('unit_cost_price_currency_code'),
            unit_cost_price_net=item_data.get('unit_cost_price_net'),
            name=item_data.get('name'),
            item_id=item_id
        )

        db.session.add(new_item_history)
        db.session.commit()











    # @staticmethod
    # def select_date_from_transaction_report(shipment_date: date, arrival_date: date, complete_date: date) -> date:
    #     if isinstance(shipment_date, date):
    #         item_date = shipment_date
    #     elif isinstance(arrival_date, date):
    #         item_date = arrival_date
    #     else:
    #         item_date = complete_date
    #     return item_date
