import os
from datetime import date, timedelta

from .model import Item

from !!! import Account
from werkzeug.exceptions import NotFound, UnsupportedMediaType

from ..utils.service import InputService
from flask import current_app

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
    def process_item_lists_upload(item_list_files: list, **kwargs):
        seller_firm_id_list = InputService.get_seller_firm_id_list(files=seller_firm_information_files, **kwargs)
        file_type='item_list'
        file_path_in_list = InputService.store_static_data_upload(files=seller_firm_information_files, seller_firm_id_list=seller_firm_id_list, file_type=file_type)

        create_function = ItemService.process_item_from_df_file_path

        flat_response_objects = InputService.create_static_data_inputs(file_path_in_list, seller_firm_id_list, create_function)

        InputService.move_static_files(file_path_in_list, file_type)

        return flat_response_objects




    @staticmethod
    def read_item_list_upload_into_df(file_path: str, encoding: str) -> df:
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            try:
                if file_name.lower().endswith('.csv'):
                    df = pd.read_csv(file_path, encoding=encoding)
                else:
                    raise UnsupportedMediaType(
                        'File extension invalid (file: {}).'.format(file_name))
                return df
            except:
                raise UnsupportedMediaType(
                    'Cannot read file {}.'.format(file_name))

        else:
            raise #!!! (not a file)



    @staticmethod
    def process_item_from_df_file_path(file_path: str, seller_firm_id: int):
        df = InputService.read_file_path_into_df((file_path, encoding=None)

        redundancy_counter = 0
        error_counter = 0
        total_number_items = len(df.index)
        input_type = 'item'

        for i in range(total_number_items):

            sku = InputService.get_str(df, i, column='sku')

            valid_from = InputService.get_date_or_None(df, i, column='valid_from')
            valid_to = InputService.get_date_or_None(df, i, column='valid_to')

            if sku and seller_firm_id:
                if not valid_from:
                    valid_from = date.today()
                if not valid_to:
                    valid_to = valid_from + timedelta(days=TAX_DEFAULT_VALIDITY)

                try:
                    redundancy_counter += ItemService.handle_redundancy(sku, seller_firm_id, valid_from)
                    new_item = ItemService.create_item(df, i, sku, seller_firm_id, valid_from, valid_to)


                except:
                    db.session.rollback()

                    error_counter += 1

            else:
                error_counter += 1


        response_objects = InputService.create_input_response_objects(file_path, input_type, total_number_items, error_counter, redundancy_counter=redundancy_counter)

        return response_objects


# List all files in a directory using scandir(): Returns an iterator of all the objects in a directory including file attribute information


    @staticmethod
    def create_item(df, i, sku: str, seller_firm_id, valid_from: date, valid_to: date) -> dict:
        new_item = Item(
            sku = sku,
            seller_firm_id = seller_firm_id,
            valid_from = valid_from,
            valid_to = valid_to,
            brand_name = InputService.get_str_or_None(df, i, column='brand_name'),
            name=InputService.get_str_or_None(df, i, column='name'),
            ean=InputService.get_str_or_None(df, i, column='ean'),
            asin=InputService.get_str_or_None(df, i, column='asin'),
            fnsku=InputService.get_str_or_None(df, i, column='fnsku'),
            weight_kg = InputService.get_float(df, i, column='weight_kg'),
            tax_code_code =InputService.get_str_or_None(df, i, column='tax_code_code'),
            unit_cost_price_currency_code =InputService.get_str_or_None(df, i, column='unit_cost_price_currency_code'),
            unit_cost_price_net =InputService.get_float(df, i, column='unit_cost_price_net')
        )

        db.session.add(new_item)
        db.session.commit()

        return new_item


    @staticmethod
    def handle_redundancy(sku: str, seller_firm_id: int, valid_from: date) -> int:
        item: Item = Item.query.filter(Item.sku == sku, Item.seller_firm_id == seller_firm_id, Item.valid_to >= valid_from).first()

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
