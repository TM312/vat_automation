import os
from datetime import date, timedelta

from flask import g, current_app
from werkzeug.exceptions import NotFound, UnsupportedMediaType

from .model import Item

from ..account import Account
from ..utils import InputService

TAX_DEFAULT_VALIDITY = current_app.config["TAX_DEFAULT_VALIDITY"]
BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config["BASE_PATH_STATIC_DATA_SELLER_FIRM"]
STATIC_DATA_ALLOWED_EXTENSIONS = current_app.config["STATIC_DATA_ALLOWED_EXTENSIONS"]


class ItemService:

    @staticmethod
    def get_by_sku_account_date(item_sku: str, account: Account, date: date) -> Item:
        if account.channel.platform_code == 'AMZ':
            item = Item.query.filter(Item.sku==item_sku, Item.seller_firm_id=account.seller_firm_id, Item.valid_from<=date, Item.valid_to>=date).first()
            if item:
                return item
            else:
                raise NotFound('The item specific SKU "{}" is not listed in the item information of the seller. Please update the item information before proceeding'.format(item_sku))




    @staticmethod
    #kwargs can contain: seller_firm_id
    def process_item_files_upload(item_information_files: list, **kwargs):
        file_type='item_list'
        df_encoding = None
        delimiter = None
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM
        user_id = g.user.id

        for file in item_information_files:
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            ItemService.process_item_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id=user_id, **kwargs)

        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(item_information_files)))
        }

        return response_object



    # celery task !!!
    @staticmethod
    def process_item_information_file(file_path_in: str, file_type: str, df_encoding, delimiter, basepath: str, **kwargs) -> list:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_objects = ItemService.create_items(df, file_path_in, **kwargs)

        # celery task !!!
        InputService.move_file_to_out(file_path_in, file_type)

        return response_objects




    @staticmethod
    def create_items(df, file_path_in: int, **kwargs):

        redundancy_counter = 0
        error_counter = 0
        total_number_items = len(df.index)
        input_type = 'item' # only used for response objects

        for i in range(total_number_items):

            sku = InputService.get_str(df, i, column='sku')
            seller_firm_id = InputService.get_seller_firm_id(df, i, **kwargs)

            valid_from = InputService.get_date_or_None(df, i, column='valid_from')
            valid_to = InputService.get_date_or_None(df, i, column='valid_to')

            if sku and seller_firm_id:
                if not valid_from:
                    valid_from = date.today()
                if not valid_to:
                    valid_to = valid_from + timedelta(days=TAX_DEFAULT_VALIDITY)

                redundancy_counter += ItemService.handle_redundancy(sku, seller_firm_id, valid_from)
                item_data = {
                    'created_by': kwargs['user_id'],
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
                    new_item = ItemService.create_item(item_data)

                except:
                    db.session.rollback()

                    error_counter += 1

            else:
                error_counter += 1


        response_objects = InputService.create_input_response_objects(file_path, input_type, total_number_items, error_counter, redundancy_counter=redundancy_counter)

        return response_objects


# List all files in a directory using scandir(): Returns an iterator of all the objects in a directory including file attribute information


    @staticmethod
    def create_item(item_data: dict) -> Item:
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
