import os
from time import sleep
from statistics import mean
from datetime import datetime, date
import pandas as pd
from typing import List, BinaryIO, Dict

from flask import g, current_app
from sqlalchemy import or_
from werkzeug.exceptions import UnsupportedMediaType, NotFound, UnprocessableEntity, ExpectationFailed, InternalServerError
from app.extensions import (
    db,
    socket_io)

from . import TransactionInput
from .interface import TransactionInputInterface
from .schema import TransactionInputSubSchema

from app.namespaces.utils.service import InputService, NotificationService, HelperService
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
            return None
        else:
            bundle = BundleService.get_by_public_id(bundle_public_id)
        if isinstance(bundle, Bundle):
            return TransactionInput.query.filter_by(bundle_id=bundle.id).all()

    @staticmethod
    def get_all_by_seller_firm_id(seller_firm_id: int) -> List[TransactionInput]:
        return TransactionInput.query.filter_by(seller_firm_id=seller_firm_id).all()

    @staticmethod
    def get_all_by_seller_firm_id_limit(seller_firm_id: int, limit: int=50) -> List[TransactionInput]:
        return TransactionInput.query.filter_by(seller_firm_id=seller_firm_id).order_by(TransactionInput.complete_date.desc()).limit(50).all()

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
    def handle_transaction_input_data_upload(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: Dict, platform_code: str, data_retrieval: bool = False) -> Dict:
        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        original_filename = os.path.basename(file_path_in)[:128]
        if data_retrieval:
            TransactionInputService.update_by_transaction_report_data(df, platform_code, seller_firm_id, user_id, original_filename)
        response_object = TransactionInputService.create_transaction_inputs_and_transactions(df, original_filename, user_id, seller_firm_id, platform_code)
        tag = TagService.get_by_code('TRANSACTION')
        NotificationService.handle_seller_firm_notification_data_upload(seller_firm_id, user_id, tag, seller_firm_notification_data)
        InputService.move_file_to_out(file_path_in, basepath, file_type, business_id=seller_firm_id)

        return response_object



    @staticmethod
    def update_by_transaction_report_data(df: pd.DataFrame, platform_code: str, seller_firm_id: int, user_id: int, original_filename: str):
        from app.namespaces.item.service import ItemService

        valid_from: date = TransactionInputVariableService.get_valid_from_df(df, platform_code)

        # create/update accounts
        df_accounts = TransactionInputVariableService.get_unique_account_details_from_transaction_inputs_as_df(df, platform_code)
        TransactionInputVariableService.update_accounts(df_accounts, platform_code, seller_firm_id, user_id, original_filename)

        #create/update items
        df_items = TransactionInputVariableService.get_unique_item_details_from_transaction_inputs_as_df(df, platform_code)
        item_unit_cost_price_est: float = ItemService.get_unit_cost_price_net_est(seller_firm_id, df, platform_code, target_currency_code, exchange_rate_date)
        TransactionInputVariableService.update_items(df_items, platform_code, seller_firm_id, user_id, original_filename, valid_from, item_unit_cost_price_est)

        #create/update vatins
        unique_vatin_numbers = TransactionInputVariableService.get_unique_vatins_from_transaction_inputs(df, seller_firm_id, platform_code)
        TransactionInputVariableService.update_vatin_data(unique_vatin_numbers, valid_from, seller_firm_id, original_filename)


    @staticmethod
    def create_transaction_inputs_and_transactions(df: pd.DataFrame, original_filename: str, user_id: int, seller_firm_id: int, platform_code: str) -> List[Dict]:
        #!!! make this general and add amazon specific function in file read columns
        from app.namespaces.distance_sale.service import DistanceSaleService
        from app.namespaces.tax.tax_code.service import TaxCodeService
        from app.namespaces.account.service import AccountService
        from app.namespaces.item.service import ItemService
        from app.namespaces.account import Account
        from app.namespaces.item import Item

        error_counter = 0
        total = total_number_transaction_inputs = len(df.index)
        input_type = 'transaction' # only used for response objects
        transaction_inputs = []
        object_type = 'transaction_input'
        object_type_human_read = 'transaction'
        duplicate_list = []
        duplicate_counter = 0

        start, stop, step = TransactionInputVariableService.verify_transaction_order(df, total_number_transaction_inputs-1, platform_code)

        # send status update via socket
        SocketService.emit_status_success(0, total_number_transaction_inputs, original_filename, object_type)



        for i in range(start, stop, step):
            current = start - i + 1 if desc else i + 1

            try:
                #retrieve all relevant vars
                (
                    account_given_id,
                    channel_code,
                    given_id,
                    activity_id,
                    item_sku,
                    item_name,
                    item_brand_name,
                    item_asin,
                    shipment_date,
                    arrival_date,
                    complete_date,
                    public_activity_period,
                    marketplace,
                    transaction_type_public_code,
                    tax_calculation_date,
                    item_manufacture_country,
                    item_quantity,
                    item_weight_kg,
                    item_weight_kg_total,
                    unit_cost_price_net,
                    item_price_discount_net,
                    item_price_discount_vat,
                    item_price_discount_gross,
                    item_price_net,
                    item_price_vat,
                    item_price_gross,
                    item_price_total_net,
                    item_price_total_vat,
                    item_price_total_gross,
                    item_price_vat_rate,
                    shipment_price_discount_net,
                    shipment_price_discount_vat,
                    shipment_price_discount_gross,
                    shipment_price_net,
                    shipment_price_vat,
                    shipment_price_gross,
                    shipment_price_total_net,
                    shipment_price_total_vat,
                    shipment_price_total_gross,
                    shipment_price_vat_rate,
                    sale_total_value_net,
                    sale_total_value_vat,
                    sale_total_value_gross,
                    gift_wrap_price_discount_net,
                    gift_wrap_price_discount_vat,
                    gift_wrap_price_discount_gross,
                    gift_wrap_price_net,
                    gift_wrap_price_vat,
                    gift_wrap_price_gross,
                    gift_wrap_price_total_net,
                    gift_wrap_price_total_vat,
                    gift_wrap_price_total_gross,
                    gift_wrap_price_tax_rate,
                    currency_code,
                    item_given_tax_code_code,
                    departure_country_code,
                    departure_postal_code,
                    departure_city,
                    arrival_country_code,
                    arrival_postal_code,
                    arrival_city,
                    arrival_address,
                    sale_departure_country_code,
                    sale_arrival_country_code,
                    shipment_mode,
                    shipment_conditions,
                    departure_seller_vat_country_code,
                    departure_seller_vat_number,
                    arrival_seller_vat_country_code,
                    arrival_seller_vat_number,
                    seller_vat_country_code,
                    seller_vat_number,
                    tax_calculation_imputation_country,
                    tax_jurisdiction,
                    tax_jurisdiction_level,
                    invoice_number,
                    invoice_amount_vat,
                    invoice_currency_code,
                    invoice_exchange_rate,
                    invoice_exchange_rate_date,
                    invoice_url,
                    export,
                    customer_name,
                    customer_vat_number,
                    customer_vat_number_country_code,
                    supplier_vat_number,
                    supplier_name
                ) = TransactionInputVariableService.get_df_vars(df, i, current, object_type, platform_code)

            except Exception as e:
                if e.code == 422:
                    SocketService.emit_status_error_column_read(current, object_type, column_name=e.description)
                elif e.code == 417:
                    SocketService.emit_status_error_no_value(current, object_type, e.description)
                return False

            item_tax_code = TaxCodeService.get_tax_code_code(item_given_tax_code_code, platform_code)
            valid_from = HelperService.get_earliest_date(shipment_date, arrival_date, complete_date, tax_calculation_date, invoice_exchange_rate_date)

            account = AccountService.get_by_given_id_channel_code(account_given_id, channel_code)
            if not isinstance(account, Account):
                SocketService.emit_status_error_unidentifiable_object(object_type, 'account', current)
                return False
            account_id = account.id

            item = ItemService.get_by_identifiers_seller_firm_id(item_sku, item_asin, seller_firm_id)
            if not isinstance(item, Item):
                SocketService.emit_status_error_unidentifiable_object(object_type, 'item', current)
                return False
            item_id = item.id

            bundle = BundleService.get_or_create(account_id, item_id, given_id)

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

                    'seller_firm_id': seller_firm_id,

                    'account_id': account_id,
                    'account_given_id': account_given_id,
                    'public_activity_period': public_activity_period,
                    'channel_code': channel_code,
                    'marketplace': marketplace,
                    'transaction_type_public_code': transaction_type_public_code,
                    'given_id': given_id,
                    'activity_id': activity_id,

                    'tax_calculation_date': tax_calculation_date,
                    'shipment_date': shipment_date,
                    'arrival_date': arrival_date,
                    'complete_date': complete_date,

                    'item_id': item_id,
                    'item_asin': item_asin,
                    'item_sku': item_sku,
                    'item_name': item_name,
                    'item_manufacture_country': item_manufacture_country,
                    'item_quantity': item_quantity,
                    'item_unit_cost_price_est': item_unit_cost_price_est,
                    'item_weight_kg': item_weight_kg,
                    'item_weight_kg_total': item_weight_kg_total,

                    'unit_cost_price_net': unit_cost_price_net,

                    'item_price_discount_net': item_price_discount_net,
                    'item_price_discount_vat': item_price_discount_vat,
                    'item_price_discount_gross': item_price_discount_gross,

                    'item_price_net': item_price_net,
                    'item_price_vat': item_price_vat,
                    'item_price_gross': item_price_gross,

                    'item_price_total_net': item_price_total_net,
                    'item_price_total_vat': item_price_total_vat,
                    'item_price_total_gross': item_price_total_gross,

                    'item_price_vat_rate': item_price_vat_rate,

                    'shipment_price_discount_net': shipment_price_discount_net,
                    'shipment_price_discount_vat': shipment_price_discount_vat,
                    'shipment_price_discount_gross': shipment_price_discount_gross,

                    'shipment_price_net': shipment_price_net,
                    'shipment_price_vat': shipment_price_vat,
                    'shipment_price_gross': shipment_price_gross,

                    'shipment_price_total_net': shipment_price_total_net,
                    'shipment_price_total_vat': shipment_price_total_vat,
                    'shipment_price_total_gross': shipment_price_total_gross,

                    'shipment_price_vat_rate': shipment_price_vat_rate,

                    'sale_total_value_net': sale_total_value_net,
                    'sale_total_value_vat': sale_total_value_vat,
                    'sale_total_value_gross': sale_total_value_gross,

                    'gift_wrap_price_discount_net': gift_wrap_price_discount_net,
                    'gift_wrap_price_discount_vat': gift_wrap_price_discount_vat,
                    'gift_wrap_price_discount_gross': gift_wrap_price_discount_gross,

                    'gift_wrap_price_net': gift_wrap_price_net,
                    'gift_wrap_price_vat': gift_wrap_price_vat,
                    'gift_wrap_price_gross': gift_wrap_price_gross,

                    'gift_wrap_price_total_net': gift_wrap_price_total_net,
                    'gift_wrap_price_total_vat': gift_wrap_price_total_vat,
                    'gift_wrap_price_total_gross': gift_wrap_price_total_gross,

                    'gift_wrap_price_tax_rate': gift_wrap_price_tax_rate,


                    'currency_code': currency_code,

                    'item_given_tax_code_code': item_given_tax_code_code,


                    'departure_country_code': departure_country_code,
                    'departure_postal_code': departure_postal_code,
                    'departure_city': departure_city,

                    'arrival_country_code': arrival_country_code,
                    'arrival_postal_code': arrival_postal_code,
                    'arrival_city': arrival_city,
                    'arrival_address': arrival_address,

                    'sale_departure_country_code': sale_departure_country_code,
                    'sale_arrival_country_code': sale_arrival_country_code,

                    'shipment_mode': shipment_mode,
                    'shipment_conditions': shipment_conditions,

                    'departure_seller_vat_country_code': departure_seller_vat_country_code,
                    'departure_seller_vat_number': departure_seller_vat_number,

                    'arrival_seller_vat_country_code': arrival_seller_vat_country_code,
                    'arrival_seller_vat_number': arrival_seller_vat_number,

                    'seller_vat_country_code': seller_vat_country_code,
                    'seller_vat_number': seller_vat_number,


                    'tax_calculation_imputation_country': tax_calculation_imputation_country,
                    'tax_jurisdiction': tax_jurisdiction,
                    'tax_jurisdiction_level': tax_jurisdiction_level,

                    'invoice_number': invoice_number,
                    'invoice_amount_vat': invoice_amount_vat,
                    'invoice_currency_code': invoice_currency_code,
                    'invoice_exchange_rate': invoice_exchange_rate,
                    'invoice_exchange_rate_date': invoice_exchange_rate_date,
                    'invoice_url': invoice_url,


                    'export': export,

                    'customer_name': customer_name,
                    'customer_vat_number': customer_vat_number,
                    'customer_vat_number_country_code': customer_vat_number_country_code,

                    'supplier_vat_number': supplier_vat_number,
                    'supplier_name': supplier_name
                }

                if transaction_input and not transaction_input.processed:
                    # update transaction_input
                    data_changes = {k:v for k,v in transaction_input_data.items() if v is not None}
                    if data_changes != {}:
                        try:
                            transaction_input.update(data_changes)
                            transaction_input.transactions = []
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            print(e, flush=True)
                            # send error status via socket
                            message = 'Error while updating {} with id: {} in row {} (file: {}). Please get in touch with one of the admins.'.format(object_type_human_read, given_id, current+1, original_filename)
                            SocketService.emit_status_error(object_type, message)
                            return False

                else:
                    # create new transaction input
                    try:
                        transaction_input = TransactionInputService.create_transaction_input(transaction_input_data)
                        transaction_inputs.append(transaction_input)
                    except Exception as e:
                        print(e, flush=True)
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
                SocketService.emit_status_success(current, total_number_transaction_inputs,  original_filename, object_type)

        # update distance sale history
        last_transaction = TransactionService.get_latest_by_seller_firm_id(seller_firm_id)
        DistanceSaleService.update_taxable_turnover_amount_365d_all_ds(seller_firm_id, last_transaction.tax_date, original_filename)

        # following the successful processing, the vuex store is being reset !!! should be updated individually soon
        # first cleared
        SocketService.emit_clear_objects(object_type)
        # then refilled
        TransactionInputService.push_all_by_seller_firm_id(seller_firm_id, object_type)

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
        transaction_inputs = TransactionInputService.get_all_by_seller_firm_id_limit(seller_firm_id)

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
            item_asin=transaction_input_data.get('item_asin'),
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
            item_given_tax_code_code = transaction_input_data.get('item_given_tax_code_code'),
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


class TransactionInputVariableService:


    @staticmethod
    def verify_transaction_order(df: pd.DataFrame, total: int, platform_code: str) -> int, int, int:
        if platform_code == 'AMZ':
            desc = TransactionInputVariableService.verify_transaction_order_AMZ(df, total)

        # general/platform-independent
        if desc:
            start, stop, step = total_number_transaction_inputs-1, 0-1, -1
        else:
            start, stop, step = 0, total_number_transaction_inputs, 1

        return start, stop, step

    @staticmethod
    def verify_transaction_order_AMZ(df, total) -> bool:
        complete_date_top = InputService.get_date_or_None(df, 0, column='TRANSACTION_COMPLETE_DATE')
        complete_date_bottom = InputService.get_date_or_None(df, total, column='TRANSACTION_COMPLETE_DATE')

        return complete_date_top >= complete_date_bottom


    @staticmethod
    def get_df_vars(df: pd.DataFrame, i: int, current: int, object_type: str, platform_code: str) -> List:
        if platform_code == 'AMZ':
            return TransactionInputVariableService.get_df_vars_AMZ(df, i, current, object_type)


    @staticmethod
    def get_item_vars_AMZ(df_items: pd.DataFrame, i: int):
        try:
            item_sku = InputService.get_str(df, i, column='SELLER_SKU')
        except:
            raise UnprocessableEntity('SELLER_SKU')

        try:
            item_name = InputService.get_str_or_None(df, i, column='ITEM_DESCRIPTION')
        except:
            raise UnprocessableEntity('ITEM_DESCRIPTION')

        try:
            item_asin = InputService.get_str_or_None(df, i, column='ASIN')
        except:
            raise UnprocessableEntity('ASIN')

        try:
            item_weight_kg = InputService.get_float_or_None(df, i, column='ITEM_WEIGHT')
        except:
            raise UnprocessableEntity('ITEM_WEIGHT')

        try:
            item_given_tax_code_code = InputService.get_str_or_None(df, i, column='PRODUCT_TAX_CODE')
        except:
            raise UnprocessableEntity('PRODUCT_TAX_CODE')

        return item_sku, item_name, item_asin, item_weight_kg, item_given_tax_code_code


    @staticmethod
    def get_df_vars_AMZ(df: pd.DataFrame, i: int, current: int, object_type: str) -> List:

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
            item_name = InputService.get_str_or_None(df, i, column='ITEM_DESCRIPTION')
        except:
            raise UnprocessableEntity('ITEM_DESCRIPTION')

        try:
            item_asin = InputService.get_str_or_None(df, i, column='ASIN')
        except:
            raise UnprocessableEntity('ASIN')

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


        try:
            public_activity_period = InputService.get_str(df, i, column='ACTIVITY_PERIOD')
        except:
            raise UnprocessableEntity('ACTIVITY_PERIOD')
        try:
            marketplace = InputService.get_str_or_None(df, i, column='MARKETPLACE')
        except:
            raise UnprocessableEntity('MARKETPLACE')
        try:
            transaction_type_public_code = InputService.get_str_or_None(df, i, column='TRANSACTION_TYPE')
        except:
            raise UnprocessableEntity('TRANSACTION_TYPE')

        try:
            tax_calculation_date = InputService.get_date_or_None(df, i, column='TAX_CALCULATION_DATE')
        except:
            raise UnprocessableEntity('TAX_CALCULATION_DATE')

        try:
            item_manufacture_country = InputService.get_str_or_None(df, i, column='ITEM_MANUFACTURE_COUNTRY')
        except:
            raise UnprocessableEntity('ITEM_MANUFACTURE_COUNTRY')
        try:
            item_quantity = int(df.iloc[i]['QTY'])
        except:
            raise UnprocessableEntity('QTY')

        try:
            item_weight_kg = InputService.get_float_or_None(df, i, column='ITEM_WEIGHT')
        except:
            raise UnprocessableEntity('ITEM_WEIGHT')
        try:
            item_weight_kg_total = InputService.get_float_or_None(df, i, column='TOTAL_ACTIVITY_WEIGHT')
        except:
            raise UnprocessableEntity('TOTAL_ACTIVITY_WEIGHT')

        try:
            unit_cost_price_net = InputService.get_float_or_None(df, i, column='COST_PRICE_OF_ITEMS')
        except:
            raise UnprocessableEntity('COST_PRICE_OF_ITEMS')

        try:
            item_price_discount_net = InputService.get_float_or_None(df, i, column='PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL')
        except:
            raise UnprocessableEntity('PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL')
        try:
            item_price_discount_vat = InputService.get_float_or_None(df, i, column='PROMO_PRICE_OF_ITEMS_VAT_AMT')
        except:
            raise UnprocessableEntity('PROMO_PRICE_OF_ITEMS_VAT_AMT')
        try:
            item_price_discount_gross = InputService.get_float_or_None(df, i, column='PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL')
        except:
            raise UnprocessableEntity('PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL')

        try:
            item_price_net = InputService.get_float_or_None(df, i, column='PRICE_OF_ITEMS_AMT_VAT_EXCL')
        except:
            raise UnprocessableEntity('PRICE_OF_ITEMS_AMT_VAT_EXCL')
        try:
            item_price_vat = InputService.get_float_or_None(df, i, column='PRICE_OF_ITEMS_VAT_AMT')
        except:
            raise UnprocessableEntity('PRICE_OF_ITEMS_VAT_AMT')
        try:
            item_price_gross = InputService.get_float_or_None(df, i, column='PRICE_OF_ITEMS_AMT_VAT_INCL')
        except:
            raise UnprocessableEntity('PRICE_OF_ITEMS_AMT_VAT_INCL')

        try:
            item_price_total_net = InputService.get_float_or_None(df, i, column='TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL')
        except:
            raise UnprocessableEntity('TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL')
        try:
            item_price_total_vat = InputService.get_float_or_None(df, i, column='TOTAL_PRICE_OF_ITEMS_VAT_AMT')
        except:
            raise UnprocessableEntity('TOTAL_PRICE_OF_ITEMS_VAT_AMT')
        try:
            item_price_total_gross = InputService.get_float_or_None(df, i, column='TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL')
        except:
            raise UnprocessableEntity('TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL')

        try:
            item_price_vat_rate = InputService.get_float_or_None(df, i, column='PRICE_OF_ITEMS_VAT_RATE_PERCENT')
        except:
            raise UnprocessableEntity('PRICE_OF_ITEMS_VAT_RATE_PERCENT')

        try:
            shipment_price_discount_net = InputService.get_float_or_None(df, i, column='PROMO_SHIP_CHARGE_AMT_VAT_EXCL')
        except:
            raise UnprocessableEntity('PROMO_SHIP_CHARGE_AMT_VAT_EXCL')
        try:
            shipment_price_discount_vat = InputService.get_float_or_None(df, i, column='PROMO_SHIP_CHARGE_VAT_AMT')
        except:
            raise UnprocessableEntity('PROMO_SHIP_CHARGE_VAT_AMT')
        try:
            shipment_price_discount_gross = InputService.get_float_or_None(df, i, column='PROMO_SHIP_CHARGE_AMT_VAT_INCL')
        except:
            raise UnprocessableEntity('PROMO_SHIP_CHARGE_AMT_VAT_INCL')

        try:
            shipment_price_net = InputService.get_float_or_None(df, i, column='SHIP_CHARGE_AMT_VAT_EXCL')
        except:
            raise UnprocessableEntity('SHIP_CHARGE_AMT_VAT_EXCL')
        try:
            shipment_price_vat = InputService.get_float_or_None(df, i, column='SHIP_CHARGE_VAT_AMT')
        except:
            raise UnprocessableEntity('SHIP_CHARGE_VAT_AMT')
        try:
            shipment_price_gross = InputService.get_float_or_None(df, i, column='SHIP_CHARGE_AMT_VAT_INCL')
        except:
            raise UnprocessableEntity('SHIP_CHARGE_AMT_VAT_INCL')

        try:
            shipment_price_total_net = InputService.get_float_or_None(df, i, column='TOTAL_SHIP_CHARGE_AMT_VAT_EXCL')
        except:
            raise UnprocessableEntity('TOTAL_SHIP_CHARGE_AMT_VAT_EXCL')
        try:
            shipment_price_total_vat = InputService.get_float_or_None(df, i, column='TOTAL_SHIP_CHARGE_VAT_AMT')
        except:
            raise UnprocessableEntity('TOTAL_SHIP_CHARGE_VAT_AMT')
        try:
            shipment_price_total_gross = InputService.get_float_or_None(df, i, column='TOTAL_SHIP_CHARGE_AMT_VAT_INCL')
        except:
            raise UnprocessableEntity('TOTAL_SHIP_CHARGE_AMT_VAT_INCL')

        try:
            shipment_price_vat_rate = InputService.get_float_or_None(df, i, column='SHIP_CHARGE_VAT_RATE_PERCENT')
        except:
            raise UnprocessableEntity('SHIP_CHARGE_VAT_RATE_PERCENT')

        try:
            sale_total_value_net = InputService.get_float_or_None(df, i, column='TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL')
        except:
            raise UnprocessableEntity('TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL')
        try:
            sale_total_value_vat = InputService.get_float_or_None(df, i, column='TOTAL_ACTIVITY_VALUE_VAT_AMT')
        except:
            raise UnprocessableEntity('TOTAL_ACTIVITY_VALUE_VAT_AMT')
        try:
            sale_total_value_gross = InputService.get_float_or_None(df, i, column='TOTAL_ACTIVITY_VALUE_AMT_VAT_INCL')
        except:
            raise UnprocessableEntity('TOTAL_ACTIVITY_VALUE_AMT_VAT_INCL')

        try:
            gift_wrap_price_discount_net = InputService.get_float_or_None(df, i, column='PROMO_GIFT_WRAP_AMT_VAT_EXCL')
        except:
            raise UnprocessableEntity('PROMO_GIFT_WRAP_AMT_VAT_EXCL')
        try:
            gift_wrap_price_discount_vat = InputService.get_float_or_None(df, i, column='PROMO_GIFT_WRAP_VAT_AMT')
        except:
            raise UnprocessableEntity('PROMO_GIFT_WRAP_VAT_AMT')
        try:
            gift_wrap_price_discount_gross = InputService.get_float_or_None(df, i, column='PROMO_GIFT_WRAP_AMT_VAT_INCL')
        except:
            raise UnprocessableEntity('PROMO_GIFT_WRAP_AMT_VAT_INCL')

        try:
            gift_wrap_price_net = InputService.get_float_or_None(df, i, column='GIFT_WRAP_AMT_VAT_EXCL')
        except:
            raise UnprocessableEntity('GIFT_WRAP_AMT_VAT_EXCL')
        try:
            gift_wrap_price_vat = InputService.get_float_or_None(df, i, column='GIFT_WRAP_VAT_AMT')
        except:
            raise UnprocessableEntity('GIFT_WRAP_VAT_AMT')
        try:
            gift_wrap_price_gross = InputService.get_float_or_None(df, i, column='GIFT_WRAP_AMT_VAT_INCL')
        except:
            raise UnprocessableEntity('GIFT_WRAP_AMT_VAT_INCL')

        try:
            gift_wrap_price_total_net = InputService.get_float_or_None(df, i, column='TOTAL_GIFT_WRAP_AMT_VAT_EXCL')
        except:
            raise UnprocessableEntity('TOTAL_GIFT_WRAP_AMT_VAT_EXCL')
        try:
            gift_wrap_price_total_vat = InputService.get_float_or_None(df, i, column='TOTAL_GIFT_WRAP_VAT_AMT')
        except:
            raise UnprocessableEntity('TOTAL_GIFT_WRAP_VAT_AMT')
        try:
            gift_wrap_price_total_gross = InputService.get_float_or_None(df, i, column='TOTAL_GIFT_WRAP_AMT_VAT_INCL')
        except:
            raise UnprocessableEntity('TOTAL_GIFT_WRAP_AMT_VAT_INCL')

        try:
            gift_wrap_price_tax_rate = InputService.get_float_or_None(df, i, column='GIFT_WRAP_VAT_RATE_PERCENT')
        except:
            raise UnprocessableEntity('GIFT_WRAP_VAT_RATE_PERCENT')


        try:
            currency_code = InputService.get_str_or_None(df, i, column='TRANSACTION_CURRENCY_CODE')
        except:
            raise UnprocessableEntity('TRANSACTION_CURRENCY_CODE')

        try:
            item_given_tax_code_code = InputService.get_str_or_None(df, i, column='PRODUCT_TAX_CODE')
        except:
            raise UnprocessableEntity('PRODUCT_TAX_CODE')


        try:
            departure_country_code = InputService.get_str_or_None(df, i, column='DEPARTURE_COUNTRY')
        except:
            raise UnprocessableEntity('DEPARTURE_COUNTRY')
        try:
            departure_postal_code = InputService.get_single_str_compact(df, i, column='DEPARTURE_POST_CODE')
        except:
            raise UnprocessableEntity('DEPARTURE_POST_CODE')
        try:
            departure_city = InputService.get_str_or_None(df, i, column='DEPATURE_CITY')
        except:
            raise UnprocessableEntity('DEPATURE_CITY')

        try:
            arrival_country_code = InputService.get_str_or_None(df, i, column='ARRIVAL_COUNTRY')
        except:
            raise UnprocessableEntity('ARRIVAL_COUNTRY')
        try:
            arrival_postal_code = InputService.get_single_str_compact(df, i, column='ARRIVAL_POST_CODE')
        except:
            raise UnprocessableEntity('ARRIVAL_POST_CODE')
        try:
            arrival_city = InputService.get_str_or_None(df, i, column='ARRIVAL_CITY')
        except:
            raise UnprocessableEntity('ARRIVAL_CITY')
        try:
            arrival_address = InputService.get_str_or_None(df, i, column='ARRIVAL_ADDRESS')
        except:
            raise UnprocessableEntity('ARRIVAL_ADDRESS')

        try:
            sale_departure_country_code = InputService.get_str_or_None(df, i, column='SALE_DEPART_COUNTRY')
        except:
            raise UnprocessableEntity('SALE_DEPART_COUNTRY')
        try:
            sale_arrival_country_code = InputService.get_str_or_None(df, i, column='SALE_ARRIVAL_COUNTRY')
        except:
            raise UnprocessableEntity('SALE_ARRIVAL_COUNTRY')

        try:
            shipment_mode = InputService.get_str_or_None(df, i, column='TRANSPORTATION_MODE')
        except:
            raise UnprocessableEntity('TRANSPORTATION_MODE')
        try:
            shipment_conditions = InputService.get_str_or_None(df, i, column='DELIVERY_CONDITIONS')
        except:
            raise UnprocessableEntity('DELIVERY_CONDITIONS')

        try:
            departure_seller_vat_country_code = InputService.get_str_or_None(df, i, column='SELLER_DEPART_VAT_NUMBER_COUNTRY')
        except:
            raise UnprocessableEntity('SELLER_DEPART_VAT_NUMBER_COUNTRY')
        try:
            departure_seller_vat_number = InputService.get_str_or_None(df, i, column='SELLER_DEPART_COUNTRY_VAT_NUMBER')
        except:
            raise UnprocessableEntity('SELLER_DEPART_COUNTRY_VAT_NUMBER')

        try:
            arrival_seller_vat_country_code = InputService.get_str_or_None(df, i, column='SELLER_ARRIVAL_VAT_NUMBER_COUNTRY')
        except:
            raise UnprocessableEntity('SELLER_ARRIVAL_VAT_NUMBER_COUNTRY')
        try:
            arrival_seller_vat_number = InputService.get_str_or_None(df, i, column='SELLER_ARRIVAL_COUNTRY_VAT_NUMBER')
        except:
            raise UnprocessableEntity('SELLER_ARRIVAL_COUNTRY_VAT_NUMBER')

        try:
            seller_vat_country_code = InputService.get_str_or_None(df, i, column='TRANSACTION_SELLER_VAT_NUMBER_COUNTRY')
        except:
            raise UnprocessableEntity('TRANSACTION_SELLER_VAT_NUMBER_COUNTRY')
        try:
            seller_vat_number = InputService.get_str_or_None(df, i, column='TRANSACTION_SELLER_VAT_NUMBER')
        except:
            raise UnprocessableEntity('TRANSACTION_SELLER_VAT_NUMBER')


        try:
            tax_calculation_imputation_country = InputService.get_str_or_None(df, i, column='VAT_CALCULATION_IMPUTATION_COUNTRY')
        except:
            raise UnprocessableEntity('VAT_CALCULATION_IMPUTATION_COUNTRY')
        try:
            tax_jurisdiction = InputService.get_str_or_None(df, i, column='TAXABLE_JURISDICTION')
        except:
            raise UnprocessableEntity('TAXABLE_JURISDICTION')
        try:
            tax_jurisdiction_level = InputService.get_str_or_None(df, i, column='TAXABLE_JURISDICTION_LEVEL')
        except:
            raise UnprocessableEntity('TAXABLE_JURISDICTION_LEVEL')

        try:
            invoice_number = InputService.get_str_or_None(df, i, column='VAT_INV_NUMBER')
        except:
            raise UnprocessableEntity('VAT_INV_NUMBER')
        try:
            invoice_amount_vat = InputService.get_float_or_None(df, i, column='VAT_INV_CONVERTED_AMT')
        except:
            raise UnprocessableEntity('VAT_INV_CONVERTED_AMT')
        try:
            invoice_currency_code = InputService.get_str_or_None(df, i, column='VAT_INV_CURRENCY_CODE')
        except:
            raise UnprocessableEntity('VAT_INV_CURRENCY_CODE')
        try:
            invoice_exchange_rate = InputService.get_float_or_None(df, i, column='VAT_INV_EXCHANGE_RATE')
        except:
            raise UnprocessableEntity('VAT_INV_EXCHANGE_RATE')
        try:
            invoice_exchange_rate_date = InputService.get_date_or_None(df, i, column='VAT_INV_EXCHANGE_RATE_DATE')
        except:
            raise UnprocessableEntity('VAT_INV_EXCHANGE_RATE_DATE')
        try:
            invoice_url = InputService.get_str_or_None(df, i, column='INVOICE_URL')
        except:
            raise UnprocessableEntity('INVOICE_URL')


        try:
            export = InputService.get_bool(df, i, column='EXPORT_OUTSIDE_EU', value_true='YES')
        except:
            raise UnprocessableEntity('EXPORT_OUTSIDE_EU')

        try:
            customer_name = InputService.get_str_or_None(df, i, column='BUYER_NAME')
        except:
            raise UnprocessableEntity('BUYER_NAME')
        try:
            customer_vat_number = InputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER')
        except:
            raise UnprocessableEntity('BUYER_VAT_NUMBER')
        try:
            customer_vat_number_country_code = InputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER_COUNTRY')
        except:
            raise UnprocessableEntity('BUYER_VAT_NUMBER_COUNTRY')

        try:
            supplier_vat_number = InputService.get_str_or_None(df, i, column='SUPPLIER_VAT_NUMBER')
        except:
            raise UnprocessableEntity('SUPPLIER_VAT_NUMBER')
        try:
            supplier_name = InputService.get_str_or_None(df, i, column='SUPPLIER_NAME')
        except:
            raise UnprocessableEntity('SUPPLIER_NAME')


        #unprovided vars
        item_brand_name = None

        return (
            account_given_id,
            channel_code,
            given_id,
            activity_id,
            item_sku,
            item_name,
            item_brand_name,
            item_asin,
            shipment_date,
            arrival_date,
            complete_date,
            public_activity_period,
            marketplace,
            transaction_type_public_code,
            tax_calculation_date,
            item_manufacture_country,
            item_quantity,
            item_weight_kg,
            item_weight_kg_total,
            unit_cost_price_net,
            item_price_discount_net,
            item_price_discount_vat,
            item_price_discount_gross,
            item_price_net,
            item_price_vat,
            item_price_gross,
            item_price_total_net,
            item_price_total_vat,
            item_price_total_gross,
            item_price_vat_rate,
            shipment_price_discount_net,
            shipment_price_discount_vat,
            shipment_price_discount_gross,
            shipment_price_net,
            shipment_price_vat,
            shipment_price_gross,
            shipment_price_total_net,
            shipment_price_total_vat,
            shipment_price_total_gross,
            shipment_price_vat_rate,
            sale_total_value_net,
            sale_total_value_vat,
            sale_total_value_gross,
            gift_wrap_price_discount_net,
            gift_wrap_price_discount_vat,
            gift_wrap_price_discount_gross,
            gift_wrap_price_net,
            gift_wrap_price_vat,
            gift_wrap_price_gross,
            gift_wrap_price_total_net,
            gift_wrap_price_total_vat,
            gift_wrap_price_total_gross,
            gift_wrap_price_tax_rate,
            currency_code,
            item_given_tax_code_code,
            departure_country_code,
            departure_postal_code,
            departure_city,
            arrival_country_code,
            arrival_postal_code,
            arrival_city,
            arrival_address,
            sale_departure_country_code,
            sale_arrival_country_code,
            shipment_mode,
            shipment_conditions,
            departure_seller_vat_country_code,
            departure_seller_vat_number,
            arrival_seller_vat_country_code,
            arrival_seller_vat_number,
            seller_vat_country_code,
            seller_vat_number,
            tax_calculation_imputation_country,
            tax_jurisdiction,
            tax_jurisdiction_level,
            invoice_number,
            invoice_amount_vat,
            invoice_currency_code,
            invoice_exchange_rate,
            invoice_exchange_rate_date,
            invoice_url,
            export,
            customer_name,
            customer_vat_number,
            customer_vat_number_country_code,
            supplier_vat_number,
            supplier_name
        )


    @staticmethod
    def update_accounts(df_accounts: pd.DataFrame, platform_code: str, seller_firm_id: int, user_id: int, original_filename: str):
        from app.namespaces.account import Account
        from app.namespaces.account.service import AccountService
        from app.namespaces.account.schema import AccountSubSchema

        for i in range(len(df_accounts.index)):
            if platform_code == 'AMZ':
                try:
                    account_given_id = InputService.get_str(df, i, column='UNIQUE_ACCOUNT_IDENTIFIER')
                except:
                    raise UnprocessableEntity('UNIQUE_ACCOUNT_IDENTIFIER')

                try:
                    channel_code = InputService.get_str(df, i, column='SALES_CHANNEL')
                except:
                    raise UnprocessableEntity('SALES_CHANNEL')

            # platform independent
            account = AccountService.get_by_given_id_channel_code(account_given_id, channel_code)
            if not isinstance(account, Account):
                account_data = {
                    'created_by': user_id,
                    'original_filename': original_filename,
                    'seller_firm_id': seller_firm_id,
                    'given_id': account_given_id,
                    'channel_code': channel_code
                }
                try:
                    account = AccountService.create(account_data)
                except Exception as e:
                    db.session.rollback()
                    SocketService.emit_status_error_unidentifiable_object(object_type, 'account', current)

                    raise InternalServerError(e)


                # push account to vuex via socket
                account_json = AccountSubSchema.get_account_sub(account)
                SocketService.emit_new_object(account_json, 'account')

            elif isinstance(account, Account) and account.seller_firm_id != seller_firm_id
                # Socket notification !!!!
                SocketService.emit_status_error_unidentifiable_object(object_type, 'account', current)



    @staticmethod
    def update_items(df_items: pd.DataFrame, platform_code: str, seller_firm_id: int, user_id: int, original_filename: str, valid_from: date, unit_cost_price_net_est: float):
        from app.namespaces.item import Item
        from app.namespaces.item.service import ItemService, ItemHistoryService
        from app.namespaces.item.schema import ItemSubSchema
        from app.namespaces.tax.tax_code.service import TaxCodeService

        for i in range(len(df_items.index)):
            if platform_code == 'AMZ':
                (
                    item_sku,
                    item_name,
                    item_asin,
                    item_weight_kg,
                    item_given_tax_code_code
                ) = TransactionInputVariableService.get_item_vars_AMZ(df_items, i)
                item_brand_name = None


        # platform independent
        item_tax_code_code = TaxCodeService.get_tax_code_code(item_given_tax_code_code, platform_code)

        item = ItemService.get_by_identifiers_seller_firm_id(item_sku, item_asin, seller_firm_id)
        item_data_raw = {
            'valid_from': valid_from,
            'created_by': user_id,
            'original_filename': original_filename,
            'sku': item_sku,
            'asin': item_asin,
            'seller_firm_id': seller_firm_id,
            'brand_name': item_brand_name,
            'name': item_name,
            'weight_kg': item_weight_kg,
            'tax_code_code': item_tax_code_code,
            # 'unit_cost_price_currency_code': unit_cost_price_currency_code,
            'unit_cost_price_net_est': unit_cost_price_net_est
        }
        item_data = {k: v for k, v in item_data_raw.items() if v is not None}

        if not isinstance(item, Item):

            try:
                item = ItemService.create(item_data)
                print(item, flush=True)
            except Exception as e:
                db.session.rollback()
                SocketService.emit_status_error_unidentifiable_object(object_type, 'item', current)
                raise InternalServerError(e)


            # push item to vuex via socket
            item_json = ItemSubSchema.get_item_sub(item)
            SocketService.emit_new_object(item_json, 'item')


        else:
            item_history = ItemHistoryService.get_current(item.id)
            data_changes = {**item_data, **item_history.attr_as_dict()}
            data_changes
            try:
                item.update(data_changes)
            except Exception as e:
                db.session.rollback()
                SocketService.emit_status_error_unidentifiable_object(object_type, 'item', current)
                raise InternalServerError(e)

            # push item to vuex via socket
            item_json = ItemSubSchema.get_item_sub(item)
            SocketService.emit_update_object(item_json, 'item')



    @staticmethod
    def get_unique_item_details_from_transaction_inputs_as_df(df: pd.DataFrame, platform_code: str) -> pd.DataFrame:
        # reduce to unique combinations of item id and channel
        if platform_code == 'AMZ':
            df_unique = df.drop_duplicates(subset=['ASIN'])[['SELLER_SKU','ASIN', 'ITEM_DESCRIPTION', 'ITEM_WEIGHT', 'PRODUCT_TAX_CODE']]

        return df_unique




    @staticmethod
    def get_item_unit_cost_price_est_from_transaction_inputs(df: pd.DataFrame, platform_code: str, target_currency_code: str = 'EUR') -> float:
        from app.namespaces.exchange_rate.service import ExchangeRateService
        # average of total value / qty * 0.6
        # needs to be differentiated by platform because of platform specific column names
        item_gross_prices = []
        if platform_code == 'AMZ':
            for i in len(df.index):
                sale_total_value_gross_raw = InputService.get_float_or_None(df, i, column='PRICE_OF_ITEMS_AMT_VAT_INCL')
                base_currency = InputService.get_str(df, i, column='TRANSACTION_CURRENCY_CODE')
                if isinstance(sale_total_value_gross_raw, float) and isinstance(base_currency, str):
                    item_quantity = InputService.get_float_or_None(df, i, column='QTY') #always provided
                    exchange_rate_date = InputService.get_date_or_None(df, i, column='TRANSACTION_COMPLETE_DATE') #always provided

                    #convert to target currency
                    sale_total_value_gross = sale_total_value_gross_raw * ExchangeRateService.get_by_base_target_date(base_currency, target_currency_code, exchange_rate_date)

                    item_gross_prices.append(sale_total_value_gross)


            avg_item_gross_price = mean(item_gross_prices)

        # general proceeding
        item_unit_cost_price_est = avg_item_gross_price * 0.6
        return item_unit_cost_price_est



    @staticmethod
    def get_unique_account_details_from_transaction_inputs_as_df(df: pd.DataFrame, platform_code: str) -> pd.DataFrame:
        # reduce to unique combinations of account id and channel
        if platform_code == 'AMZ':
            df_unique = df.drop_duplicates(subset=['UNIQUE_ACCOUNT_IDENTIFIER','SALES_CHANNEL'])[['UNIQUE_ACCOUNT_IDENTIFIER','SALES_CHANNEL']]

        return df_unique

    @staticmethod
    def get_unique_vatins_from_transaction_inputs(df: pd.DataFrame, seller_firm_id: int, platform_code: str) -> List:

        if platform_code == 'AMZ':
            column_values = df[["SELLER_DEPART_COUNTRY_VAT_NUMBER", "SELLER_ARRIVAL_COUNTRY_VAT_NUMBER", "TRANSACTION_SELLER_VAT_NUMBER"]].values.ravel('K')

        # general/platform-independent proceeding
        #unique values
        unique_vatin_numbers_raw = pd.unique(column_values).tolist()
        # drop nan
        unique_vatin_numbers = [vatin_number for vatin_number in unique_vatin_numbers_raw if str(vatin_number) != 'nan']

        return unique_vatin_numbers




    @staticmethod
    def get_valid_from_df(df, platform_code):
        if platform_code == 'AMZ':
            dates_all = df[[
                "TRANSACTION_DEPART_DATE",
                "TRANSACTION_ARRIVAL_DATE",
                "TRANSACTION_COMPLETE_DATE",
                "TAX_CALCULATION_DATE",
                "VAT_INV_EXCHANGE_RATE_DATE"
                ]].values.ravel('K')
            dates_raw = pd.unique(dates_all).tolist()
            #remove nan and transform to datetime.date object
            dates = [datetime.strptime(d, '%d-%m-%Y').date() for d in dates_raw if str(d) != 'nan']

        valid_from = min(dates)
        return valid_from





    @staticmethod
    def update_vatin_data(vatin_numbers, valid_from: date, seller_firm_id: int, original_filename):

        from app.namespaces.tax.vatin.service import VATINService, VIESService
        from app.namespaces.tax.vatin import VATIN
        from app.namespaces.tax.vatin.schema import VatinSchemaSocket

        for vatin_number_raw in vatin_numbers:
            country_code, number = VATINService.vat_precheck(None, number_raw)
            vatin = VATINService.get_by_country_code_number_date(country_code, number, date.today())

            if not isinstance(vatin, VATIN):

                vatin_data = {
                    'country_code': country_code,
                    'number': number,
                    'business_id': seller_firm_id,
                    'request_date': date.today()
                    'original_filename': original_filename,
                    'valid_from': valid_from
                }
                try:
                    resp_data = VIESService.send_request(country_code, number)
                    if resp_data['valid'] is not None:
                        vatin_data['valid'] = resp_data['valid']
                    vatin = VATINService.create(vatin_data)

                except:
                    # send error status via socket
                    message = 'Validation of vat number "{}-{}" temporarily unavailable.'.format(country_code, number)
                    SocketService.emit_status_warning('vatin', message)
                    db.session.rollback()
                    continue

                # push vatin to vuex via socket
                vatin_json=VatinSchemaSocket.get_vatin_sub(vatin)
                SocketService.emit_new_object(vatin_json, 'vatin')

            # upgrade
            else:
                if not isinstance(vatin.business_id, int):
                    vatin.business_id = seller_firm_id

                elif vatin.business_id != seller_firm_id
                    # send error status via socket
                    message = 'Vat number "{}-{}" is already associated with a different account.'.format(country_code, number)
                    SocketService.emit_status_warning(object_type, message)
                    continue

                if valid_from < vatin.valid_from:
                    vatin.valid_from = valid_from

                if !vatin.valid or vatin.valid is None:
                    try:
                        resp_data = VIESService.send_request(country_code, number)
                        if resp_data['valid'] and resp_data['valid'] is not None:
                            vatin.valid = True

                    except Exception as e:
                        current_app.logger.info(e)
                        continue

                try:
                    db.session.commit()
                except:
                    db.session.rollback()
