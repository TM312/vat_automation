import os
from datetime import datetime
import pandas as pd
from typing import List, BinaryIO
from flask import g, current_app

from .model import TransactionInput
from .interface import TransactionInputInterface

from werkzeug.exceptions import UnsupportedMediaType, NotFound
from app.extensions import db

from ..utils.service import InputService
from ..utils.interface import ResponseObjectInterface
from ..transaction.service import TransactionService




class TransactionInputService:


    @staticmethod
    def get_df_transaction_input_delimiter(file: BinaryIO) -> str:
        if file.lower().endswith('.txt'):
            delimiter='\t'
        elif file.lower().endswith('.txt'):
            delimiter=None
        else:
            filename = os.path.basename(file)
            raise UnsupportedMediaType('File extension invalid (file: {}).'.format(filename))

        return delimiter


    @staticmethod
    #kwargs can contain: seller_firm_public_id
    def process_transaction_input_files_upload(transaction_input_files: List[BinaryIO], **kwargs) -> ResponseObjectInterface:
        BASE_PATH_TRANSACTION_DATA_SELLER_FIRM = current_app.config["BASE_PATH_TRANSACTION_DATA_SELLER_FIRM"]

        file_type='item_list'
        df_encoding = 'utf-8'
        basepath = BASE_PATH_TRANSACTION_DATA_SELLER_FIRM
        user_id = g.user.id

        for file in transaction_input_files:
            delimiter = TransactionInputService.get_df_transaction_input_delimiter(file)
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            TransactionInputService.process_transaction_input_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, **kwargs)


        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(item_information_files)))
        }

        return response_object



    # celery task !!
    @staticmethod
    def process_transaction_input_file(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, **kwargs) -> List[ResponseObjectInterface]:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_objects = TransactionInputService.create_transaction_inputs_and_transactions(df, file_path_in, user_id, **kwargs)


        InputService.move_file_to_out(file_path_in, file_type)

        return response_objects



    @staticmethod
    def create_transaction_inputs_and_transactions(df: pd.DataFrame, file_path_in: str, user_id: int, **kwargs) -> List[ResponseObjectInterface]:

        redundancy_counter = 0
        error_counter = 0
        total_number_transaction_inputs = len(df.index)
        input_type = 'transaction' # only used for response objects

        for i in range(total_number_transaction_inputs):
            account_public_id = InputService.get_str(df, i, identifier='UNIQUE_ACCOUNT_IDENTIFIER')
            channel_code = InputService.get_str(df, i, identifier='SALES_CHANNEL')
            public_id = InputService.get_str(df, i, identifier='TRANSACTION_EVENT_ID')
            activity_id = InputService.get_str(df, i, identifier='ACTIVITY_TRANSACTION_ID')
            item_sku = InputService.get_str(df, i, identifier='SELLER_SKU')

            if account_public_id and channel_code and public_id and activity_id and item_sku:

                redundancy_counter += TransactionInputService.handle_redundancy(account_public_id, channel_code, public_id, activity_id, item_sku)
                transaction_input_data = {
                    'created_by': user_id,
                    'original_filename': os.path.basename(file_path_in),

                    'account_public_id': account_public_id,
                    'public_activity_period': InputService.get_str(df, i, column='ACTIVITY_PERIOD').upper(),
                    'channel_code': channel_code,
                    'marketplace': InputService.get_str_or_None(df, i, column='MARKETPLACE'),
                    'transaction_type_public_code': InputService.get_str_or_None(df, i, column='TRANSACTION_TYPE'),
                    'public_id': public_id,
                    'activity_id': activity_id,

                    'check_tax_calculation_date': InputService.get_date_or_None(df, i, column='TAX_CALCULATION_DATE'),
                    'shipment_date': InputService.get_date_or_None(df, i, column='TRANSACTION_DEPART_DATE'),
                    'arrival_date': InputService.get_date_or_None(df, i, column='TRANSACTION_ARRIVAL_DATE'),
                    'complete_date': InputService.get_date_or_None(df, i, column='TRANSACTION_COMPLETE_DATE'),

                    'item_sku': item_sku,
                    'item_name': InputService.get_str(df, i, column='ITEM_DESCRIPTION'),
                    'item_manufacture_country': InputService.get_str_or_None(df, i, column='ITEM_MANUFACTURE_COUNTRY'),
                    'item_quantity': int(df.iloc[i]['QTY']),
                    'item_weight_kg': InputService.get_float(df, i, column='ITEM_WEIGHT'),
                    'item_weight_kg_total': InputService.get_float(df, i, column='TOTAL_ACTIVITY_WEIGHT'),

                    'check_unit_cost_price_net': InputService.get_float(df, i, column='COST_PRICE_OF_ITEMS'),

                    'check_item_price_discount_net': InputService.get_float(df, i, column='PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL'),
                    'check_item_price_discount_vat': InputService.get_float(df, i, column='PROMO_PRICE_OF_ITEMS_VAT_AMT'),
                    'item_price_discount_gross': InputService.get_float(df, i, column='PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL'),

                    'check_item_price_net': InputService.get_float(df, i, column='PRICE_OF_ITEMS_AMT_VAT_EXCL'),
                    'check_item_price_vat': InputService.get_float(df, i, column='PRICE_OF_ITEMS_VAT_AMT'),
                    'item_price_gross': InputService.get_float(df, i, column='PRICE_OF_ITEMS_AMT_VAT_INCL'),

                    'check_item_price_total_net': InputService.get_float(df, i, column='TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL'),
                    'check_item_price_total_vat': InputService.get_float(df, i, column='TOTAL_PRICE_OF_ITEMS_VAT_AMT'),
                    'item_price_total_gross': InputService.get_float(df, i, column='TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL'),

                    'check_item_price_vat_rate': InputService.get_float(df, i, column='PRICE_OF_ITEMS_VAT_RATE_PERCENT'),

                    'check_shipment_price_discount_net': InputService.get_float(df, i, column='PROMO_SHIP_CHARGE_AMT_VAT_EXCL'),
                    'check_shipment_price_discount_vat': InputService.get_float(df, i, column='PROMO_SHIP_CHARGE_VAT_AMT'),
                    'shipment_price_discount_gross': InputService.get_float(df, i, column='PROMO_SHIP_CHARGE_AMT_VAT_INCL'),

                    'check_shipment_price_net': InputService.get_float(df, i, column='SHIP_CHARGE_AMT_VAT_EXCL'),
                    'check_shipment_price_vat': InputService.get_float(df, i, column='SHIP_CHARGE_VAT_AMT'),
                    'shipment_price_gross': InputService.get_float(df, i, column='SHIP_CHARGE_AMT_VAT_INCL'),

                    'check_shipment_price_total_net': InputService.get_float(df, i, column='TOTAL_SHIP_CHARGE_AMT_VAT_EXCL'),
                    'check_shipment_price_total_vat': InputService.get_float(df, i, column='TOTAL_SHIP_CHARGE_VAT_AMT'),
                    'shipment_price_total_gross': InputService.get_float(df, i, column='TOTAL_SHIP_CHARGE_AMT_VAT_INCL'),

                    'check_shipment_price_vat_rate': InputService.get_float(df, i, column='SHIP_CHARGE_VAT_RATE_PERCENT'),

                    'check_sale_total_value_net': InputService.get_float(df, i, column='TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL'),
                    'check_sale_total_value_vat': InputService.get_float(df, i, column='TOTAL_ACTIVITY_VALUE_VAT_AMT'),
                    'sale_total_value_gross': InputService.get_float(df, i, column='TOTAL_ACTIVITY_VALUE_AMT_VAT_INCL'),

                    'check_gift_wrap_price_discount_net': InputService.get_float(df, i, column='PROMO_GIFT_WRAP_AMT_VAT_EXCL'),
                    'check_gift_wrap_price_discount_vat': InputService.get_float(df, i, column='PROMO_GIFT_WRAP_VAT_AMT'),
                    'gift_wrap_price_discount_gross': InputService.get_float(df, i, column='PROMO_GIFT_WRAP_AMT_VAT_INCL'),

                    'check_gift_wrap_price_net': InputService.get_float(df, i, column='GIFT_WRAP_AMT_VAT_EXCL'),
                    'check_gift_wrap_price_vat': InputService.get_float(df, i, column='GIFT_WRAP_VAT_AMT'),
                    'gift_wrap_price_gross': InputService.get_float(df, i, column='GIFT_WRAP_AMT_VAT_INCL'),

                    'check_gift_wrap_price_total_net': InputService.get_float(df, i, column='TOTAL_GIFT_WRAP_AMT_VAT_EXCL'),
                    'check_gift_wrap_price_total_vat': InputService.get_float(df, i, column='TOTAL_GIFT_WRAP_VAT_AMT'),
                    'gift_wrap_price_total_gross': InputService.get_float(df, i, column='TOTAL_GIFT_WRAP_AMT_VAT_INCL'),

                    'check_gift_wrap_price_tax_rate': InputService.get_float(df, i, column='GIFT_WRAP_VAT_RATE_PERCENT'),


                    'currency_code': InputService.get_str_or_None(df, i, column='TRANSACTION_CURRENCY_CODE'),

                    'check_item_tax_code_code': InputService.get_str_or_None(df, i, column='PRODUCT_TAX_CODE'),


                    'departure_country_code': InputService.get_str(df, i, column='DEPARTURE_COUNTRY'),
                    'departure_postal_code': InputService.get_str(df, i, column='DEPARTURE_POST_CODE'),
                    'departure_city': InputService.get_str(df, i, column='DEPATURE_CITY'),

                    'arrival_country_code': InputService.get_str(df, i, column='ARRIVAL_COUNTRY'),
                    'arrival_postal_code': InputService.get_str(df, i, column='ARRIVAL_POST_CODE'),
                    'arrival_city': InputService.get_str(df, i, column='ARRIVAL_CITY'),
                    'arrival_address': InputService.get_str_or_None(df, i, column='ARRIVAL_ADDRESS'),

                    'shipment_mode': InputService.get_str_or_None(df, i, column='TRANSPORTATION_MODE'),
                    'shipment_conditions': InputService.get_str_or_None(df, i, column='DELIVERY_CONDITIONS'),


                    'check_departure_seller_vat_country_code': InputService.get_str_or_None(df, i, column='SELLER_DEPART_VAT_NUMBER_COUNTRY'),
                    'check_departure_seller_vat_number': InputService.get_str_or_None(df, i, column='SELLER_DEPART_COUNTRY_VAT_NUMBER'),

                    'check_arrival_seller_vat_country_code': InputService.get_str_or_None(df, i, column='SELLER_ARRIVAL_VAT_NUMBER_COUNTRY'),
                    'check_arrival_seller_vat_number': InputService.get_str_or_None(df, i, column='SELLER_ARRIVAL_COUNTRY_VAT_NUMBER'),

                    'check_seller_vat_country_code': InputService.get_str_or_None(df, i, column='TRANSACTION_SELLER_VAT_NUMBER_COUNTRY'),
                    'check_seller_vat_number': InputService.get_str_or_None(df, i, column='TRANSACTION_SELLER_VAT_NUMBER'),


                    'check_tax_calculation_imputation_country': InputService.get_str_or_None(df, i, column='VAT_CALCULATION_IMPUTATION_COUNTRY'),
                    'check_tax_jurisdiction': InputService.get_str_or_None(df, i, column='TAXABLE_JURISDICTION'),
                    'check_tax_jurisdiction_level': InputService.get_str_or_None(df, i, column='TAXABLE_JURISDICTION_LEVEL'),

                    'invoice_number': InputService.get_str_or_None(df, i, column='VAT_INV_NUMBER'),
                    'check_invoice_amount_vat': InputService.get_float(df, i, column='VAT_INV_CONVERTED_AMT'),
                    'check_invoice_currency_code': InputService.get_str_or_None(df, i, column='VAT_INV_CURRENCY_CODE'),
                    'check_invoice_exchange_rate': InputService.get_float(df, i, column='VAT_INV_EXCHANGE_RATE'),
                    'check_invoice_exchange_rate_date': InputService.get_date_or_None(df, i, column='VAT_INV_EXCHANGE_RATE_DATE'),
                    'invoice_url': InputService.get_str_or_None(df, i, column='INVOICE_URL'),


                    'check_export': InputService.get_bool(df, i, column='EXPORT_OUTSIDE_EU', value_true='YES'),

                    'customer_name': InputService.get_str_or_None(df, i, column='BUYER_NAME'),
                    'customer_vat_number': InputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER'),
                    'customer_vat_number_country_code': InputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER_COUNTRY'),

                    'supplier_vat_number': InputService.get_str_or_None(df, i, column='SUPPLIER_VAT_NUMBER'),
                    'supplier_name': InputService.get_str_or_None(df, i, column='SUPPLIER_NAME')
                }

                try:
                    new_transaction_input = TransactionInputService.create_transaction_input(transaction_input_data)
                    TransactionService.create_transaction_s(transaction_input_data)

                except:
                    db.session.rollback()

                    error_counter += 1

            else:
                error_counter += 1


        response_objects = InputService.create_input_response_objects(file_path, input_type, total_number_items, error_counter, redundancy_counter=redundancy_counter)

        return response_objects


    @staticmethod
    def create_transaction_input(transaction_input_data: TransactionInputInterface) -> TransactionInput:
        new_transaction_input = TransactionInput(
            created_by = transaction_input_data.get('created_by'),
            original_filename = transaction_input_data.get('original_filename'),
            account_public_id = transaction_input_data.get('account_public_id'),
            public_activity_period = transaction_input_data.get('public_activity_period'),
            channel_code = transaction_input_data.get('channel_code'),
            marketplace = transaction_input_data.get('marketplace'),
            transaction_type_public_code = transaction_input_data.get('transaction_type_public_code'),
            public_id = transaction_input_data.get('public_id'),
            activity_id = transaction_input_data.get('activity_id'),
            check_tax_calculation_date = transaction_input_data.get('check_tax_calculation_date'),
            shipment_date = transaction_input_data.get('shipment_date'),
            arrival_date = transaction_input_data.get('arrival_date'),
            complete_date = transaction_input_data.get('complete_date'),
            item_sku = transaction_input_data.get('item_sku'),
            item_name = transaction_input_data.get('item_name'),
            item_manufacture_country = transaction_input_data.get('item_manufacture_country'),
            item_quantity = transaction_input_data.get('item_quantity'),
            item_weight_kg = transaction_input_data.get('item_weight_kg'),
            item_weight_kg_total = transaction_input_data.get('item_weight_kg_total'),
            check_unit_cost_price_net = transaction_input_data.get('check_unit_cost_price_net'),
            check_item_price_discount_net = transaction_input_data.get('check_item_price_discount_net'),
            check_item_price_discount_vat = transaction_input_data.get('check_item_price_discount_vat'),
            item_price_discount_gross = transaction_input_data.get('item_price_discount_gross'),
            check_item_price_net = transaction_input_data.get('check_item_price_net'),
            check_item_price_vat = transaction_input_data.get('check_item_price_vat'),
            item_price_gross = transaction_input_data.get('item_price_gross'),
            check_item_price_total_net = transaction_input_data.get('check_item_price_total_net'),
            check_item_price_total_vat = transaction_input_data.get('check_item_price_total_vat'),
            item_price_total_gross = transaction_input_data.get('item_price_total_gross'),
            check_item_price_vat_rate = transaction_input_data.get('check_item_price_vat_rate'),
            check_shipment_price_discount_net = transaction_input_data.get('check_shipment_price_discount_net'),
            check_shipment_price_discount_vat = transaction_input_data.get('check_shipment_price_discount_vat'),
            shipment_price_discount_gross = transaction_input_data.get('shipment_price_discount_gross'),
            check_shipment_price_net = transaction_input_data.get('check_shipment_price_net'),
            check_shipment_price_vat = transaction_input_data.get('check_shipment_price_vat'),
            shipment_price_gross = transaction_input_data.get('shipment_price_gross'),
            check_shipment_price_total_net = transaction_input_data.get('check_shipment_price_total_net'),
            check_shipment_price_total_vat = transaction_input_data.get('check_shipment_price_total_vat'),
            shipment_price_total_gross = transaction_input_data.get('shipment_price_total_gross'),
            check_shipment_price_vat_rate = transaction_input_data.get('check_shipment_price_vat_rate'),
            check_sale_total_value_net = transaction_input_data.get('check_sale_total_value_net'),
            check_sale_total_value_vat = transaction_input_data.get('check_sale_total_value_vat'),
            sale_total_value_gross = transaction_input_data.get('sale_total_value_gross'),
            check_gift_wrap_price_discount_net = transaction_input_data.get('check_gift_wrap_price_discount_net'),
            check_gift_wrap_price_discount_vat = transaction_input_data.get('check_gift_wrap_price_discount_vat'),
            gift_wrap_price_discount_gross = transaction_input_data.get('gift_wrap_price_discount_gross'),
            check_gift_wrap_price_net = transaction_input_data.get('check_gift_wrap_price_net'),
            check_gift_wrap_price_vat = transaction_input_data.get('check_gift_wrap_price_vat'),
            gift_wrap_price_gross = transaction_input_data.get('gift_wrap_price_gross'),
            check_gift_wrap_price_total_net = transaction_input_data.get('check_gift_wrap_price_total_net'),
            check_gift_wrap_price_total_vat = transaction_input_data.get('check_gift_wrap_price_total_vat'),
            gift_wrap_price_total_gross = transaction_input_data.get('gift_wrap_price_total_gross'),
            check_gift_wrap_price_tax_rate = transaction_input_data.get('check_gift_wrap_price_tax_rate'),
            currency_code = transaction_input_data.get('currency_code'),
            check_item_tax_code_code = transaction_input_data.get('check_item_tax_code_code'),
            departure_country_code = transaction_input_data.get('departure_country_code'),
            departure_postal_code = transaction_input_data.get('departure_postal_code'),
            departure_city = transaction_input_data.get('departure_city'),
            arrival_country_code = transaction_input_data.get('arrival_country_code'),
            arrival_postal_code = transaction_input_data.get('arrival_postal_code'),
            arrival_city = transaction_input_data.get('arrival_city'),
            arrival_address = transaction_input_data.get('arrival_address'),
            shipment_mode = transaction_input_data.get('shipment_mode'),
            shipment_conditions = transaction_input_data.get('shipment_conditions'),
            check_departure_seller_vat_country_code = transaction_input_data.get('check_departure_seller_vat_country_code'),
            check_departure_seller_vat_number = transaction_input_data.get('check_departure_seller_vat_number'),
            check_arrival_seller_vat_country_code = transaction_input_data.get('check_arrival_seller_vat_country_code'),
            check_arrival_seller_vat_number = transaction_input_data.get('check_arrival_seller_vat_number'),
            check_seller_vat_country_code = transaction_input_data.get('check_seller_vat_country_code'),
            check_seller_vat_number = transaction_input_data.get('check_seller_vat_number'),
            check_tax_calculation_imputation_country = transaction_input_data.get('check_tax_calculation_imputation_country'),
            check_tax_jurisdiction = transaction_input_data.get('check_tax_jurisdiction'),
            check_tax_jurisdiction_level = transaction_input_data.get('check_tax_jurisdiction_level'),
            invoice_number = transaction_input_data.get('invoice_number'),
            check_invoice_amount_vat = transaction_input_data.get('check_invoice_amount_vat'),
            check_invoice_currency_code = transaction_input_data.get('check_invoice_currency_code'),
            check_invoice_exchange_rate = transaction_input_data.get('check_invoice_exchange_rate'),
            check_invoice_exchange_rate_date = transaction_input_data.get('check_invoice_exchange_rate_date'),
            invoice_url = transaction_input_data.get('invoice_url'),
            check_export = transaction_input_data.get('check_export'),
            customer_name = transaction_input_data.get('customer_name'),
            customer_vat_number = transaction_input_data.get('customer_vat_number'),
            customer_vat_number_country_code = transaction_input_data.get('customer_vat_number_country_code'),
            supplier_vat_number = transaction_input_data.get('supplier_vat_number'),
            supplier_name = transaction_input_data.get('supplier_name')
        )

        db.session.add(new_transaction_input)
        db.session.commit()

        return new_transaction_input


    @staticmethod
    def handle_redundancy(account_public_id: str, channel_code: str, public_id: str) -> int:
        transation_input: TransactionInput = TransactionInput.query.filter_by(account_public_id=account_public_id, channel_code=channel_code, public_id=public_id, activity_id=activity_id, item_sku=item_sku).first()

        # if an item with the same sku for the specified validity period already exists, it is being deleted.
        if transation_input:
            db.session.delete(transation_input)
            redundancy_counter = 1
        else:
            redundancy_counter = 0

        return redundancy_counter
