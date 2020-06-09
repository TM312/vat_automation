import os
from datetime import date, timedelta
from typing import List, BinaryIO
import pandas as pd

from flask import g, current_app
from werkzeug.exceptions import NotFound, UnsupportedMediaType
from app.extensions import db

from . import Item
from .interface import ItemInterface

from ..account import Account
from ..utils.service import InputService, NotificationService
from ..utils.schema import response_object_dto
from ..transaction_input import TransactionInput



class ItemService:
    @staticmethod
    def get_all() -> List[Item]:
        items = Item.query.all()
        return items

    @staticmethod
    def get_by_id(item_id: int) -> Item:
        return Item.query.filter(Item.id == item_id).first()


    @staticmethod
    def update(item_id: int, data_changes: ItemInterface) -> Item:
        item = ItemService.get_by_id(item_id)
        item.update(data_changes)
        db.session.commit()
        return item

    @staticmethod
    def delete_by_id(item_id: str):
        item = Item.query.filter(Item.id == item_id).first()
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
    def get_by_sku_account_date(item_sku: str, account: Account, date: date) -> Item:
        if account.channel.platform_code == 'AMZ':
            item = Item.query.filter(Item.sku==item_sku, Item.seller_firm_id==account.seller_firm_id, Item.valid_from<=date, Item.valid_to>=date).first()
            if item:
                return item
            else:
                raise NotFound('The item specific SKU "{}" is not listed in the item information of the seller. Please update the item information before proceeding'.format(item_sku))


    @staticmethod
    def compare_calculation_reference(transaction_input: TransactionInput, item: Item):
        notification_data_list = []
        if item.name and transaction_input.item_name and item.name != transaction_input.item_name:
            notification_data = NotificationService.create_notification_data(main_subject='Item Name', original_filename=transaction_input.original_filename, status='info', reference_value=transaction_input.item_name, calculated_value=item.name, transaction_input_id=transaction_input.id)
            notification_data_list.append(notification_data)

        if item.weight_kg and transaction_input.item_weight_kg and item.weight_kg != transaction_input.item_weight_kg:
            notification_data = NotificationService.create_notification_data(main_subject='Item Weight', original_filename=transaction_input.original_filename, status='info', reference_value=transaction_input.item_weight_kg, calculated_value=item.weight_kg, transaction_input_id=transaction_input.id)
            notification_data_list.append(notification_data)


        if item.asin and transaction_input.asin and item.asin != transaction_input.asin:
            notification_data = NotificationService.create_notification_data(main_subject='ASIN', original_filename=transaction_input.original_filename, status='info', reference_value=transaction_input.asin, calculated_value=item.asin, transaction_input_id=transaction_input.id)
            notification_data_list.append(notification_data)

        try:
            for notification_data in notification_data_list:
                NotificationService.create_transaction_notification(notification_data)

        except:
            raise






    @staticmethod
    #kwargs can contain: seller_firm_public_id
    def process_item_files_upload(item_information_files: List[BinaryIO], **kwargs) -> response_object_dto:
        BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config["BASE_PATH_STATIC_DATA_SELLER_FIRM"]

        file_type='item_list'
        df_encoding = 'utf-8'
        delimiter = None
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM
        user_id = g.user.id

        for file in item_information_files:
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            ItemService.process_item_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, **kwargs)

        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(item_information_files)))
        }

        return response_object



    # celery task !!
    @staticmethod
    def process_item_information_file(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, **kwargs) -> List[response_object_dto]:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_objects = ItemService.create_items(df, file_path_in, user_id, **kwargs)

        # celery task !!
        InputService.move_file_to_out(file_path_in, file_type)

        return response_objects




    @staticmethod
    def create_items(df: pd.DataFrame, file_path_in: str, user_id: int, **kwargs) -> List[response_object_dto]:
        from ..business.seller_firm.service import SellerFirmService

        TAX_DEFAULT_VALIDITY = current_app.config["TAX_DEFAULT_VALIDITY"]


        redundancy_counter = 0
        error_counter = 0
        total_number_items = len(df.index)
        input_type = 'item' # only used for response objects

        for i in range(total_number_items):

            sku = InputService.get_str(df, i, column='sku')
            seller_firm_id = SellerFirmService.get_seller_firm_id(df=df, i=i, **kwargs)

            valid_from = InputService.get_date_or_None(df, i, column='valid_from')
            valid_to = InputService.get_date_or_None(df, i, column='valid_to')

            if sku and seller_firm_id:
                if not valid_from:
                    valid_from = date.today()
                if not valid_to:
                    valid_to = valid_from + timedelta(days=TAX_DEFAULT_VALIDITY)

                redundancy_counter += ItemService.handle_redundancy(sku, seller_firm_id, valid_from)
                item_data = {
                    'created_by': user_id,
                    'original_filename': os.path.basename(file_path_in),
                    'sku': sku,
                    'seller_firm_id' : seller_firm_id,
                    'valid_from' : valid_from,
                    'valid_to' : valid_to,
                    'brand_name' : InputService.get_str_or_None(df, i, column='brand_name'),
                    'name' : InputService.get_str_or_None(df, i, column='name'),
                    'ean' : InputService.get_str_or_None(df, i, column='ean'),
                    'asin' : InputService.get_str_or_None(df, i, column='asin'),
                    'fnsku' : InputService.get_str_or_None(df, i, column='fnsku'),
                    'weight_kg' : InputService.get_float(df, i, column='weight_kg'),
                    'tax_code_code' :InputService.get_str_or_None(df, i, column='tax_code_code'),
                    'unit_cost_price_currency_code' :InputService.get_str_or_None(df, i, column='unit_cost_price_currency_code'),
                    'unit_cost_price_net' :InputService.get_float(df, i, column='unit_cost_price_net')
                }

                try:
                    new_item = ItemService.create(item_data)

                except:
                    db.session.rollback()

                    error_counter += 1

            else:
                error_counter += 1


        response_objects = InputService.create_input_response_objects(file_path, input_type, total_number_items, error_counter, redundancy_counter=redundancy_counter)

        return response_objects


# List all files in a directory using scandir(): Returns an iterator of all the objects in a directory including file attribute information


    @staticmethod
    def create(item_data: ItemInterface) -> Item:
        new_item = Item(
            created_by = item_data.get('created_by'),
            original_filename = item_data.get('original_filename'),
            sku = item_data.get('sku'),
            seller_firm_id = item_data.get('seller_firm_id'),
            valid_from = item_data.get('valid_from'),
            valid_to = item_data.get('valid_to'),
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

        return new_item


    @staticmethod
    def handle_redundancy(sku: str, seller_firm_id: int, valid_from: date) -> int:
        item: Item = Item.query.filter(Item.sku == sku, Item.seller_firm_id == seller_firm_id, Item.valid_to >= valid_from).first()

        # if an item with the same sku for the specified validity period already exists, it is being updated or deleted.
        if item:
            if item.valid_from >= valid_from:
                db.session.delete(item)

            else:
                data_changes = {
                    'valid_to': valid_from - timedelta(days=1)
                }
                item.update(data_changes)
                redundancy_counter = 1
        else:
            redundancy_counter = 0

        return redundancy_counter
