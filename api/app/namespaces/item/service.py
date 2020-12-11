import os
from datetime import date, timedelta, datetime
from typing import List, BinaryIO, Dict
import pandas as pd

from flask import g, current_app
from werkzeug.exceptions import NotFound, UnsupportedMediaType, UnprocessableEntity, ExpectationFailed
from app.extensions import (
    db,
    socket_io)

from . import Item, ItemHistory
from .schema import ItemSubSchema
from .interface import ItemInterface

from app.namespaces.utils.service import InputService, NotificationService, TemplateService, HistoryService
from app.namespaces.transaction_input import TransactionInput
from app.namespaces.tag.service import TagService

from app.extensions.socketio.emitters import SocketService



class ItemService:
    @staticmethod
    def get_all() -> List[Item]:
        return Item.query.all()

    @staticmethod
    def get_all_by_seller_firm_id(seller_firm_id: int) -> List[Item]:
        return Item.query.filter_by(seller_firm_id = seller_firm_id).all()


    @staticmethod
    def get_by_id(item_id: int) -> Item:
        return Item.query.filter_by(id = item_id).first()

    @staticmethod
    def get_by_public_id(item_public_id: str) -> Item:
        return Item.query.filter_by(public_id = item_public_id).first()

    @staticmethod
    def get_by_identifiers_seller_firm_id(item_sku: str, item_asin: str, seller_firm_id: int) -> Item:
        if isinstance(item_sku, str):
            item = ItemService.get_by_sku_seller_firm_id(item_sku, seller_firm_id)
        else:
            item = ItemService.get_by_asin_seller_firm_id(item_asin, seller_firm_id)
        return item

    @staticmethod
    def get_by_sku_seller_firm_id(item_sku: str, seller_firm_id: int) -> Item:
        return Item.query.filter(
            Item.sku==item_sku,
            Item.seller_firm_id==seller_firm_id
            ).first()

    @staticmethod
    def get_by_asin_seller_firm_id(item_asin: str, seller_firm_id: int) -> Item:
        return Item.query.filter(
            Item.sku == item_asin,
            Item.seller_firm_id == seller_firm_id
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
        if isinstance(item, Item):
            item.update(data_changes)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise

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
                'message': 'Item (id: {}) has been successfully deleted.'.format(item_id)
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
                'message': 'Item (id: {}) has been successfully deleted.'.format(item_public_id)
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
        from app.namespaces.business.seller_firm.service import SellerFirmService

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if seller_firm:
            item_data['seller_firm_id'] = seller_firm.id
            item = ItemService.get_by_sku_seller_firm_id(item_data['sku'], item_data['seller_firm_id'])
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
    def get_unit_cost_price_net_est(
            seller_firm_id: int,
            df_transaction_inputs: pd.DataFrame = None,
            platform_code: str = None
        ) -> float:

        """
        There are the following options for estimating the item unit cost prices prioritized in the order as followed:
        1. Average of unit cost prices of other items
            if len(item_unit_cost_prices) > 5:
                Average of total value amt / qty in transaction reports
        2. If

        """

        items_raw = ItemService.get_all_by_seller_firm_id(seller_firm_id)
        item_unit_cost_prices = [item.unit_cost_price_net for item in items_raw if item.unit_cost_price_net is not None]
        if items_raw is not None and len(item_unit_cost_prices) > 5:
            unit_cost_price_net_est = sum(item_unit_cost_prices) / len(item_unit_cost_prices) #avg item_unit_cost_prices

        elif df_transaction_inputs is not None and platform_code is not None:
            from app.namespaces.transaction_input.service import TransactionInputVariableService
            unit_cost_price_net_est = TransactionInputVariableService.get_item_unit_cost_price_est_from_transaction_inputs(df_transaction_inputs, platform_code)




        else:
            unit_cost_price_net_est = None



        return unit_cost_price_net_est



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
                reference_value='{}kg'.format(round(transaction_input.item_weight_kg, 3)),
                calculated_value='{}kg'.format(round(item.weight_kg, 3)),
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
        InputService.move_file_to_out(file_path_in, basepath, file_type, business_id=seller_firm_id)

        return response_object

    @staticmethod
    def get_df_vars(df: pd.DataFrame, i: int, current: int, object_type: str, seller_firm_id: int) -> List:
        try:
            sku = InputService.get_str_or_None(df, i, column='SKU')
        except:
            raise UnprocessableEntity('SKU')

        if not sku or sku == '':
            message = 'No SKU was provided for at least one of the items (row {}). In order to avoid processing errors, please make sure to add SKUs for all items before uploading any transaction file.'.format(current+1)
            SocketService.emit_status_info(object_type, message)

        try:
            name = InputService.get_str_or_None(df, i, column='name')
        except:
            raise UnprocessableEntity('name')

        try:
            asin = InputService.get_str_or_None(df, i, column='asin')
        except:
            raise UnprocessableEntity('asin')

        try:
            unit_cost_price_net = InputService.get_float_or_None(df, i, column='unit_cost_price_net')
        except:
            raise UnprocessableEntity('unit_cost_price_net')

        try:
            unit_cost_price_currency_code = InputService.get_str_or_None(df, i, column='unit_cost_price_currency_code')
        except:
            raise UnprocessableEntity('unit_cost_price_currency_code')


        try:
            brand_name = InputService.get_str_or_None(df, i, column='brand_name')
        except:
            raise UnprocessableEntity('brand_name')

        try:
            weight_kg = InputService.get_float_or_None(df, i, column='weight_kg')
        except:
            raise UnprocessableEntity('weight_kg')

        try:
            tax_code_code = InputService.get_str_or_None(df, i, column='tax_code')
        except:
            raise UnprocessableEntity('tax_code')


        return (
            sku,
            name,
            asin,
            unit_cost_price_net,
            unit_cost_price_currency_code,
            brand_name,
            weight_kg,
            tax_code_code
        )





    @staticmethod
    def create_items(df: pd.DataFrame, file_path_in: str, user_id: int, seller_firm_id: int) -> List[Dict]:

        total = total_number_items = len(df.index)
        original_filename = os.path.basename(file_path_in)[:128]
        object_type = object_type_human_read = 'item'
        duplicate_list = []
        duplicate_counter = 0


        if not seller_firm_id:
            SocketService.emit_status_error_no_seller_firm(object_type)
            return False

        # send status update via socket
        SocketService.emit_status_success(0, total, original_filename, object_type)

        unit_cost_price_net_est = ItemService.get_unit_cost_price_net_est(seller_firm_id)

        for i in range(total_number_items):
            current = i + 1

            try:
                sku, name, asin, unit_cost_price_net, unit_cost_price_currency_code, brand_name, weight_kg, tax_code_code = ItemService.get_df_vars(df, i, current, object_type, seller_firm_id)
            except Exception as e:
                if e.code == 422:
                    SocketService.emit_status_error_column_read(current, object_type, column_name=e.description)
                if e.code == 417:
                    SocketService.emit_status_error_invalid_value(object_type, e.description)
                return False

            item = ItemService.get_by_identifiers_seller_firm_id(sku, asin, seller_firm_id)
            try:
                valid_from = TemplateService.get_valid_from(df, i, item, Item)
            except:
                raise UnprocessableEntity('valid_from')


            item_data = {
                'valid_from': valid_from,
                'created_by': user_id,
                'original_filename': original_filename,
                'sku': sku,
                'asin': asin,
                'seller_firm_id': seller_firm_id,
                'brand_name': brand_name,
                'name': name,
                'weight_kg': weight_kg,
                'tax_code_code': tax_code_code,
                'unit_cost_price_currency_code': unit_cost_price_currency_code,
                'unit_cost_price_net': unit_cost_price_net,
                'unit_cost_price_net_est': unit_cost_price_net_est
            }



            # handling item updates
            if isinstance(item, Item):

                item_history = ItemHistoryService.get_by_relationship_date(item.id, valid_from)
                if isinstance(item_history, ItemHistory):

                    # handling exact duplicates of relevant state
                    if (
                        item_history.valid_from == valid_from
                        and item_history.sku == sku
                        and item_history.asin == asin
                        and item_history.seller_firm_id == seller_firm_id
                        and item_history.brand_name == brand_name
                        and item_history.name == name
                        and item_history.weight_kg == weight_kg
                        and item_history.tax_code_code == tax_code_code
                        and item_history.unit_cost_price_currency_code == unit_cost_price_currency_code
                        and item_history.unit_cost_price_net == unit_cost_price_net
                        ):
                        if not duplicate_counter > 2:
                            message = 'An item with the given sku "{}" already exists. Registration has been skipped consequently.'.format(sku)
                            SocketService.emit_status_info(object_type, message)

                        total -= 1
                        duplicate_list.append(sku)
                        duplicate_counter += 1
                        continue


                    # updating item
                    else:
                        try:
                            item.update(data_changes=item_data)
                            db.session.commit()
                            continue

                        except:
                            db.session.rollback()
                            message = 'Error at {} with sku "{}" (file: {}). Please recheck.'.format(object_type_human_read, sku, original_filename)
                            SocketService.emit_status_error(object_type, message)
                            return False


            # handling new item
            else:
                try:
                    new_item = ItemService.create(item_data)
                except:
                    db.session.rollback()
                    message = 'Error at {} with sku "{}" (file: {}). Please recheck.'.format(object_type_human_read, sku, original_filename)
                    SocketService.emit_status_error(object_type, message)
                    return False

                # send status update via socket
                SocketService.emit_status_success(current, total, original_filename, object_type)

        # following the succesful processing, the vuex store is being reset
        # first cleared
        SocketService.emit_clear_objects(object_type)
        # then refilled
        ItemService.push_all_by_seller_firm_id(seller_firm_id, object_type)

        # send final status via socket
        SocketService.emit_status_final(total, original_filename, object_type, object_type_human_read, duplicate_list=duplicate_list)

        return True


    # List all files in a directory using scandir(): Returns an iterator of all the objects in a directory including file attribute information

    @staticmethod
    def push_all_by_seller_firm_id(seller_firm_id: int, object_type: str) -> None:
        socket_list = []
        items = ItemService.get_all_by_seller_firm_id(seller_firm_id)
        for item in items:
            # push new distance sale to vuex via socket
            item_schema_sub = ItemSubSchema.get_item_sub(item)

            if len(items) < 10:
                SocketService.emit_new_object(item_schema_sub, object_type)
            else:
                socket_list.append(item_schema_sub)

        if len(socket_list) > 0:
            SocketService.emit_new_objects(socket_list, object_type)


    @staticmethod
    def create(item_data: ItemInterface) -> Item:
        new_item = Item(
            created_by = item_data.get('created_by'),
            active = item_data.get('active'),
            category_id = item_data.get('category_id'),
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
            unit_cost_price_net = item_data.get('unit_cost_price_net'),
            unit_cost_price_net_est = item_data.get('unit_cost_price_net_est')
        )

        db.session.add(new_item)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        item_data['item_id'] = new_item.id
        item_data['tax_code_code'] = new_item.tax_code_code
        item_data['unit_cost_price_currency_code'] = new_item.unit_cost_price_currency_code
        try:
            ItemHistoryService.create(item_data)
        except Exception as e:
            db.session.rollback()
            raise

        return new_item




class ItemHistoryService:


    @staticmethod
    def get_oldest(item_id: int) -> ItemHistory:
        return ItemHistory.query.filter_by(item_id=item_id).order_by(ItemHistory.valid_from.asc()).first()

    @staticmethod
    def get_current(item_id: int) -> ItemHistory:
        return ItemHistory.query.filter_by(item_id=item_id).order_by(ItemHistory.valid_from.desc()).first()

    @staticmethod
    def get_by_relationship_date(item_id: int, date: date):
        return ItemHistory.query.filter(
            ItemHistory.item_id == item_id,
            ItemHistory.valid_from <= date,
            ItemHistory.valid_to >= date
            ).first()

    @staticmethod
    def create(item_data) -> ItemHistory:

        # create new item history
        new_item_history = ItemHistory(
            valid_from=item_data.get('valid_from'),
            valid_to=item_data.get('valid_to'),
            item_id=item_data.get('item_id'),

            created_by = item_data.get('created_by'),
            active = item_data.get('active'),
            category_id = item_data.get('category_id'),
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
            unit_cost_price_net = item_data.get('unit_cost_price_net'),
        )

        db.session.add(new_item_history)
        db.session.commit()

        return new_item_history

    @staticmethod
    def create_empty(item_id: int) -> ItemHistory:
        # create new item history
        new_item_history = ItemHistory(item_id=item_id)
        db.session.add(new_item_history)
        db.session.commit()

        return new_item_history












    # @staticmethod
    # def select_date_from_transaction_report(shipment_date: date, arrival_date: date, complete_date: date) -> date:
    #     if isinstance(shipment_date, date):
    #         item_date = shipment_date
    #     elif isinstance(arrival_date, date):
    #         item_date = arrival_date
    #     else:
    #         item_date = complete_date
    #     return item_date
