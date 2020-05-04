from datetime import datetime
import pandas as pd
from typing import List

from .model import TransactionInput

from werkzeug.exceptions import UnsupportedMediaType, NotFound
from app.extensions import db



class TransactionInputService:
    @staticmethod
    def read_transaction_upload_into_df(file) -> df:
        try:
            !!! if type(file) == txt !!! :
                    df = pd.read_csv(file, encoding='latin-1', delimiter='\t')
               !!! elif type(file) == csv  !!!!
                 df = pd.read_csv(file, encoding='latin-1')
                else:
                    raise UnsupportedMediaType('File extension invalid (file: {}).'.format(file))  !!!! filename
            return df
        except:
            raise UnsupportedMediaType('Cannot read file {}.'.format(file)) !!!! filename


    @staticmethod
    def get_date_or_None(df, i:int, column:str) -> date or None:
        if pd.isnull(df.iloc[i][column]):
            return None
        else:
            try:
                date = datetime.strptime(df.iloc[i][column], '%d-%m-%Y').date()
            except:
                try:
                    date = datetime.strptime(df.iloc[i][column], '%d.%m.%y').date()
                except:
                    raise UnsupportedMediaType('Can not read date format.')
        return date


    @staticmethod
    def get_str(df, i:int, column:str) -> str:
        try:
            string = str(df.iloc[i][column])
        except:
            raise UnsupportedMediaType('Can not read date format.')
        return string


    @staticmethod
    def get_str_or_None(df, i:int, column:str) -> str or None:
        if pd.isnull(df.iloc[i][column]):
            return None
        else:
            try:
                string = str(df.iloc[i][column])
            except:
                raise UnsupportedMediaType('Can not read date format.')

        return string


    @staticmethod
    def get_bool(df, i:int, column:str, value_true) -> bool:
        try:
            boolean = bool(df.iloc[i][column] == value_true)
        except:
            raise UnsupportedMediaType('Can not read date format.')

        return boolean


    @staticmethod
    def get_transaction_inputs_by_source(source: str):
        transaction_inputs = TransactionInput.query.filter_by(source=source).all()
        if transaction_inputs:
            return transaction_inputs

        else:
            raise NotFound('Can not find transaction inputs for the specified source ({}).'.format(source))




    @staticmethod
    def create_input_response_objects(file, total_number_transactions: int, error_counter: int, redundancy_counter: int) -> List[dict]:
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


        response_object = {
                'status': 'success',
                'message': 'The transaction file "{}" ({} transactions in total) has been {} uploaded. {}'.format(str(file.filename), str(total_number_transactions), success_status, notification)
        }

        response_objects.append(response_object)

        return response_objects


    @staticmethod
    def create_transaction_input(file):

        df = TransactionInputService.read_transaction_upload_into_df(file)

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
                        new_transaction_input = TransactionInputService.create_transaction_input_by_amazon_df(source=file.filename, df, i, account_public_id, channel_code, public_id, activity_id, item_sku)
                        db.session.add(new_transaction_input)
                        db.session.commit()
                    except:
                        !!!! db.session.rollback()
                        !!!! logger.log

                        error_counter += 1

                else:
                    redundancy_counter += 1

            else:
                error_counter += 1

        response_objects = TransactionInputService.create_input_response_objects(file, total_number_transactions, error_counter, redundancy_counter)

        return response_objects


    @staticmethod
    def get_transaction_input_identifier_from_amazon_df(df, i: int, identifier:str):
        try:
            if identifier == 'UNIQUE_ACCOUNT_IDENTIFIER':
                return TransactionInputService.get_str(df, i, column='UNIQUE_ACCOUNT_IDENTIFIER').upper()
            elif identifier == 'SALES_CHANNEL':
                return TransactionInputService.get_str(df, i, column='SALES_CHANNEL').upper() # str #-->PlatformService.retrieve_account()
            elif identifier == 'TRANSACTION_EVENT_ID':
                return TransactionInputService.get_str(df, i, column='TRANSACTION_EVENT_ID') # str #-->transaction
            elif identifier == 'ACTIVITY_TRANSACTION_ID':
                return TransactionInputService.get_str(df, i, column='ACTIVITY_TRANSACTION_ID')  # str #-->transaction --> becomes shipment_id/return_id , etc.
            elif identifier == 'SELLER_SKU':
                return TransactionInputService.get_str(df, i, column='SELLER_SKU')  # str #-->transaction --> becomes shipment_id/return_id , etc.

       except:
            return None #could be a file belonging to a different platform

    @staticmethod
    def get_transaction_input(account_public_id: str, channel_code: str, transaction_public_id: str, transaction_activity_id: str, item_sku: str) -> TransactionInput:
        transaction_input = TransactionInput.query.filter_by(account_public_id=account_public_id, channel_code=channel_code, transaction_public_id=transaction_public_id, transaction_activity_id=transaction_activity_id, item_sku=item_sku).first()
        return transaction_input


    @staticmethod
    def create_transaction_input_by_amazon_df(source: str, df, i: int, account_public_id: str, channel_code: str, public_id: str, activity_id: str, item_sku:str) -> TransactionInput

        account_public_id = account_public_id
        public_activity_period = TransactionInputService.get_str(df, i, column='ACTIVITY_PERIOD').upper() # --> OUTPUT
        channel_code = channel_code
        marketplace_name = TransactionInputService.get_str_or_None(df, i, column='MARKETPLACE') # str #-->transaction
        transaction_type_public_code = TransactionInputService.get_str_or_None(df, i, column='TRANSACTION_TYPE') #-->TransactionService.retrieve_transaction_type()
        public_id = public_id
        activity_id = activity_id


        check_tax_calculation_date = TransactionInputService.get_date_or_None(df, i, column='TAX_CALCULATION_DATE')
        shipment_date = TransactionInputService.get_date_or_None(df, i, column='TRANSACTION_DEPART_DATE')
        arrival_date = TransactionInputService.get_date_or_None(df, i, column='TRANSACTION_ARRIVAL_DATE')
        tax_date = TransactionInputService.get_date_or_None(df, i, column='TRANSACTION_COMPLETE_DATE')

        item_sku = item_sku  # str --> ItemService.retrieve_item() --> transaction
        item_name = str(df.iloc[i]['ITEM_DESCRIPTION']) #str
        item_manufacture_country = TransactionInputService.get_str_or_None(df, i, column='ITEM_MANUFACTURE_COUNTRY') #str/NoneType
        item_quantity = int(df.iloc[i]['QTY']) #-->transaction
        item_weight_kg = float(df.iloc[i]['ITEM_WEIGHT']) if not pd.isnull(df.iloc[i]['ITEM_WEIGHT']) else None #float/NoneType
        item_weight_kg_total = float(df.iloc[i]['TOTAL_ACTIVITY_WEIGHT']) if not pd.isnull(df.iloc[i]['TOTAL_ACTIVITY_WEIGHT']) else None

        unit_cost_price_net = float(df.iloc[i]['COST_PRICE_OF_ITEMS']) if not pd.isnull(df.iloc[i]['COST_PRICE_OF_ITEMS']) else None

        check_item_price_discount_net = float(df.iloc[i]['PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None
        check_item_price_discount_vat = float(df.iloc[i]['PROMO_PRICE_OF_ITEMS_VAT_AMT']) if not pd.isnull(df.iloc[i]['PROMO_PRICE_OF_ITEMS_VAT_AMT']) else None
        item_price_discount_gross = float(df.iloc[i]['PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL']) else None #-->transaction

        check_item_price_net = float(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None
        check_item_price_vat = float(df.iloc[i]['PRICE_OF_ITEMS_VAT_AMT']) if not pd.isnull(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None
        item_price_gross = float(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None #-->transaction

        check_item_price_total_net = float(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None
        check_item_price_total_vat = float(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_VAT_AMT']) if not pd.isnull(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_VAT_AMT']) else None
        item_price_total_gross = float(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL']) else None #-->transaction

        check_item_price_tax_rate_rate = float(df.iloc[i]['PRICE_OF_ITEMS_VAT_RATE_PERCENT']) if not pd.isnull(df.iloc[i]['PRICE_OF_ITEMS_VAT_RATE_PERCENT']) else None

        check_shipment_price_discount_net = float(df.iloc[i]['PROMO_SHIP_CHARGE_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) else None
        check_shipment_price_discount_vat = float(df.iloc[i]['PROMO_SHIP_CHARGE_VAT_AMT']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) else None
        shipment_price_discount_gross = float(df.iloc[i]['PROMO_SHIP_CHARGE_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) else None #-->transaction

        check_shipment_price_net = float(df.iloc[i]['SHIP_CHARGE_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['SHIP_CHARGE_AMT_VAT_EXCL']) else None
        check_shipment_price_vat = float(df.iloc[i]['SHIP_CHARGE_VAT_AMT']) if not pd.isnull(df.iloc[i]['SHIP_CHARGE_VAT_AMT']) else None
        shipment_price_gross = float(df.iloc[i]['SHIP_CHARGE_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['SHIP_CHARGE_AMT_VAT_INCL']) else None #-->transaction

        check_shipment_price_total_net = float(df.iloc[i]['TOTAL_SHIP_CHARGE_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['TOTAL_SHIP_CHARGE_AMT_VAT_EXCL']) else None
        check_shipment_price_total_vat = float(df.iloc[i]['TOTAL_SHIP_CHARGE_VAT_AMT']) if not pd.isnull(df.iloc[i]['TOTAL_SHIP_CHARGE_VAT_AMT']) else None
        shipment_price_total_gross = float(df.iloc[i]['TOTAL_SHIP_CHARGE_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['TOTAL_SHIP_CHARGE_AMT_VAT_INCL']) else None #-->transaction

        check_shipment_price_tax_rate_rate = float(df.iloc[i]['SHIP_CHARGE_VAT_RATE_PERCENT']) if not pd.isnull(df.iloc[i]['SHIP_CHARGE_VAT_RATE_PERCENT']) else None

        check_sale_total_value_net = float(df.iloc[i]['TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL']) else None
        check_sale_total_value_vat = float(df.iloc[i]['TOTAL_ACTIVITY_VALUE_VAT_AMT']) if not pd.isnull(df.iloc[i]['TOTAL_ACTIVITY_VALUE_VAT_AMT']) else None
        sale_total_value_gross = float(df.iloc[i]['TOTAL_ACTIVITY_VALUE_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['TOTAL_ACTIVITY_VALUE_AMT_VAT_INCL']) else None #-->transaction

        check_gift_wrap_price_discount_net = float(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) else None
        check_gift_wrap_price_discount_vat = float(df.iloc[i]['PROMO_GIFT_WRAP_VAT_AMT']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_VAT_AMT']) else None
        gift_wrap_price_discount_gross = float(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_INCL']) else None #-->transaction

        check_gift_wrap_price_net = float(df.iloc[i]['GIFT_WRAP_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['GIFT_WRAP_AMT_VAT_EXCL']) else None
        check_gift_wrap_price_vat = float(df.iloc[i]['GIFT_WRAP_VAT_AMT']) if not pd.isnull(df.iloc[i]['GIFT_WRAP_VAT_AMT']) else None
        gift_wrap_price_gross = float(df.iloc[i]['GIFT_WRAP_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['GIFT_WRAP_AMT_VAT_INCL']) else None #-->transaction

        check_gift_wrap_price_total_net = float(df.iloc[i]['TOTAL_GIFT_WRAP_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['TOTAL_GIFT_WRAP_AMT_VAT_EXCL']) else None
        check_gift_wrap_price_total_vat = float(df.iloc[i]['TOTAL_GIFT_WRAP_VAT_AMT']) if not pd.isnull(df.iloc[i]['TOTAL_GIFT_WRAP_VAT_AMT']) else None
        gift_wrap_price_total_gross = float(df.iloc[i]['TOTAL_GIFT_WRAP_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['TOTAL_GIFT_WRAP_AMT_VAT_INCL']) else None #-->transaction

        check_gift_wrap_price_tax_rate = float(df.iloc[i]['GIFT_WRAP_VAT_RATE_PERCENT']) if not pd.isnull(df.iloc[i]['GIFT_WRAP_VAT_RATE_PERCENT']) else None


        currency_code = TransactionInputService.get_str_or_None(df, i, column='TRANSACTION_CURRENCY_CODE') #str/NoneType

        check_item_tax_code_code = TransactionInputService.get_str_or_None(df, i, column='PRODUCT_TAX_CODE') #str/NoneType


        departure_country_code = str(df.iloc[i]['DEPARTURE_COUNTRY']) #str
        departure_postal_code = str(df.iloc[i]['DEPARTURE_POST_CODE']) #str
        departure_city = str(df.iloc[i]['DEPATURE_CITY']) #str

        arrival_country_code = str(df.iloc[i]['ARRIVAL_COUNTRY']) #str
        arrival_postal_code = str(df.iloc[i]['ARRIVAL_POST_CODE']) #str
        arrival_city = str(df.iloc[i]['ARRIVAL_CITY']) #str
        arrival_address = TransactionInputService.get_str_or_None(df, i, column='ARRIVAL_ADDRESS')  #str/NoneType

        shipment_mode = TransactionInputService.get_str_or_None(df, i, column='TRANSPORTATION_MODE') #str/NoneType
        shipment_conditions = TransactionInputService.get_str_or_None(df, i, column='DELIVERY_CONDITIONS') #str/NoneType


        check_departure_seller_vat_country_code = TransactionInputService.get_str_or_None(df, i, column='SELLER_DEPART_VAT_NUMBER_COUNTRY')
        check_departure_seller_vat_number = TransactionInputService.get_str_or_None(df, i, column='SELLER_DEPART_COUNTRY_VAT_NUMBER')

        check_arrival_seller_vat_country_code = TransactionInputService.get_str_or_None(df, i, column='SELLER_ARRIVAL_VAT_NUMBER_COUNTRY')
        check_arrival_seller_vat_number = TransactionInputService.get_str_or_None(df, i, column='SELLER_ARRIVAL_COUNTRY_VAT_NUMBER')

        check_seller_vat_country_code = TransactionInputService.get_str_or_None(df, i, column='TRANSACTION_SELLER_VAT_NUMBER_COUNTRY')
        check_seller_vat_number = TransactionInputService.get_str_or_None(df, i, column='TRANSACTION_SELLER_VAT_NUMBER')


        check_tax_calculation_imputation_country = TransactionInputService.get_str_or_None(df, i, column='VAT_CALCULATION_IMPUTATION_COUNTRY')
        check_tax_jurisdiction = TransactionInputService.get_str_or_None(df, i, column='TAXABLE_JURISDICTION')
        check_tax_jurisdiction_level = TransactionInputService.get_str_or_None(df, i, column='TAXABLE_JURISDICTION_LEVEL')

        invoice_number = TransactionInputService.get_str_or_None(df, i, column='VAT_INV_NUMBER')
        check_invoice_amount_vat = float(df.iloc[i]['VAT_INV_CONVERTED_AMT'])
        check_invoice_currency_code = TransactionInputService.get_str_or_None(df, i, column='VAT_INV_CURRENCY_CODE')
        check_invoice_exchange_rate = float(df.iloc[i]['VAT_INV_EXCHANGE_RATE']) if not pd.isnull(df.iloc[i]['VAT_INV_EXCHANGE_RATE']) else None
        check_invoice_exchange_rate_date = TransactionInputService.get_date_or_None(df, i, column='VAT_INV_EXCHANGE_RATE_DATE')
        invoice_url = TransactionInputService.get_str_or_None(df, i, column='INVOICE_URL')


        check_export = TransactionInputService.get_bool(df, i, column='EXPORT_OUTSIDE_EU', value_true='YES')  #str #-->transaction

        customer_name = TransactionInputService.get_str_or_None(df, i, column='BUYER_NAME')
        customer_vat_number = TransactionInputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER')
        customer_vat_number_country_code = TransactionInputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER_COUNTRY')

        supplier_vat_number = TransactionInputService.get_str_or_None(df, i, column='SUPPLIER_VAT_NUMBER') # #NoneType/str object #-->transaction
        supplier_name = TransactionInputService.get_str_or_None(df, i, column='SUPPLIER_NAME') #NoneType/str object #-->transaction

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
            unit_cost_price_net = unit_cost_price_net,
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
