import os
from datetime import datetime
import pandas as pd
from typing import List, BinaryIO, Dict

from flask import g, current_app
from werkzeug.exceptions import UnsupportedMediaType, NotFound
from app.extensions import db

from . import TransactionInput
from .interface import TransactionInputInterface

from ..account import Account
from ..utils.service import InputService



class TransactionInputService:

    @staticmethod
    def get_all() -> List[TransactionInput]:
        transaction_inputs = TransactionInput.query.all()
        return transaction_inputs

    @staticmethod
    def get_by_id(transaction_input_id: int) -> TransactionInput:
        return TransactionInput.query.filter(TransactionInput.id == transaction_input_id).first()

    @staticmethod
    def get_by_public_id(transaction_input_public_id: str) -> TransactionInput:
        return TransactionInput.query.filter(TransactionInput.public_id == transaction_input_public_id).first()

    @staticmethod
    def get_by_seller_firm_public_id(seller_firm_public_id: str) -> List[TransactionInput]:
        transaction_inputs = TransactionInput.query.join(TransactionInput.account).join(Account.seller_firm, aliased=True).filter_by(public_id=seller_firm_public_id).all()
        return transaction_inputs

    @staticmethod
    def get_by_identifiers(account_given_id: str, channel_code: str, given_id: str, activity_id: str, item_sku: str) -> TransactionInput:
        return TransactionInput.query.filter_by(account_given_id=account_given_id, channel_code=channel_code, given_id=given_id, activity_id=activity_id, item_sku=item_sku).first()


    @staticmethod
    def get_sale_transaction_input_by_bundle(bundle: 'app.namespaces.bundle.Bundle') -> TransactionInput:
        sale_transaction_input = TransactionInput.query.filter_by(bundle_id=bundle.id, transaction_type_public_code='SALE').first()
        if not sale_transaction_input:
            sale_transaction_input = TransactionInput.query.filter_by(bundle_id=bundle.id, transaction_type_public_code='COMMINGLING_BUY').first()

        return sale_transaction_input


    @staticmethod
    def update(transaction_input_id: int, data_changes: TransactionInputInterface) -> TransactionInput:
        transaction_input = TransactionInputService.get_by_id(transaction_input_id)
        if transaction_input:
            transaction_input.update(data_changes)
            db.session.commit()
            return transaction_input
        else:
            raise NotFound('The indicated transaction input does not exist.')

    @staticmethod
    def update_by_public_id(transaction_input_public_id: str, data_changes: TransactionInputInterface) -> TransactionInput:
        transaction_input = TransactionInputService.get_by_public_id(transaction_input_public_id)
        if transaction_input:
            transaction_input.update(data_changes)
            db.session.commit()
            return transaction_input
        else:
            raise NotFound('The indicated transaction input does not exist.')

    @staticmethod
    def delete_by_id(transaction_input_id: int):
        transaction_input = TransactionInput.query.filter(TransactionInput.id == transaction_input_id).first()
        if transaction_input:
            db.session.delete(transaction_input)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Transaction input (id: {}) has been successfully deleted.'.format(transaction_input_id)
            }
            return response_object
        else:
            raise NotFound('This transaction input does not exist.')

    @staticmethod
    def delete_by_public_id(transaction_input_public_id: str):
        transaction_input = TransactionInput.query.filter(TransactionInput.public_id == transaction_input_public_id).first()
        if transaction_input:
            db.session.delete(transaction_input)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Transaction input (public_id: {}) has been successfully deleted.'.format(transaction_input_public_id)
            }
            return response_object
        else:
            raise NotFound('This transaction input does not exist.')


    @staticmethod
    def delete_all() -> Dict:
        transaction_inputs = TransactionInput.query.all()
        if transaction_inputs:
            for transaction_input in transaction_inputs:
                db.session.delete(transaction_input)

            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'All transaction inputs have been successfully deleted.'
            }
            return response_object


    @staticmethod
    def get_df_transaction_input_delimiter(file: BinaryIO) -> str:
        if file.lower().endswith('.txt'):
            delimiter='\t'
        elif file.lower().endswith('.csv'):
            delimiter=None
        else:
            filename = os.path.basename(file)
            raise UnsupportedMediaType('File extension invalid (file: {}).'.format(filename))

        return delimiter


    @staticmethod
    def process_transaction_input_files_upload(transaction_input_files: List[BinaryIO]) -> Dict:
        BASE_PATH_TRANSACTION_DATA_SELLER_FIRM = current_app.config["BASE_PATH_TRANSACTION_DATA_SELLER_FIRM"]

        file_type='item_list'
        df_encoding = 'utf-8'
        basepath = BASE_PATH_TRANSACTION_DATA_SELLER_FIRM
        user_id = g.user.id

        for file in transaction_input_files:
            delimiter = TransactionInputService.get_df_transaction_input_delimiter(file)
            allowed_extensions = ['csv']
            file_path_in = InputService.store_file(file, allowed_extensions, basepath)
            TransactionInputService.process_transaction_input_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id)


        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(transaction_input_files)))
        }

        return response_object



    # celery task !!
    @staticmethod
    def process_transaction_input_file(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int) -> List[Dict]:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_objects = TransactionInputService.create_transaction_inputs_and_transactions(df, file_path_in, user_id)


        InputService.move_file_to_out(file_path_in, basepath, file_type)

        return response_objects



    @staticmethod
    def create_transaction_inputs_and_transactions(df: pd.DataFrame, file_path_in: str, user_id: int) -> List[Dict]:
        from ..transaction.service import TransactionService
        from ..account.service import AccountService
        from ..bundle.service import BundleService
        from ..item.service import ItemService


        error_counter = 0
        total_number_transaction_inputs = len(df.index)
        input_type = 'transaction' # only used for response objects
        transaction_inputs = []

        for i in range(total_number_transaction_inputs):
            account_given_id = InputService.get_str(df, i, column='UNIQUE_ACCOUNT_IDENTIFIER')
            channel_code = InputService.get_str(df, i, column='SALES_CHANNEL')
            account = AccountService.get_by_given_id_channel_code(account_given_id, channel_code)
            given_id = InputService.get_str(df, i, column='TRANSACTION_EVENT_ID')
            activity_id = InputService.get_str(df, i, column='ACTIVITY_TRANSACTION_ID')
            item_sku = InputService.get_str(df, i, column='SELLER_SKU')

            shipment_date = InputService.get_date_or_None(df, i, column='TRANSACTION_DEPART_DATE')
            arrival_date = InputService.get_date_or_None(df, i, column='TRANSACTION_ARRIVAL_DATE')
            complete_date = InputService.get_date_or_None(df, i, column='TRANSACTION_COMPLETE_DATE')

            item_date = ItemService.select_date_from_transaction_report(shipment_date, arrival_date, complete_date)

            item = ItemService.get_by_sku_account_date(item_sku, account, item_date)
            bundle = BundleService.get_or_create(account.id, item.id, given_id)

            if account_given_id and channel_code and given_id and activity_id and item_sku:

                transaction_input = TransactionInputService.get_by_identifiers(account_given_id, channel_code, given_id, activity_id, item_sku)
                if transaction_input and transaction_input.processed:
                    continue #skipping duplicates

                else:
                    transaction_input_data = {
                        'created_by': user_id,
                        'bundle_id': bundle.id,
                        'original_filename': os.path.basename(file_path_in),

                        'account_id': account.id,
                        'account_given_id': account_given_id,
                        'public_activity_period': InputService.get_str(df, i, column='ACTIVITY_PERIOD'),
                        'channel_code': channel_code,
                        'marketplace': InputService.get_str_or_None(df, i, column='MARKETPLACE'),
                        'transaction_type_public_code': InputService.get_str_or_None(df, i, column='TRANSACTION_TYPE'),
                        'given_id': given_id,
                        'activity_id': activity_id,

                        'check_tax_calculation_date': InputService.get_date_or_None(df, i, column='TAX_CALCULATION_DATE'),
                        'shipment_date': shipment_date,
                        'arrival_date': arrival_date,
                        'complete_date': complete_date,

                        'item_id': item.id,
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


                        'departure_country_code': InputService.get_str_or_None(df, i, column='DEPARTURE_COUNTRY'),
                        'departure_postal_code': InputService.get_single_str_compact(df, i, column='DEPARTURE_POST_CODE'),
                        'departure_city': InputService.get_str_or_None(df, i, column='DEPATURE_CITY'),

                        'arrival_country_code': InputService.get_str_or_None(df, i, column='ARRIVAL_COUNTRY'),
                        'arrival_postal_code': InputService.get_single_str_compact(df, i, column='ARRIVAL_POST_CODE'),
                        'arrival_city': InputService.get_str_or_None(df, i, column='ARRIVAL_CITY'),
                        'arrival_address': InputService.get_str_or_None(df, i, column='ARRIVAL_ADDRESS'),

                        'sale_departure_country_code': InputService.get_str_or_None(df, i, column='SALE_DEPART_COUNTRY'),
                        'sale_arrival_country_code': InputService.get_str_or_None(df, i, column='SALE_ARRIVAL_COUNTRY'),

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

                        'customer_firm_name': InputService.get_str_or_None(df, i, column='BUYER_NAME'),
                        'customer_firm_vat_number': InputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER'),
                        'customer_firm_vat_number_country_code': InputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER_COUNTRY'),

                        'supplier_vat_number': InputService.get_str_or_None(df, i, column='SUPPLIER_VAT_NUMBER'),
                        'supplier_name': InputService.get_str_or_None(df, i, column='SUPPLIER_NAME')
                    }

                    if transaction_input and not transaction_input.processed:
                        # update transaction_input

                        data_changes = {k:v for k,v in transaction_input_data.items() if v is not None}
                        if data_changes != {}:
                            try:
                                transaction_input.update(data_changes)
                                transaction_input.transactions = []
                                db.session.commit()
                            except:
                                db.session.rollback()
                                raise

                    else:
                        # create new transaction input
                        try:
                            transaction_input = TransactionInputService.create_transaction_input(transaction_input_data)
                            transaction_inputs.append(transaction_input)
                            print('')
                        except:
                            db.session.rollback()
                            raise




            else:
                error_counter += 1


        # after all transaction inputs have been stored transactions are created
        print('all transaction inputs have been stored', flush=True)
        for transaction_input in transaction_inputs:
            if not transaction_input.processed:
                try:
                    # create transactions
                    boolean = TransactionService.create_transaction_s(transaction_input)
                    print('boolean: {},  transaction_input: {}'.format(boolean, transaction_input), flush=True )
                    if boolean:
                        transaction_input.update_processed()
                        db.session.commit()

                except:
                    db.session.rollback()
                    raise #!!! to be deleted later

            else:
                continue

        response_objects = InputService.create_input_response_objects(file_path_in, input_type, total_number_transaction_inputs, error_counter, redundancy_counter=0)

        return response_objects


    @staticmethod
    def create_transaction_input(transaction_input_data: TransactionInputInterface) -> TransactionInput:

        new_transaction_input = TransactionInput(
            created_by = transaction_input_data.get('created_by'),
            bundle_id = transaction_input_data.get('bundle_id'),
            original_filename = transaction_input_data.get('original_filename'),
            account_id = transaction_input_data.get('account_id'),
            account_given_id = transaction_input_data.get('account_given_id'),
            public_activity_period = transaction_input_data.get('public_activity_period'),
            channel_code = transaction_input_data.get('channel_code'),
            marketplace = transaction_input_data.get('marketplace'),
            transaction_type_public_code = transaction_input_data.get('transaction_type_public_code'),
            given_id = transaction_input_data.get('given_id'),
            activity_id = transaction_input_data.get('activity_id'),
            check_tax_calculation_date = transaction_input_data.get('check_tax_calculation_date'),
            shipment_date = transaction_input_data.get('shipment_date'),
            arrival_date = transaction_input_data.get('arrival_date'),
            complete_date = transaction_input_data.get('complete_date'),
            item_id = transaction_input_data.get('item_id'),
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
            sale_departure_country_code = transaction_input_data.get('sale_departure_country_code'),
            sale_arrival_country_code = transaction_input_data.get('sale_arrival_country_code'),
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
            customer_firm_name = transaction_input_data.get('customer_firm_name'),
            customer_firm_vat_number = transaction_input_data.get('customer_firm_vat_number'),
            customer_firm_vat_number_country_code = transaction_input_data.get('customer_firm_vat_number_country_code'),
            supplier_vat_number = transaction_input_data.get('supplier_vat_number'),
            supplier_name = transaction_input_data.get('supplier_name')
        )


        db.session.add(new_transaction_input)
        db.session.commit()

        return new_transaction_input
