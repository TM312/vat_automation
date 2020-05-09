from os import scandir, path
from datetime import date, timedelta

from .model import Item

from !!! import Account
from werkzeug.exceptions import NotFound

from ..utils.service import InputService
from flask import current_app

TAX_DEFAULT_VALIDITY = current_app.config["TAX_DEFAULT_VALIDITY"]
BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config["BASE_PATH_STATIC_DATA_SELLER_FIRM"]
ITEM_DATA_ALLOWED_EXTENSIONS = current_app.config["ITEM_DATA_ALLOWED_EXTENSIONS"]


class ItemService:

    @staticmethod
    def get_by_sku_account_date(item_sku: str, account: Account, date: date) -> Item:
        if account.channel.platform_name == 'amazon':
            item = Item.query.filter(Item.sku==item_sku, Item.seller_firm_id=account.seller_firm_id, Item.valid_from<=date, Item.valid_to>=date).first()
            if item:
                return item
            else:
                raise NotFound('The item specific SKU "{}" is not listed in the item information of the seller. Please update the item information before proceeding'.format(item_sku))


    @staticmethod
    def process_item_lists_upload(item_list_files: list, seller_firm_id_list: list):
        file_path_list = []
        for i, item_list_file in enumerate(item_list_files):
            seller_firm_id = seller_firm_id_list[i]
            try:
                file_path = ItemService.store_item_list_file(item_list_file, seller_firm_id)
                file_path_list.append(file_path)

            except:
                raise
                !!! log??

        ItemService.create_item_inputs(file_path_list, seller_firm_id)


        return flat_response_objects



    @staticmethod
    def store_item_list_file(item_list_file, seller_firm_id: int):
        file_path = InputService.store_file(file=item_list_file, allowed_extensions=ITEM_DATA_ALLOWED_EXTENSIONS, basepath=BASE_PATH_STATIC_DATA_SELLER_FIRM, file_type='item_list', owner_id=seller_firm_id)
        return file_path


    def create_item_inputs(file_path_list: list, seller_firm_id_list: list):
        if (file_path_list and seller_firm_id_list):
            response_objects_cum = []
            for i, file_path in enumerate(file_path_list):
                seller_firm_id = seller_firm_id_list[i]
                try:
                    response_objects = ItemService.create_item_input(file_path, seller_firm_id)

                    response_objects_cum.append(response_objects)

            # flatten list of response_object lists (i.e. response_objects)
            flat_response_objects = [response_object for response_objects in response_objects_cum for response_object in response_objects]

        else:
            raise



basepath_in = path.join(BASE_PATH_STATIC_DATA_SELLER_FIRM, 'item_list', 'in')
with scandir(basepath_in) as entries:
    for entry in entries:
        if entry.is_file():
            print(entry.name)

    def read_item_list_upload_into_df(file):
        try:
            if file.is_file() and file.lower().endswith('.csv'):
                df = pd.read_csv(file, encoding='latin-1')
            else:
                raise UnsupportedMediaType(
                    'File extension invalid (file: {}).'.format(file.name))
            return df
        except:
            if file.is_file():
                raise UnsupportedMediaType(
                    'Cannot read file {}.'.format(file.names))
            else:
                raise UnsupportedMediaType('Cannot read file.')










    @staticmethod
    def create_item_input(file_path: str, seller_firm_id: int):
        df = ItemService.read_item_list_upload_into_df(file_path)

        redundancy_counter = 0
        error_counter = 0
        total_number_items = len(df.index)

        for i in range(total_number_items):

            sku = InputService.get_str(df, i, column='sku'),
            seller_firm_id = seller_firm_id,

            valid_from = InputService.get_date_or_None(df, i, column='valid_from')
            valid_to = InputService.get_date_or_None(df, i, column='valid_from')

            if sku and seller_firm_id:
                if not valid_from:
                    valid_from = date.today()
                if not valid_to:
                    valid_to = valid_from + timedelta(days=TAX_DEFAULT_VALIDITY)

                try:
                    new_item = ItemService.create_item(df, sku, seller_firm_id, valid_from, valid_to)
                    db.session.add(new_item)
                    db.session.commit()

                except:
                    db.session.rollback()

                    error_counter += 1

            else:
                redundancy_counter += 1


        #response_objects = TransactionInputService.create_input_response_objects(file_path, total_number_transactions, error_counter, redundancy_counter)

        return response_objects


# List all files in a directory using scandir(): Returns an iterator of all the objects in a directory including file attribute information



    def create_item(df, sku: str, seller_firm_id, valid_from: date, valid_to: date) -> Item:
        item = Item.query.filter(Item.sku == sku, Item.seller_firm_id=seller_firm_id, Item.valid_from <= date, Item.valid_to >= date).first()

        if not item:
            new_item = Item(
                sku = sku,
                seller_firm_id = seller_firm_id,
                valid_from = valid_from,
                valid_to = valid_to
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

        response_object = {
            'status':'success',
            'message': '{} (validity: {}-{}) has been added to the database.'.format(sku, str(valid_from), str(valid_to))
        }
