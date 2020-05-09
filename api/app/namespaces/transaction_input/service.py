import os
from datetime import datetime
import pandas as pd
from typing import List
from flask import current_app
from .model import TransactionInput

from werkzeug.exceptions import UnsupportedMediaType, NotFound
from app.extensions import db

from ..utils.service import InputService

class TransactionInputService:

    @staticmethod
    def read_transaction_upload_into_df(file) -> df:
        try:
            !!! if file.is_file() and file.lower().endswith('.txt'):
                    df = pd.read_csv(file, encoding='latin-1', delimiter='\t')
               !!! elif if file.is_file() and file.lower().endswith('.csv'):
                 df = pd.read_csv(file, encoding='latin-1')
                else:
                    raise UnsupportedMediaType('File extension invalid (file: {}).'.format(file))  !!!! filename
            return df
        except:
            raise UnsupportedMediaType('Cannot read file {}.'.format(file)) !!!! filename


    @staticmethod
    def get_transaction_inputs_by_source(source: str) -> List[TransactionInput]:
        transaction_inputs = TransactionInput.query.filter_by(source=source).all()
        if transaction_inputs:
            return transaction_inputs

        else:
            raise NotFound('Can not find transaction inputs for the specified source ({}).'.format(source))




    @staticmethod
    def create_input_response_objects(file_path, total_number_transactions: int, error_counter: int, redundancy_counter: int) -> List[dict]:
        response_objects = []
        success_status = 'successfully'
        notification = ''

        if redundancy_counter > 0:
            response_object_info = {
                'status': 'info',
                'message': '{} transactions had been uploaded earlier already and were skipped.'.format(str(redundancy_counter))
            }
            response_objects.append(response_object_info)


        if error_counter > 0:
            notification = 'However, please recheck the submitted file for invalid data.'

            response_object_error = {
                'status': 'warning',
                'message': 'For {} transactions, the necessary transaction details could not be read.'.format(str(error_counter))
            }
            response_objects.append(response_object_error)

        filename = os.path.basename(file_path)
        response_object = {
                'status': 'success',
                'message': 'The transaction file "{}" ({} transactions in total) has been {} uploaded. {}'.format(filename, str(total_number_transactions), success_status, notification)
        }

        response_objects.append(response_object)

        return response_objects


    @staticmethod
    def create_transaction_input(file_path):

        df = TransactionInputService.read_transaction_upload_into_df(file_path)

        redundancy_counter = 0
        error_counter = 0
        total_number_transactions = len(df.index)

        for i in range(total_number_transactions):
            account_public_id = TransactionInputService.get_transaction_input_identifier_from_amazon_df(df, i, identifier='UNIQUE_ACCOUNT_IDENTIFIER')
            channel_code = TransactionInputService.get_transaction_input_identifier_from_amazon_df(df, i, identifier='SALES_CHANNEL')
            public_id = TransactionInputService.get_transaction_input_identifier_from_amazon_df(df, i, identifier='TRANSACTION_EVENT_ID')
            activity_id = TransactionInputService.get_transaction_input_identifier_from_amazon_df(df, i, identifier='ACTIVITY_TRANSACTION_ID')
            item_sku = TransactionInputService.get_transaction_input_identifier_from_amazon_df(df, i, identifier='SELLER_SKU')

            if account_public_id and channel_code and public_id and activity_id and item_sku:

                # in the future other platforms will be added << HERE >>
                transaction_input = TransactionInputService.get_transaction_input(account_public_id, channel_code, public_id, activity_id, item_sku)
                if not transaction_input:
                    try:
                        new_transaction_input = TransactionInputService.create_transaction_input_by_amazon_df(source=file_path, df, i, account_public_id, channel_code, public_id, activity_id, item_sku)
                        db.session.add(new_transaction_input)
                        db.session.commit()
                    except:
                        db.session.rollback()

                        error_counter += 1

                else:
                    redundancy_counter += 1

            else:
                error_counter += 1

        response_objects = TransactionInputService.create_input_response_objects(file_path, total_number_transactions, error_counter, redundancy_counter)

        return response_objects


    @staticmethod
    def get_transaction_input_identifier_from_amazon_df(df, i: int, identifier:str):
        try:
            if identifier == 'UNIQUE_ACCOUNT_IDENTIFIER':
                return InputService.get_str(df, i, column='UNIQUE_ACCOUNT_IDENTIFIER').upper()
            elif identifier == 'SALES_CHANNEL':
                return InputService.get_str(df, i, column='SALES_CHANNEL').upper() # str #-->PlatformService.retrieve_account()
            elif identifier == 'TRANSACTION_EVENT_ID':
                return InputService.get_str(df, i, column='TRANSACTION_EVENT_ID') # str #-->transaction
            elif identifier == 'ACTIVITY_TRANSACTION_ID':
                return InputService.get_str(df, i, column='ACTIVITY_TRANSACTION_ID')  # str #-->transaction --> becomes shipment_id/return_id , etc.
            elif identifier == 'SELLER_SKU':
                return InputService.get_str(df, i, column='SELLER_SKU')  # str #-->transaction --> becomes shipment_id/return_id , etc.

       except:
            return None #could be a file belonging to a different platform

    @staticmethod
    def get_transaction_input(account_public_id: str, channel_code: str, transaction_public_id: str, transaction_activity_id: str, item_sku: str) -> TransactionInput:
        transaction_input = TransactionInput.query.filter_by(account_public_id=account_public_id, channel_code=channel_code, transaction_public_id=transaction_public_id, transaction_activity_id=transaction_activity_id, item_sku=item_sku).first()
        return transaction_input


    @staticmethod
    def create_transaction_input_by_amazon_df(source: str, df, i: int, account_public_id: str, channel_code: str, public_id: str, activity_id: str, item_sku:str) -> TransactionInput

        account_public_id = account_public_id
        public_activity_period = InputService.get_str(df, i, column='ACTIVITY_PERIOD').upper() # --> OUTPUT
        channel_code = channel_code
        marketplace_name = InputService.get_str_or_None(df, i, column='MARKETPLACE') # str #-->transaction
        transaction_type_public_code = InputService.get_str_or_None(df, i, column='TRANSACTION_TYPE') #-->TransactionService.retrieve_transaction_type()
        public_id = public_id
        activity_id = activity_id


        check_tax_calculation_date = InputService.get_date_or_None(df, i, column='TAX_CALCULATION_DATE')
        shipment_date = InputService.get_date_or_None(df, i, column='TRANSACTION_DEPART_DATE')
        arrival_date = InputService.get_date_or_None(df, i, column='TRANSACTION_ARRIVAL_DATE')
        tax_date = InputService.get_date_or_None(df, i, column='TRANSACTION_COMPLETE_DATE')

        item_sku = item_sku  # str --> ItemService.retrieve_item() --> transaction
        item_name = str(df.iloc[i]['ITEM_DESCRIPTION']) #str
        item_manufacture_country = InputService.get_str_or_None(df, i, column='ITEM_MANUFACTURE_COUNTRY') #str/NoneType
        item_quantity = int(df.iloc[i]['QTY']) #-->transaction
        item_weight_kg = InputService.get_float(df, i, column='ITEM_WEIGHT')
        item_weight_kg_total = InputService.get_float(df, i, column='TOTAL_ACTIVITY_WEIGHT')

        check_unit_cost_price_net = InputService.get_float(df, i, column='COST_PRICE_OF_ITEMS')

        check_item_price_discount_net = InputService.get_float(df, i, column='PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL')
        check_item_price_discount_vat = InputService.get_float(df, i, column='PROMO_PRICE_OF_ITEMS_VAT_AMT')
        item_price_discount_gross = InputService.get_float(df, i, column='PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL') #-->transaction

        check_item_price_net = InputService.get_float(df, i, column='PRICE_OF_ITEMS_AMT_VAT_EXCL')
        check_item_price_vat = InputService.get_float(df, i, column='PRICE_OF_ITEMS_VAT_AMT')
        item_price_gross = InputService.get_float(df, i, column='PRICE_OF_ITEMS_AMT_VAT_INCL') #-->transaction

        check_item_price_total_net = InputService.get_float(df, i, column='TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL')
        check_item_price_total_vat = InputService.get_float(df, i, column='TOTAL_PRICE_OF_ITEMS_VAT_AMT')
        item_price_total_gross = InputService.get_float(df, i, column='TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL') #-->transaction

        check_item_price_tax_rate_rate = InputService.get_float(df, i, column='PRICE_OF_ITEMS_VAT_RATE_PERCENT')

        check_shipment_price_discount_net = InputService.get_float(df, i, column='PROMO_SHIP_CHARGE_AMT_VAT_EXCL')
        check_shipment_price_discount_vat = InputService.get_float(df, i, column='PROMO_SHIP_CHARGE_VAT_AMT')
        shipment_price_discount_gross = InputService.get_float(df, i, column='PROMO_SHIP_CHARGE_AMT_VAT_INCL') #-->transaction

        check_shipment_price_net = InputService.get_float(df, i, column='SHIP_CHARGE_AMT_VAT_EXCL')
        check_shipment_price_vat = InputService.get_float(df, i, column='SHIP_CHARGE_VAT_AMT')
        shipment_price_gross = InputService.get_float(df, i, column='SHIP_CHARGE_AMT_VAT_INCL') #-->transaction

        check_shipment_price_total_net = InputService.get_float(df, i, column='TOTAL_SHIP_CHARGE_AMT_VAT_EXCL')
        check_shipment_price_total_vat = InputService.get_float(df, i, column='TOTAL_SHIP_CHARGE_VAT_AMT')
        shipment_price_total_gross = InputService.get_float(df, i, column='TOTAL_SHIP_CHARGE_AMT_VAT_INCL') #-->transaction

        check_shipment_price_tax_rate_rate = InputService.get_float(df, i, column='SHIP_CHARGE_VAT_RATE_PERCENT')

        check_sale_total_value_net = InputService.get_float(df, i, column='TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL')
        check_sale_total_value_vat = InputService.get_float(df, i, column='TOTAL_ACTIVITY_VALUE_VAT_AMT')
        sale_total_value_gross = InputService.get_float(df, i, column='TOTAL_ACTIVITY_VALUE_AMT_VAT_INCL') #-->transaction

        check_gift_wrap_price_discount_net = InputService.get_float(df, i, column='PROMO_GIFT_WRAP_AMT_VAT_EXCL')
        check_gift_wrap_price_discount_vat = InputService.get_float(df, i, column='PROMO_GIFT_WRAP_VAT_AMT')
        gift_wrap_price_discount_gross = InputService.get_float(df, i, column='PROMO_GIFT_WRAP_AMT_VAT_INCL') #-->transaction

        check_gift_wrap_price_net = InputService.get_float(df, i, column='GIFT_WRAP_AMT_VAT_EXCL')
        check_gift_wrap_price_vat = InputService.get_float(df, i, column='GIFT_WRAP_VAT_AMT')
        gift_wrap_price_gross = InputService.get_float(df, i, column='GIFT_WRAP_AMT_VAT_INCL') #-->transaction

        check_gift_wrap_price_total_net = InputService.get_float(df, i, column='TOTAL_GIFT_WRAP_AMT_VAT_EXCL')
        check_gift_wrap_price_total_vat = InputService.get_float(df, i, column='TOTAL_GIFT_WRAP_VAT_AMT')
        gift_wrap_price_total_gross = InputService.get_float(df, i, column='TOTAL_GIFT_WRAP_AMT_VAT_INCL') #-->transaction

        check_gift_wrap_price_tax_rate = InputService.get_float(df, i, column='GIFT_WRAP_VAT_RATE_PERCENT')


        currency_code = InputService.get_str_or_None(df, i, column='TRANSACTION_CURRENCY_CODE') #str/NoneType

        check_item_tax_code_code = InputService.get_str_or_None(df, i, column='PRODUCT_TAX_CODE') #str/NoneType


        departure_country_code = str(df.iloc[i]['DEPARTURE_COUNTRY']) #str
        departure_postal_code = str(df.iloc[i]['DEPARTURE_POST_CODE']) #str
        departure_city = str(df.iloc[i]['DEPATURE_CITY']) #str

        arrival_country_code = str(df.iloc[i]['ARRIVAL_COUNTRY']) #str
        arrival_postal_code = str(df.iloc[i]['ARRIVAL_POST_CODE']) #str
        arrival_city = str(df.iloc[i]['ARRIVAL_CITY']) #str
        arrival_address = InputService.get_str_or_None(df, i, column='ARRIVAL_ADDRESS')  #str/NoneType

        shipment_mode = InputService.get_str_or_None(df, i, column='TRANSPORTATION_MODE') #str/NoneType
        shipment_conditions = InputService.get_str_or_None(df, i, column='DELIVERY_CONDITIONS') #str/NoneType


        check_departure_seller_vat_country_code = InputService.get_str_or_None(df, i, column='SELLER_DEPART_VAT_NUMBER_COUNTRY')
        check_departure_seller_vat_number = InputService.get_str_or_None(df, i, column='SELLER_DEPART_COUNTRY_VAT_NUMBER')

        check_arrival_seller_vat_country_code = InputService.get_str_or_None(df, i, column='SELLER_ARRIVAL_VAT_NUMBER_COUNTRY')
        check_arrival_seller_vat_number = InputService.get_str_or_None(df, i, column='SELLER_ARRIVAL_COUNTRY_VAT_NUMBER')

        check_seller_vat_country_code = InputService.get_str_or_None(df, i, column='TRANSACTION_SELLER_VAT_NUMBER_COUNTRY')
        check_seller_vat_number = InputService.get_str_or_None(df, i, column='TRANSACTION_SELLER_VAT_NUMBER')


        check_tax_calculation_imputation_country = InputService.get_str_or_None(df, i, column='VAT_CALCULATION_IMPUTATION_COUNTRY')
        check_tax_jurisdiction = InputService.get_str_or_None(df, i, column='TAXABLE_JURISDICTION')
        check_tax_jurisdiction_level = InputService.get_str_or_None(df, i, column='TAXABLE_JURISDICTION_LEVEL')

        invoice_number = InputService.get_str_or_None(df, i, column='VAT_INV_NUMBER')
        check_invoice_amount_vat = InputService.get_float(df, i, column='VAT_INV_CONVERTED_AMT')
        check_invoice_currency_code = InputService.get_str_or_None(df, i, column='VAT_INV_CURRENCY_CODE')
        check_invoice_exchange_rate = InputService.get_float(df, i, column='VAT_INV_EXCHANGE_RATE')
        check_invoice_exchange_rate_date = InputService.get_date_or_None(df, i, column='VAT_INV_EXCHANGE_RATE_DATE')
        invoice_url = InputService.get_str_or_None(df, i, column='INVOICE_URL')


        check_export = InputService.get_bool(df, i, column='EXPORT_OUTSIDE_EU', value_true='YES')  #str #-->transaction

        customer_name = InputService.get_str_or_None(df, i, column='BUYER_NAME')
        customer_vat_number = InputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER')
        customer_vat_number_country_code = InputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER_COUNTRY')

        supplier_vat_number = InputService.get_str_or_None(df, i, column='SUPPLIER_VAT_NUMBER') # #NoneType/str object #-->transaction
        supplier_name = InputService.get_str_or_None(df, i, column='SUPPLIER_NAME') #NoneType/str object #-->transaction

        new_transaction_input = TransactionInput(
            source = source,
            account_public_id = account_public_id,
            public_activity_period = public_activity_period,
            channel_code = channel_code,
            marketplace_name = marketplace_name,
            transaction_type_public_code = transaction_type_public_code,
            transaction_public_id = transaction_public_id,
            transaction_activity_id = transaction_activity_id,
            check_tax_calculation_date = check_tax_calculation_date,
            shipment_date = shipment_date,
            arrival_date = arrival_date,
            tax_date = tax_date,
            item_sku = item_sku,
            item_name = item_name,
            item_manufacture_country = item_manufacture_country,
            item_quantity = item_quantity,
            item_weight_kg = item_weight_kg,
            item_weight_kg_total = item_weight_kg_total,
            check_unit_cost_price_net = check_unit_cost_price_net,
            check_item_price_discount_net = check_item_price_discount_net,
            check_item_price_discount_vat = check_item_price_discount_vat,
            item_price_discount_gross = item_price_discount_gross,
            check_item_price_net = check_item_price_net,
            check_item_price_vat = check_item_price_vat,
            item_price_gross = item_price_gross,
            check_item_price_total_net = check_item_price_total_net,
            check_item_price_total_vat = check_item_price_total_vat,
            item_price_total_gross = item_price_total_gross,
            check_item_price_tax_rate_rate = check_item_price_tax_rate_rate,
            check_shipment_price_discount_net = check_shipment_price_discount_net,
            check_shipment_price_discount_vat = check_shipment_price_discount_vat,
            shipment_price_discount_gross = shipment_price_discount_gross,
            check_shipment_price_net = check_shipment_price_net,
            check_shipment_price_vat = check_shipment_price_vat,
            shipment_price_gross = shipment_price_gross,
            check_shipment_price_total_net = check_shipment_price_total_net,
            check_shipment_price_total_vat = check_shipment_price_total_vat,
            shipment_price_total_gross = shipment_price_total_gross,
            check_shipment_price_tax_rate_rate = check_shipment_price_tax_rate_rate,
            check_sale_total_value_net = check_sale_total_value_net,
            check_sale_total_value_vat = check_sale_total_value_vat,
            sale_total_value_gross = sale_total_value_gross,
            check_gift_wrap_price_discount_net = check_gift_wrap_price_discount_net,
            check_gift_wrap_price_discount_vat = check_gift_wrap_price_discount_vat,
            gift_wrap_price_discount_gross = gift_wrap_price_discount_gross,
            check_gift_wrap_price_net = check_gift_wrap_price_net,
            check_gift_wrap_price_vat = check_gift_wrap_price_vat,
            gift_wrap_price_gross = gift_wrap_price_gross,
            check_gift_wrap_price_total_net = check_gift_wrap_price_total_net,
            check_gift_wrap_price_total_vat = check_gift_wrap_price_total_vat,
            gift_wrap_price_total_gross = gift_wrap_price_total_gross,
            check_gift_wrap_price_tax_rate = check_gift_wrap_price_tax_rate,
            currency_code = currency_code,
            check_item_tax_code_code = check_item_tax_code_code,
            departure_country_code = departure_country_code,
            departure_postal_code = departure_postal_code,
            departure_city = departure_city,
            arrival_country_code = arrival_country_code,
            arrival_postal_code = arrival_postal_code,
            arrival_city = arrival_city,
            arrival_address = arrival_address,
            shipment_mode = shipment_mode,
            shipment_conditions = shipment_conditions,
            check_departure_seller_vat_country_code = check_departure_seller_vat_country_code,
            check_departure_seller_vat_number = check_departure_seller_vat_number,
            check_arrival_seller_vat_country_code = check_arrival_seller_vat_country_code,
            check_arrival_seller_vat_number = check_arrival_seller_vat_number,
            check_seller_vat_country_code = check_seller_vat_country_code,
            check_seller_vat_number = check_seller_vat_number,
            check_tax_calculation_imputation_country = check_tax_calculation_imputation_country,
            check_tax_jurisdiction = check_tax_jurisdiction,
            check_tax_jurisdiction_level = check_tax_jurisdiction_level,
            invoice_number = invoice_number,
            check_invoice_amount_vat = check_invoice_amount_vat,
            check_invoice_currency_code = check_invoice_currency_code,
            check_invoice_exchange_rate = check_invoice_exchange_rate,
            check_invoice_exchange_rate_date = check_invoice_exchange_rate_date,
            invoice_url = invoice_url,
            check_export = check_export,
            customer_name = customer_name,
            customer_vat_number = customer_vat_number,
            customer_vat_number_country_code = customer_vat_number_country_code,
            supplier_vat_number = supplier_vat_number,
            supplier_name = supplier_name
        )

        return new_transaction_input
