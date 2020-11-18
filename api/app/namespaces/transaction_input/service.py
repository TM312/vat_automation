import os
from datetime import datetime
import pandas as pd
from typing import List, BinaryIO, Dict

from flask import g, current_app
from sqlalchemy import or_
from werkzeug.exceptions import UnsupportedMediaType, NotFound, UnprocessableEntity, ExpectationFailed
from app.extensions import (
    db,
    socket_io)

from . import TransactionInput
from .interface import TransactionInputInterface
from .schema import TransactionInputSubSchema

from app.namespaces.account import Account
from app.namespaces.utils.service import InputService, NotificationService
from app.namespaces.tag.service import TagService
from app.namespaces.bundle import Bundle
from app.namespaces.bundle.service import BundleService
from app.namespaces.transaction.service import TransactionService


from app.extensions.socketio.emitters import SocketService


class TransactionInputService:

    @staticmethod
    def get_all() -> List[TransactionInput]:
        transaction_inputs = TransactionInput.query.all()
        return transaction_inputs

    @staticmethod
    def get_by_id(transaction_input_id: int) -> TransactionInput:
        return TransactionInput.query.filter_by(id = transaction_input_id).first()

    @staticmethod
    def get_by_public_id(transaction_input_public_id: str) -> TransactionInput:
        if transaction_input_public_id == 'undefined':
            return None
        else:
            return TransactionInput.query.filter_by(public_id = transaction_input_public_id).first()


    @staticmethod
    def get_by_bundle_public_id(bundle_public_id: str) -> List[TransactionInput]:
        if bundle_public_id == 'undefined' or bundle_public_id is None:
            print('bundle_public_id == undefined')
            return None
        else:
            bundle = BundleService.get_by_public_id(bundle_public_id)
        if isinstance(bundle, Bundle):
            return TransactionInput.query.filter_by(bundle_id=bundle.id).all()

    @staticmethod
    def get_all_by_seller_firm_id(seller_firm_id: int) -> List[TransactionInput]:
        return TransactionInput.query.filter_by(seller_firm_id=seller_firm_id).all()

    @staticmethod
    def get_all_by_seller_firm_public_id(seller_firm_public_id: str) -> List[TransactionInput]:
        from app.namespaces.business.seller_firm.service import SellerFirmService
        seller_firm_id = SellerFirmService.get_by_public_id(seller_firm_public_id).id
        return TransactionInput.query.filter_by(seller_firm_id=seller_firm_id).all()


    @staticmethod
    def get_by_seller_firm_public_id(seller_firm_public_id: str, **kwargs) -> List[TransactionInput]:
        from app.namespaces.business.seller_firm.service import SellerFirmService
        seller_firm_id = SellerFirmService.get_by_public_id(seller_firm_public_id).id
        #base_query = TransactionInput.query.join(TransactionInput.account).join(Account.seller_firm, aliased=True).filter_by(public_id=seller_firm_public_id).order_by(TransactionInput.complete_date.desc())
        base_query = TransactionInput.query.filter_by(seller_firm_id=seller_firm_id).order_by(TransactionInput.complete_date.desc())
        if kwargs.get('paginate') == True and isinstance(kwargs.get('page'), int):
            per_page = current_app.config.TRANSACTIONS_PER_QUERY
            page = kwargs.get('page')
            transaction_inputs = base_query.paginate(page, per_page, False).items

        else:
            transaction_inputs = base_query.all()
        return transaction_inputs

    @staticmethod
    def get_by_identifiers(account_given_id: str, channel_code: str, given_id: str, activity_id: str, item_sku: str) -> TransactionInput:
        return TransactionInput.query.filter(
            TransactionInput.account_given_id==account_given_id,
            TransactionInput.channel_code==channel_code,
            TransactionInput.given_id==given_id,
            TransactionInput.activity_id==activity_id,
            TransactionInput.item_sku==item_sku
            ).first()


    @staticmethod
    def get_sale_transaction_input_by_bundle_id(bundle_id: int) -> TransactionInput:
        return TransactionInput.query.filter(
            TransactionInput.bundle_id==bundle_id,
            or_(
                TransactionInput.transaction_type_public_code=='SALE',
                TransactionInput.transaction_type_public_code=='COMMINGLING_BUY'
                )
            ).first()


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
        transaction_input = TransactionInputService.get_by_id(transaction_input_id)
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
        transaction_input = TransactionInputService.get_by_public_id(transaction_input_public_id)
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
    def handle_transaction_input_data_upload(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: Dict) -> Dict:
        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_object = TransactionInputService.create_transaction_inputs_and_transactions(df, file_path_in, user_id)
        tag = TagService.get_by_code('TRANSACTION')
        NotificationService.handle_seller_firm_notification_data_upload(seller_firm_id, user_id, tag, seller_firm_notification_data)
        InputService.move_file_to_out(file_path_in, basepath, file_type, business_id=seller_firm_id)

        return response_object

    @staticmethod
    def get_df_vars(df: pd.DataFrame, i: int, current: int, object_type: str) -> List:

        try:
            account_given_id = InputService.get_str(df, i, column='UNIQUE_ACCOUNT_IDENTIFIER')
        except:
            raise UnprocessableEntity('UNIQUE_ACCOUNT_IDENTIFIER')

        try:
            channel_code = InputService.get_str(df, i, column='SALES_CHANNEL')
        except:
            raise UnprocessableEntity('SALES_CHANNEL')

        try:
            given_id = InputService.get_str(df, i, column='TRANSACTION_EVENT_ID')
        except:
            raise UnprocessableEntity('TRANSACTION_EVENT_ID')

        try:
            activity_id = InputService.get_str(df, i, column='ACTIVITY_TRANSACTION_ID')
        except:
            raise UnprocessableEntity('ACTIVITY_TRANSACTION_ID')

        try:
            item_sku = InputService.get_str(df, i, column='SELLER_SKU')
        except:
            raise UnprocessableEntity('SELLER_SKU')

        try:
            shipment_date = InputService.get_date_or_None(df, i, column='TRANSACTION_DEPART_DATE')
        except:
            raise UnprocessableEntity('TRANSACTION_DEPART_DATE')

        try:
            arrival_date = InputService.get_date_or_None(df, i, column='TRANSACTION_ARRIVAL_DATE')
        except:
            raise UnprocessableEntity('TRANSACTION_ARRIVAL_DATE')

        try:
            complete_date = InputService.get_date_or_None(df, i, column='TRANSACTION_COMPLETE_DATE')
        except:
            raise UnprocessableEntity('TRANSACTION_COMPLETE_DATE')


        # send error status via socket
        if not account_given_id or account_given_id == '':
            raise ExpectationFailed('UNIQUE_ACCOUNT_IDENTIFIER')

        if not channel_code or channel_code == '':
            raise ExpectationFailed('SALES_CHANNEL')

        if not given_id or given_id == '':
            raise ExpectationFailed('TRANSACTION_EVENT_ID')

        if not activity_id or activity_id == '':
            raise ExpectationFailed('ACTIVITY_TRANSACTION_ID')

        if not item_sku or item_sku == '':
            raise ExpectationFailed('SELLER_SKU')

        return account_given_id, channel_code, given_id, activity_id, item_sku, shipment_date, arrival_date, complete_date

    @staticmethod
    def verify_transaction_order(df, total) -> bool:

        complete_date_top = InputService.get_date_or_None(df, 0, column='TRANSACTION_COMPLETE_DATE')
        complete_date_bottom = InputService.get_date_or_None(df, total, column='TRANSACTION_COMPLETE_DATE')

        return complete_date_top >= complete_date_bottom



    @staticmethod
    def create_transaction_inputs_and_transactions(df: pd.DataFrame, file_path_in: str, user_id: int) -> List[Dict]:
        from app.namespaces.account.service import AccountService
        from app.namespaces.bundle.service import BundleService
        from app.namespaces.item.service import ItemService
        from app.namespaces.distance_sale.service import DistanceSaleService

        print('enter create_transaction_inputs_and_transactions', flush=True)

        error_counter = 0
        total = total_number_transaction_inputs = len(df.index)
        input_type = 'transaction' # only used for response objects
        transaction_inputs = []
        object_type = 'transaction_input'
        object_type_human_read = 'transaction'
        original_filename = os.path.basename(file_path_in)[:128]
        duplicate_list = []
        duplicate_counter = 0


        desc = TransactionInputService.verify_transaction_order(df, total_number_transaction_inputs-1)
        if desc:
            start, stop, step = total_number_transaction_inputs-1, 0-1, -1
        else:
            start, stop, step = 0, total_number_transaction_inputs, 1

        # send status update via socket
        SocketService.emit_status_success(0, abs(stop-start), original_filename, object_type)

        for i in range(start, stop, step):
            print('in loop', i, flush=True)
            current = i + 1

            try:
                account_given_id, channel_code, given_id, activity_id, item_sku, shipment_date, arrival_date, complete_date = TransactionInputService.get_df_vars(df, i, current, object_type)
            except Exception as e:
                raise(e) #!!!!
                # if e.code == 422:
                #     SocketService.emit_status_error_column_read(current, object_type, column_name=e.description)
                # elif e.code == 417:
                #     SocketService.emit_status_error_no_value(current, object_type, e.description)
                # return False

            try:
                account = AccountService.get_by_given_id_channel_code(account_given_id, channel_code)
                print('account: {}, account_given_id: {}, channel_code: {}'.format(account, account_given_id, channel_code), flush=True)
            except:
                SocketService.emit_status_error_unidentifiable_object(object_type, 'account', current)
                return False

            try:
                item = ItemService.get_by_sku_account(item_sku, account)
            except:
                SocketService.emit_status_error_unidentifiable_object(object_type, 'item', current)
                return False

            bundle = BundleService.get_or_create(account.id, item.id, given_id)

            #!!!!
            print('account: {}, item: {}, bundle: {}'.format(account, item, bundle), flush=True)
            if account is None or item is None:
                raise
            #!!!!

            transaction_input = TransactionInputService.get_by_identifiers(account_given_id, channel_code, given_id, activity_id, item_sku)
            if transaction_input and transaction_input.processed:
                if not duplicate_counter > 2:
                    message = 'The transaction id: "{}" has already been processed. It has been skipped consequently'.format(given_id)
                    SocketService.emit_status_info(object_type, message)

                total -= 1
                duplicate_list.append(given_id)
                duplicate_counter +=1
                continue #skipping duplicates

            else:
                transaction_input_data = {
                    'created_by': user_id,
                    'bundle_id': bundle.id,
                    'original_filename': original_filename,

                    'seller_firm_id': account.seller_firm_id,

                    'account_id': account.id,
                    'account_given_id': account_given_id,
                    'public_activity_period': InputService.get_str(df, i, column='ACTIVITY_PERIOD'),
                    'channel_code': channel_code,
                    'marketplace': InputService.get_str_or_None(df, i, column='MARKETPLACE'),
                    'transaction_type_public_code': InputService.get_str_or_None(df, i, column='TRANSACTION_TYPE'),
                    'given_id': given_id,
                    'activity_id': activity_id,

                    'tax_calculation_date': InputService.get_date_or_None(df, i, column='TAX_CALCULATION_DATE'),
                    'shipment_date': shipment_date,
                    'arrival_date': arrival_date,
                    'complete_date': complete_date,

                    'item_id': item.id,
                    'item_sku': item_sku,
                    'item_name': InputService.get_str(df, i, column='ITEM_DESCRIPTION'),
                    'item_manufacture_country': InputService.get_str_or_None(df, i, column='ITEM_MANUFACTURE_COUNTRY'),
                    'item_quantity': int(df.iloc[i]['QTY']),
                    'item_weight_kg': InputService.get_float_or_None(df, i, column='ITEM_WEIGHT'),
                    'item_weight_kg_total': InputService.get_float_or_None(df, i, column='TOTAL_ACTIVITY_WEIGHT'),

                    'unit_cost_price_net': InputService.get_float_or_None(df, i, column='COST_PRICE_OF_ITEMS'),

                    'item_price_discount_net': InputService.get_float_or_None(df, i, column='PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL'),
                    'item_price_discount_vat': InputService.get_float_or_None(df, i, column='PROMO_PRICE_OF_ITEMS_VAT_AMT'),
                    'item_price_discount_gross': InputService.get_float_or_None(df, i, column='PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL'),

                    'item_price_net': InputService.get_float_or_None(df, i, column='PRICE_OF_ITEMS_AMT_VAT_EXCL'),
                    'item_price_vat': InputService.get_float_or_None(df, i, column='PRICE_OF_ITEMS_VAT_AMT'),
                    'item_price_gross': InputService.get_float_or_None(df, i, column='PRICE_OF_ITEMS_AMT_VAT_INCL'),

                    'item_price_total_net': InputService.get_float_or_None(df, i, column='TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL'),
                    'item_price_total_vat': InputService.get_float_or_None(df, i, column='TOTAL_PRICE_OF_ITEMS_VAT_AMT'),
                    'item_price_total_gross': InputService.get_float_or_None(df, i, column='TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL'),

                    'item_price_vat_rate': InputService.get_float_or_None(df, i, column='PRICE_OF_ITEMS_VAT_RATE_PERCENT'),

                    'shipment_price_discount_net': InputService.get_float_or_None(df, i, column='PROMO_SHIP_CHARGE_AMT_VAT_EXCL'),
                    'shipment_price_discount_vat': InputService.get_float_or_None(df, i, column='PROMO_SHIP_CHARGE_VAT_AMT'),
                    'shipment_price_discount_gross': InputService.get_float_or_None(df, i, column='PROMO_SHIP_CHARGE_AMT_VAT_INCL'),

                    'shipment_price_net': InputService.get_float_or_None(df, i, column='SHIP_CHARGE_AMT_VAT_EXCL'),
                    'shipment_price_vat': InputService.get_float_or_None(df, i, column='SHIP_CHARGE_VAT_AMT'),
                    'shipment_price_gross': InputService.get_float_or_None(df, i, column='SHIP_CHARGE_AMT_VAT_INCL'),

                    'shipment_price_total_net': InputService.get_float_or_None(df, i, column='TOTAL_SHIP_CHARGE_AMT_VAT_EXCL'),
                    'shipment_price_total_vat': InputService.get_float_or_None(df, i, column='TOTAL_SHIP_CHARGE_VAT_AMT'),
                    'shipment_price_total_gross': InputService.get_float_or_None(df, i, column='TOTAL_SHIP_CHARGE_AMT_VAT_INCL'),

                    'shipment_price_vat_rate': InputService.get_float_or_None(df, i, column='SHIP_CHARGE_VAT_RATE_PERCENT'),

                    'sale_total_value_net': InputService.get_float_or_None(df, i, column='TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL'),
                    'sale_total_value_vat': InputService.get_float_or_None(df, i, column='TOTAL_ACTIVITY_VALUE_VAT_AMT'),
                    'sale_total_value_gross': InputService.get_float_or_None(df, i, column='TOTAL_ACTIVITY_VALUE_AMT_VAT_INCL'),

                    'gift_wrap_price_discount_net': InputService.get_float_or_None(df, i, column='PROMO_GIFT_WRAP_AMT_VAT_EXCL'),
                    'gift_wrap_price_discount_vat': InputService.get_float_or_None(df, i, column='PROMO_GIFT_WRAP_VAT_AMT'),
                    'gift_wrap_price_discount_gross': InputService.get_float_or_None(df, i, column='PROMO_GIFT_WRAP_AMT_VAT_INCL'),

                    'gift_wrap_price_net': InputService.get_float_or_None(df, i, column='GIFT_WRAP_AMT_VAT_EXCL'),
                    'gift_wrap_price_vat': InputService.get_float_or_None(df, i, column='GIFT_WRAP_VAT_AMT'),
                    'gift_wrap_price_gross': InputService.get_float_or_None(df, i, column='GIFT_WRAP_AMT_VAT_INCL'),

                    'gift_wrap_price_total_net': InputService.get_float_or_None(df, i, column='TOTAL_GIFT_WRAP_AMT_VAT_EXCL'),
                    'gift_wrap_price_total_vat': InputService.get_float_or_None(df, i, column='TOTAL_GIFT_WRAP_VAT_AMT'),
                    'gift_wrap_price_total_gross': InputService.get_float_or_None(df, i, column='TOTAL_GIFT_WRAP_AMT_VAT_INCL'),

                    'gift_wrap_price_tax_rate': InputService.get_float_or_None(df, i, column='GIFT_WRAP_VAT_RATE_PERCENT'),


                    'currency_code': InputService.get_str_or_None(df, i, column='TRANSACTION_CURRENCY_CODE'),

                    'item_tax_code_code': InputService.get_str_or_None(df, i, column='PRODUCT_TAX_CODE'),


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

                    'departure_seller_vat_country_code': InputService.get_str_or_None(df, i, column='SELLER_DEPART_VAT_NUMBER_COUNTRY'),
                    'departure_seller_vat_number': InputService.get_str_or_None(df, i, column='SELLER_DEPART_COUNTRY_VAT_NUMBER'),

                    'arrival_seller_vat_country_code': InputService.get_str_or_None(df, i, column='SELLER_ARRIVAL_VAT_NUMBER_COUNTRY'),
                    'arrival_seller_vat_number': InputService.get_str_or_None(df, i, column='SELLER_ARRIVAL_COUNTRY_VAT_NUMBER'),

                    'seller_vat_country_code': InputService.get_str_or_None(df, i, column='TRANSACTION_SELLER_VAT_NUMBER_COUNTRY'),
                    'seller_vat_number': InputService.get_str_or_None(df, i, column='TRANSACTION_SELLER_VAT_NUMBER'),


                    'tax_calculation_imputation_country': InputService.get_str_or_None(df, i, column='VAT_CALCULATION_IMPUTATION_COUNTRY'),
                    'tax_jurisdiction': InputService.get_str_or_None(df, i, column='TAXABLE_JURISDICTION'),
                    'tax_jurisdiction_level': InputService.get_str_or_None(df, i, column='TAXABLE_JURISDICTION_LEVEL'),

                    'invoice_number': InputService.get_str_or_None(df, i, column='VAT_INV_NUMBER'),
                    'invoice_amount_vat': InputService.get_float_or_None(df, i, column='VAT_INV_CONVERTED_AMT'),
                    'invoice_currency_code': InputService.get_str_or_None(df, i, column='VAT_INV_CURRENCY_CODE'),
                    'invoice_exchange_rate': InputService.get_float_or_None(df, i, column='VAT_INV_EXCHANGE_RATE'),
                    'invoice_exchange_rate_date': InputService.get_date_or_None(df, i, column='VAT_INV_EXCHANGE_RATE_DATE'),
                    'invoice_url': InputService.get_str_or_None(df, i, column='INVOICE_URL'),


                    'export': InputService.get_bool(df, i, column='EXPORT_OUTSIDE_EU', value_true='YES'),

                    'customer_name': InputService.get_str_or_None(df, i, column='BUYER_NAME'),
                    'customer_vat_number': InputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER'),
                    'customer_vat_number_country_code': InputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER_COUNTRY'),

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
                            # send error status via socket
                            message = 'Error while updating {} with id: {} in row {} (file: {}). Please get in touch with one of the admins.'.format(object_type_human_read, given_id, current+1, original_filename)
                            SocketService.emit_status_error(object_type, message)
                            return False

                else:
                    # create new transaction input
                    try:
                        transaction_input = TransactionInputService.create_transaction_input(transaction_input_data)
                        transaction_inputs.append(transaction_input)
                    except:
                        db.session.rollback()
                        # send error status via socket
                        message = 'Error while updating {} with id: {} in row {} (file: {}). Please get in touch with one of the admins.'.format(object_type_human_read, given_id, current+1, original_filename)
                        SocketService.emit_status_error(object_type, message)
                        return False



                try:
                    # transactions are being created
                    TransactionInputService.process(transaction_input)
                except:
                    # send error status via socket
                    message = 'Error while processing {} with id: {} in row {} (file: {}). Please get in touch with one of the admins.'.format(object_type_human_read, given_id, current+1, original_filename)
                    SocketService.emit_status_error(object_type, message)
                    return False


                # send status update via socket
                SocketService.emit_status_success(abs(stop-current), abs(stop-start), original_filename, object_type)

        # update distance sale history
        last_transaction = TransactionService.get_latest_by_seller_firm_id(account.seller_firm_id)
        DistanceSaleService.update_taxable_turnover_amount_365d_all_ds(account.seller_firm_id, last_transaction.tax_date, original_filename)

        # following the successful processing, the vuex store is being reset !!! should be updated individually soon
        # first cleared
        SocketService.emit_clear_objects(object_type)
        # then refilled
        TransactionInputService.push_all_by_seller_firm_id(account.seller_firm_id, object_type)

        # send final status via socket
        SocketService.emit_status_final(total, original_filename, object_type, object_type_human_read, duplicate_list=duplicate_list)

        return True

    @staticmethod
    def process(transaction_input: TransactionInput):
        # transactions are being created
        if not transaction_input.processed:
            try:
                # create transactions
                TransactionService.create_transaction_s(transaction_input)
                transaction_input.update_processed()
                db.session.commit()

            except Exception as e:
                print(e, flush=True)
                db.session.rollback()
                raise




    @staticmethod
    def push_all_by_seller_firm_id(seller_firm_id: int, object_type: str) -> None:
        socket_list = []
        transaction_inputs = TransactionInputService.get_all_by_seller_firm_id(seller_firm_id)

        for transaction_input in transaction_inputs:
            # push transaction inputs to vuex via socket
            transaction_input_json = TransactionInputSubSchema.get_transaction_input_sub(transaction_input)
            socket_list.append(transaction_input_json)

        if len(socket_list) > 0:
            SocketService.emit_new_objects(socket_list, object_type)



    @staticmethod
    def create_transaction_input(transaction_input_data: TransactionInputInterface) -> TransactionInput:

        new_transaction_input = TransactionInput(
            created_by = transaction_input_data.get('created_by'),
            bundle_id = transaction_input_data.get('bundle_id'),
            original_filename = transaction_input_data.get('original_filename'),
            seller_firm_id=transaction_input_data.get('seller_firm_id'),
            account_id = transaction_input_data.get('account_id'),
            account_given_id = transaction_input_data.get('account_given_id'),
            public_activity_period = transaction_input_data.get('public_activity_period'),
            channel_code = transaction_input_data.get('channel_code'),
            marketplace = transaction_input_data.get('marketplace'),
            transaction_type_public_code = transaction_input_data.get('transaction_type_public_code'),
            given_id = transaction_input_data.get('given_id'),
            activity_id = transaction_input_data.get('activity_id'),
            tax_calculation_date = transaction_input_data.get('tax_calculation_date'),
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
            unit_cost_price_net = transaction_input_data.get('unit_cost_price_net'),
            item_price_discount_net = transaction_input_data.get('item_price_discount_net'),
            item_price_discount_vat = transaction_input_data.get('item_price_discount_vat'),
            item_price_discount_gross = transaction_input_data.get('item_price_discount_gross'),
            item_price_net = transaction_input_data.get('item_price_net'),
            item_price_vat = transaction_input_data.get('item_price_vat'),
            item_price_gross = transaction_input_data.get('item_price_gross'),
            item_price_total_net = transaction_input_data.get('item_price_total_net'),
            item_price_total_vat = transaction_input_data.get('item_price_total_vat'),
            item_price_total_gross = transaction_input_data.get('item_price_total_gross'),
            item_price_vat_rate = transaction_input_data.get('item_price_vat_rate'),
            shipment_price_discount_net = transaction_input_data.get('shipment_price_discount_net'),
            shipment_price_discount_vat = transaction_input_data.get('shipment_price_discount_vat'),
            shipment_price_discount_gross = transaction_input_data.get('shipment_price_discount_gross'),
            shipment_price_net = transaction_input_data.get('shipment_price_net'),
            shipment_price_vat = transaction_input_data.get('shipment_price_vat'),
            shipment_price_gross = transaction_input_data.get('shipment_price_gross'),
            shipment_price_total_net = transaction_input_data.get('shipment_price_total_net'),
            shipment_price_total_vat = transaction_input_data.get('shipment_price_total_vat'),
            shipment_price_total_gross = transaction_input_data.get('shipment_price_total_gross'),
            shipment_price_vat_rate = transaction_input_data.get('shipment_price_vat_rate'),
            sale_total_value_net = transaction_input_data.get('sale_total_value_net'),
            sale_total_value_vat = transaction_input_data.get('sale_total_value_vat'),
            sale_total_value_gross = transaction_input_data.get('sale_total_value_gross'),
            gift_wrap_price_discount_net = transaction_input_data.get('gift_wrap_price_discount_net'),
            gift_wrap_price_discount_vat = transaction_input_data.get('gift_wrap_price_discount_vat'),
            gift_wrap_price_discount_gross = transaction_input_data.get('gift_wrap_price_discount_gross'),
            gift_wrap_price_net = transaction_input_data.get('gift_wrap_price_net'),
            gift_wrap_price_vat = transaction_input_data.get('gift_wrap_price_vat'),
            gift_wrap_price_gross = transaction_input_data.get('gift_wrap_price_gross'),
            gift_wrap_price_total_net = transaction_input_data.get('gift_wrap_price_total_net'),
            gift_wrap_price_total_vat = transaction_input_data.get('gift_wrap_price_total_vat'),
            gift_wrap_price_total_gross = transaction_input_data.get('gift_wrap_price_total_gross'),
            gift_wrap_price_tax_rate = transaction_input_data.get('gift_wrap_price_tax_rate'),
            currency_code = transaction_input_data.get('currency_code'),
            item_tax_code_code = transaction_input_data.get('item_tax_code_code'),
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
            departure_seller_vat_country_code = transaction_input_data.get('departure_seller_vat_country_code'),
            departure_seller_vat_number = transaction_input_data.get('departure_seller_vat_number'),
            arrival_seller_vat_country_code = transaction_input_data.get('arrival_seller_vat_country_code'),
            arrival_seller_vat_number = transaction_input_data.get('arrival_seller_vat_number'),
            seller_vat_country_code = transaction_input_data.get('seller_vat_country_code'),
            seller_vat_number = transaction_input_data.get('seller_vat_number'),
            tax_calculation_imputation_country = transaction_input_data.get('tax_calculation_imputation_country'),
            tax_jurisdiction = transaction_input_data.get('tax_jurisdiction'),
            tax_jurisdiction_level = transaction_input_data.get('tax_jurisdiction_level'),
            invoice_number = transaction_input_data.get('invoice_number'),
            invoice_amount_vat = transaction_input_data.get('invoice_amount_vat'),
            invoice_currency_code = transaction_input_data.get('invoice_currency_code'),
            invoice_exchange_rate = transaction_input_data.get('invoice_exchange_rate'),
            invoice_exchange_rate_date = transaction_input_data.get('invoice_exchange_rate_date'),
            invoice_url = transaction_input_data.get('invoice_url'),
            export = transaction_input_data.get('export'),
            customer_name = transaction_input_data.get('customer_name'),
            customer_vat_number = transaction_input_data.get('customer_vat_number'),
            customer_vat_number_country_code = transaction_input_data.get('customer_vat_number_country_code'),
            supplier_vat_number = transaction_input_data.get('supplier_vat_number'),
            supplier_name = transaction_input_data.get('supplier_name')
        )


        db.session.add(new_transaction_input)
        db.session.commit()

        return new_transaction_input
