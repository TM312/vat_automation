
import shutil
from pathlib import Path
from typing import List
from datetime import datetime, timedelta, date
import pandas as pd

from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound, RequestEntityTooLarge, UnsupportedMediaType
from app.extensions import db


from . import Transaction
from .interface import TransactionInterface

from app.namespaces.account import Account
from app.namespaces.bundle import Bundle
from app.namespaces.bundle.service import BundleService
from app.namespaces.distance_sale import DistanceSale, DistanceSaleHistory
from app.namespaces.distance_sale.service import DistanceSaleService, DistanceSaleHistoryService
from app.namespaces.item import Item, ItemHistory
from app.namespaces.item.service import ItemService, ItemHistoryService
from app.namespaces.country import Country, EU
from app.namespaces.country.service import CountryService
from app.namespaces.business.service_parent import BusinessService
from app.namespaces.tax.vatin import VATIN
from app.namespaces.tax.vatin.service import VATINService
from app.namespaces.tax.tax_code.service import TaxCodeService
from app.namespaces.transaction_input import TransactionInput
from app.namespaces.transaction_input.interface import TransactionInputInterface
from app.namespaces.transaction_type import TransactionType
from app.namespaces.transaction_type_public.service import TransactionTypePublicService
from app.namespaces.tax.vat.service import VatHistoryService
from app.namespaces.tax.vatin.schema import VatinSchemaSocket
from app.namespaces.business.seller_firm import SellerFirm
from app.namespaces.utils.service import HelperService, NotificationService

from app.extensions.socketio.emitters import SocketService



class TransactionService:
    @staticmethod
    def get_all() -> List[Transaction]:
        transactions = Transaction.query.all()
        return transactions

    @staticmethod
    def get_by_id(transaction_id: int) -> Transaction:
        return Transaction.query.filter_by(id = transaction_id).first()

    @staticmethod
    def get_by_public_id(transaction_public_id: str) -> Transaction:
        return Transaction.query.filter_by(public_id = transaction_public_id).first()

    @staticmethod
    def get_by_transaction_input_id(transaction_input_id) -> Transaction:
        return Transaction.query.filter_by(transaction_input_id=transaction_input_id).first()

    @staticmethod
    def get_all_by_seller_firm_id(seller_firm_id: int) -> List[Transaction]:
        return Transaction.query.filter_by(seller_firm_id=seller_firm_id).all()

    @staticmethod
    def get_latest_by_seller_firm_id(seller_firm_id: int) -> List[Transaction]:
        return Transaction.query.filter_by(seller_firm_id=seller_firm_id).order_by(Transaction.tax_date.desc()).first()


    @staticmethod
    def get_by_tax_record(tax_record_public_id: str, **kwargs) -> List[Transaction]:
        from app.namespaces.tax_record import TaxRecord
        base_query = Transaction.query.join(TaxRecord.transactions).filter(TaxRecord.public_id == tax_record_public_id).order_by(Transaction.tax_date.desc())

        if kwargs.get('paginate') == True and isinstance(kwargs.get('page'), int):
            per_page = current_app.config.TRANSACTIONS_PER_QUERY
            page = kwargs.get('page')
            transactions = base_query.paginate(page, per_page, False).items

        else:
            transactions = base_query.all()
        return transactions

    @staticmethod
    def get_by_tax_record_tax_treatment(tax_record_public_id: str, tax_treatment_code: str, **kwargs) -> List[Transaction]:
        from app.namespaces.tax_record import TaxRecord
        base_query = Transaction.query.join(TaxRecord.transactions).filter(TaxRecord.public_id == tax_record_public_id).filter(Transaction.tax_treatment_code == tax_treatment_code).order_by(Transaction.tax_date.desc())

        if kwargs.get('paginate') == True and isinstance(kwargs.get('page'), int):
            per_page = current_app.config.TRANSACTIONS_PER_QUERY
            page = kwargs.get('page')
            transactions = base_query.paginate(page, per_page, False).items

        else:
            transactions = base_query.all()
        return transactions


    @staticmethod
    def update_by_public_id(transaction_public_id: str, data_changes: TransactionInterface) -> Transaction:
        transaction = TransactionService.get_by_public_id(transaction_public_id)
        if isinstance(transaction, Transaction):
            transaction.update(data_changes)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise

            return transaction



    @staticmethod
    def create_transaction_s(transaction_input: TransactionInputInterface) -> Transaction:
        from app.namespaces.account.service import AccountService

        account_given_id = transaction_input.account_given_id
        channel_code = transaction_input.channel_code
        given_id = transaction_input.given_id
        activity_id = transaction_input.activity_id
        item_sku = transaction_input.item_sku

        try:
            account = AccountService.get_by_given_id_channel_code(transaction_input.account_given_id, transaction_input.channel_code)
        except:
            SocketService.emit_status_error_unidentifiable_object(object_type, 'account', current)
            return False

        platform_code = account.channel.platform_code

        try:
            transaction_type = TransactionTypePublicService.get_by_code_platform_code(transaction_input.transaction_type_public_code, platform_code).transaction_type
            #TransactionTypeService.get_transaction_type_by_platform_public_code(transaction_input.transaction_type_public_code, platform_code)
        except:
            SocketService.emit_status_error_unidentifiable_object(object_type, 'transaction type', current)
            return False

        try:
            tax_date = TransactionService.get_tax_date(transaction_type, transaction_input)
        except:
            SocketService.emit_status_error_unidentifiable_object(object_type, 'tax date', current)
            return False

        try:
            item = ItemService.get_by_sku_account(transaction_input.item_sku, account)
        except:
            SocketService.emit_status_error_unidentifiable_object(object_type, 'item', current)
            return False


        # define foundational vars
        bundle = BundleService.get_by_id(transaction_input.bundle_id)

        try:
            arrival_country = TransactionService.get_country(transaction_input, bundle.id, transaction_type.code, country_type='arrival')
        except:
            SocketService.emit_status_error_unidentifiable_object(object_type, 'arrival country', current)
            return False

        try:
            departure_country = TransactionService.get_country(transaction_input, bundle.id, transaction_type.code, country_type='departure')
        except:
            SocketService.emit_status_error_unidentifiable_object(object_type, 'departure country', current)
            return False

        try:
            eu = CountryService.get_eu_by_date(tax_date)
        except:
            SocketService.emit_status_error_unidentifiable_object(object_type, 'eu', current)
            return False



        customer_vat_check_required: bool = TransactionService.vat_check_required(tax_date=tax_date, number=transaction_input.customer_vat_number)

        amazon_vat_calculation_service: bool = TransactionService.check_amazon_vat_calculation_service(transaction_input.tax_calculation_date)

        if transaction_type.code == 'MOVEMENT' or transaction_type.code == 'RETURN' or transaction_type.code == 'INBOUND': #!!! recheck if INBOUND here is correct
            customer_vatin = VATINService.get_by_country_code_seller_firm_id(arrival_country.code, account.seller_firm_id)
            customer_relationship = 'B2B'
            customer_relationship_checked = False

        else:
            customer_vatin = VATINService.get_vatin_or_None(country_code_temp=transaction_input.customer_vat_number_country_code, number_temp=transaction_input.customer_vat_number, date=tax_date)
            customer_relationship = TransactionService.get_transaction_relationship(customer_vatin, check_required=customer_vat_check_required)
            customer_relationship_checked = isinstance(customer_vatin, VATIN)



        if transaction_type.code == 'SALE' or transaction_type.code == 'REFUND':
            tax_treatment_code = TransactionService.get_tax_treatment_code(transaction_type.code, account.seller_firm_id, account.seller_firm.establishment_country_code, transaction_input, eu, customer_relationship, departure_country.code, arrival_country, amazon_vat_calculation_service, tax_date)
            new_transaction = TransactionService.calculate_transaction_vars(transaction_input, transaction_type, account, tax_treatment_code, tax_date, item, bundle, arrival_country, departure_country, eu, customer_relationship, customer_vatin, customer_relationship_checked, amazon_vat_calculation_service, customer_vat_check_required)
            # check for special case: non taxable distance sale
            if new_transaction.tax_treatment_code == 'DISTANCE_SALE':
                tax_treatment_code = 'NON_TAXABLE_DISTANCE_SALE'
                new_non_taxable_distance_sale = TransactionService.calculate_transaction_vars(transaction_input, transaction_type, account, tax_treatment_code, tax_date, item, bundle, arrival_country, departure_country, eu, customer_relationship, customer_vatin, customer_relationship_checked, amazon_vat_calculation_service, customer_vat_check_required)

        elif transaction_type.code == 'ACQUISITION':
            tax_treatment_code: str = TransactionService.get_tax_treatment_code(transaction_type.code, account.seller_firm_id, account.seller_firm.establishment_country_code, transaction_input, eu, customer_relationship, departure_country.code, arrival_country, amazon_vat_calculation_service, tax_date)
            new_transaction = TransactionService.calculate_transaction_vars(transaction_input, transaction_type, account, tax_treatment_code, tax_date, item, bundle, arrival_country, departure_country, eu, customer_relationship, customer_vatin, customer_relationship_checked, amazon_vat_calculation_service, customer_vat_check_required)

        elif transaction_type.code == 'MOVEMENT' or transaction_type.code == 'INBOUND' or transaction_type.code == 'RETURN':
            tax_treatment_codes = ['INTRA_COMMUNITY_SALE', 'INTRA_COMMUNITY_ACQUISITION']
            for tax_treatment_code in tax_treatment_codes:
                new_transaction = TransactionService.calculate_transaction_vars(
                    transaction_input,
                    transaction_type,
                    account,
                    tax_treatment_code,
                    tax_date,
                    item,
                    bundle,
                    arrival_country,
                    departure_country,
                    eu,
                    customer_relationship,
                    customer_vatin,
                    customer_relationship_checked,
                    amazon_vat_calculation_service,
                    customer_vat_check_required
                    )

        return True




    @staticmethod
    def calculate_transaction_vars(
            transaction_input: TransactionInput,
            transaction_type: TransactionType,
            account: Account,
            tax_treatment_code: str,
            tax_date: date,
            item: Item,
            bundle: Bundle,
            arrival_country: Country,
            departure_country: Country,
            eu: EU,
            customer_relationship: str,
            customer_vatin: VATIN,
            customer_relationship_checked: bool,
            amazon_vat_calculation_service: bool,
            customer_vat_check_required: bool
        ):


        seller_firm_id = account.seller_firm_id

        supplier_relationship = TransactionService.get_supplier_relationship(tax_treatment_code)
        supplier_vatin = TransactionService.get_supplier_vatin(tax_treatment_code, departure_country.code, seller_firm_id, transaction_input.departure_seller_vat_country_code, transaction_input.departure_seller_vat_number, tax_date)


        platform_code = account.channel.platform_code
        tax_calculation_date = TransactionService.get_tax_calculation_date(transaction_input.tax_calculation_date, tax_date, transaction_type.code, bundle.id)
        tax_jurisdiction: Country = TransactionService.get_tax_jurisdiction(tax_treatment_code, departure_country, arrival_country)

        item_history = ItemHistoryService.get_by_item_id_date(item.id, tax_date)

        item_tax_code_code, calculated_item_tax_code_code = TransactionService.get_item_tax_code_code(transaction_input, item_history.tax_code_code, platform_code, reference_tax_code=transaction_input.item_tax_code_code)
        item_vat_temp = VatHistoryService.get_by_tax_code_country_tax_date(item_tax_code_code, tax_jurisdiction.code, tax_date)
        item_tax_rate_type_code=item_vat_temp.tax_rate_type_code

        shipment_tax_rate_type_code = current_app.config.STANDARD_SERVICE_TAX_RATE_TYPE
        shipment_vat_temp = VatHistoryService.get_by_tax_rate_type_country_tax_date(tax_jurisdiction.code, shipment_tax_rate_type_code, tax_date)
        gift_wrap_tax_rate_type_code = current_app.config.STANDARD_SERVICE_TAX_RATE_TYPE
        gift_wrap_vat_temp = VatHistoryService.get_by_tax_rate_type_country_tax_date(tax_jurisdiction.code, shipment_tax_rate_type_code, tax_date)

        item_price_vat_rate: float = TransactionService.get_vat_rate(transaction_input, tax_jurisdiction, tax_treatment_code, tax_date, tax_rate_type_code=item_tax_rate_type_code, reference_vat_rate=item_vat_temp.rate, calculated_vat_rate=item_vat_temp.rate)
        gift_wrap_price_vat_rate: float = TransactionService.get_vat_rate(transaction_input, tax_jurisdiction, tax_treatment_code, tax_date, tax_rate_type_code=shipment_tax_rate_type_code, calculated_vat_rate=gift_wrap_vat_temp.rate)
        shipment_price_vat_rate: float = TransactionService.get_vat_rate(transaction_input, tax_jurisdiction, tax_treatment_code, tax_date, tax_rate_type_code=gift_wrap_tax_rate_type_code, calculated_vat_rate=shipment_vat_temp.rate)

        item_price_net: float = TransactionService.get_price_net(item_history.unit_cost_price_net, transaction_input.item_price_gross, item_price_vat_rate, transaction_type.code, price_type='item', discount=False)
        item_price_discount_net: float = TransactionService.get_price_net(item_history.unit_cost_price_net, transaction_input.item_price_discount_gross, item_price_vat_rate, transaction_type.code, price_type='item', discount=True)
        item_price_total_net: float = TransactionService.get_price_net(item_history.unit_cost_price_net, transaction_input.item_price_total_gross, item_price_vat_rate, transaction_type.code, price_type='item', discount=False)

        shipment_price_net: float = TransactionService.get_price_net(item_history.unit_cost_price_net, transaction_input.shipment_price_gross, shipment_price_vat_rate, transaction_type.code, price_type='shipment', discount=False)
        shipment_price_discount_net: float = TransactionService.get_price_net(item_history.unit_cost_price_net, transaction_input.shipment_price_discount_gross, shipment_price_vat_rate, transaction_type.code, price_type='shipment', discount=True)
        shipment_price_total_net: float = TransactionService.get_price_net(item_history.unit_cost_price_net, transaction_input.shipment_price_total_gross, shipment_price_vat_rate, transaction_type.code, price_type='shipment', discount=False)

        gift_wrap_price_net: float = TransactionService.get_price_net(item_history.unit_cost_price_net, transaction_input.gift_wrap_price_gross, gift_wrap_price_vat_rate, transaction_type.code, price_type='gift_wrap', discount=False)
        gift_wrap_price_discount_net: float = TransactionService.get_price_net(item_history.unit_cost_price_net, transaction_input.gift_wrap_price_discount_gross, gift_wrap_price_vat_rate, transaction_type.code, price_type='gift_wrap', discount=True)
        gift_wrap_price_total_net: float = TransactionService.get_price_net(item_history.unit_cost_price_net, transaction_input.gift_wrap_price_total_gross, gift_wrap_price_vat_rate, transaction_type.code, price_type='gift_wrap', discount=False)

        item_price_vat: float = TransactionService.get_price_vat(transaction_input.item_price_gross, item_price_vat_rate, transaction_type.code)
        item_price_discount_vat: float = TransactionService.get_price_vat(transaction_input.item_price_discount_gross, item_price_vat_rate, transaction_type.code)
        item_price_total_vat: float = TransactionService.get_price_vat(transaction_input.item_price_total_gross, item_price_vat_rate, transaction_type.code)

        shipment_price_vat: float = TransactionService.get_price_vat(transaction_input.shipment_price_gross, shipment_price_vat_rate, transaction_type.code)
        shipment_price_discount_vat: float = TransactionService.get_price_vat(transaction_input.shipment_price_discount_gross, shipment_price_vat_rate, transaction_type.code)
        shipment_price_total_vat: float = TransactionService.get_price_vat(transaction_input.shipment_price_total_gross, shipment_price_vat_rate, transaction_type.code)

        gift_wrap_price_vat: float = TransactionService.get_price_vat(transaction_input.gift_wrap_price_gross, gift_wrap_price_vat_rate, transaction_type.code)
        gift_wrap_price_discount_vat: float = TransactionService.get_price_vat(transaction_input.gift_wrap_price_discount_gross, gift_wrap_price_vat_rate, transaction_type.code)
        gift_wrap_price_total_vat: float = TransactionService.get_price_vat(transaction_input.gift_wrap_price_total_gross, gift_wrap_price_vat_rate, transaction_type.code)

        total_value_net: float = TransactionService.get_total_value(transaction_input.item_quantity, transaction_type.code, item_price_total_net, shipment_price_total_net, gift_wrap_price_total_net, item_price_total_net)
        total_value_vat: float = TransactionService.get_total_value(transaction_input.item_quantity, transaction_type.code, item_price_total_vat, shipment_price_total_vat, gift_wrap_price_total_vat, item_price_total_vat)
        total_value_gross: float = TransactionService.get_total_value(transaction_input.item_quantity, transaction_type.code, transaction_input.item_price_total_gross, transaction_input.shipment_price_total_gross, transaction_input.gift_wrap_price_total_gross, item_price_total_net)
        # !!! comment: first total_value_gross dann daraus total_value_vat und total_value_net

        transaction_currency_code: str = TransactionService.get_transaction_currency(item_history.unit_cost_price_currency_code, transaction_type.code, transaction_input.currency_code)


        invoice_currency_code: str = TransactionService.get_invoice_currency_code(departure_country, tax_jurisdiction, tax_treatment_code)
        invoice_exchange_rate_date: date = TransactionService.get_invoice_exchange_rate_date(transaction_type.code, bundle.id, transaction_currency_code, invoice_currency_code, tax_date)
        invoice_exchange_rate: float = TransactionService.get_invoice_exchange_rate(invoice_exchange_rate_date=invoice_exchange_rate_date, transaction_currency_code=transaction_currency_code, invoice_currency_code=invoice_currency_code)

        invoice_amount_net: float = TransactionService.get_invoice_amount(total_value_net, invoice_exchange_rate)
        invoice_amount_vat: float = TransactionService.get_invoice_amount(total_value_vat, invoice_exchange_rate)
        invoice_amount_gross: float = TransactionService.get_invoice_amount(total_value_gross, invoice_exchange_rate)

        reverse_charge_vat_rate: float = TransactionService.get_reverse_charge_vat_rate(transaction_input, arrival_country.code, tax_treatment_code, tax_date, item_tax_rate_type_code, item_history.tax_code_code)
        invoice_amount_reverse_charge_vat: float = TransactionService.get_invoice_amount_reverse_charge_vat(invoice_amount_net, reverse_charge_vat_rate)


        try:
            arrival_seller_vatin = VATINService.get_vatin_or_None(arrival_country.vat_country_code, transaction_input.arrival_seller_vat_number, date=tax_date)
        except:
            raise
        try:
            departure_seller_vatin = VATINService.get_vatin_or_None(departure_country.vat_country_code, transaction_input.departure_seller_vat_number, date=tax_date)
        except:
            raise
        try:
            seller_vatin = VATINService.get_vatin_or_None(tax_jurisdiction.vat_country_code, transaction_input.seller_vat_number, date=tax_date)
        except:
            raise

        seller_firm = BusinessService.get_by_id(seller_firm_id)
        if arrival_seller_vatin in seller_firm.vat_numbers and (
            arrival_seller_vatin.initial_tax_date is None or
            tax_date < arrival_seller_vatin.initial_tax_date
        ):
            arrival_seller_vatin.initial_tax_date = tax_date
            try:
                db.session.commit()
                meta = VatinSchemaSocket.get_vatin_sub(arrival_seller_vatin)
                SocketService.emit_update_object(meta, 'vat_number')
            except:
                db.session.rollback()
                raise

        if departure_seller_vatin in seller_firm.vat_numbers and (
            departure_seller_vatin.initial_tax_date is None or
            tax_date < departure_seller_vatin.initial_tax_date
        ):
            departure_seller_vatin.initial_tax_date = tax_date
            try:
                db.session.commit()
                meta = VatinSchemaSocket.get_vatin_sub(departure_seller_vatin)
                SocketService.emit_update_object(meta, 'vat_number')
            except:
                db.session.rollback()
                raise

        if seller_vatin in seller_firm.vat_numbers and (
            seller_vatin.initial_tax_date is None or
            tax_date < seller_vatin.initial_tax_date
        ):
            seller_vatin.initial_tax_date = tax_date
            try:
                db.session.commit()
                meta = VatinSchemaSocket.get_vatin_sub(seller_vatin)
                SocketService.emit_update_object(meta, 'vat_number')
            except:
                db.session.rollback()
                raise


        transaction_data= {
            'transaction_input_id': transaction_input.id,
            'seller_firm_id': seller_firm.id,
            'item_id': item.id,

            'type_code': transaction_type.code,
            'amazon_vat_calculation_service': amazon_vat_calculation_service,

            'customer_relationship_checked': customer_relationship_checked,
            'customer_relationship': customer_relationship,
            'customer_vatin_id': customer_vatin.id if customer_vatin else None,

            'supplier_relationship': supplier_relationship if supplier_relationship else None,
            'supplier_vatin_id': supplier_vatin.id if isinstance(supplier_vatin, VATIN) else None,

            'tax_jurisdiction_code': tax_jurisdiction.code,
            'arrival_country_code': arrival_country.code,
            'departure_country_code': departure_country.code,

            'tax_treatment_code': tax_treatment_code,

            'tax_date': tax_date,
            'tax_calculation_date': tax_calculation_date,

            'item_tax_code_code': item_tax_code_code,

            'item_tax_rate_type_code': item_tax_rate_type_code,
            'shipment_tax_rate_type_code': shipment_tax_rate_type_code,
            'gift_wrap_tax_rate_type_code': gift_wrap_tax_rate_type_code,

            'item_price_net': item_price_net,
            'item_price_discount_net': item_price_discount_net,
            'item_price_total_net': item_price_total_net,

            'shipment_price_net': shipment_price_net,
            'shipment_price_discount_net': shipment_price_discount_net,
            'shipment_price_total_net': shipment_price_total_net,

            'gift_wrap_price_net': gift_wrap_price_net,
            'gift_wrap_price_discount_net': gift_wrap_price_discount_net,
            'gift_wrap_price_total_net': gift_wrap_price_total_net,

            'item_price_vat_rate': item_price_vat_rate,
            'item_price_vat': item_price_vat,
            'item_price_discount_vat': item_price_discount_vat,
            'item_price_total_vat': item_price_total_vat,

            'shipment_price_vat_rate': shipment_price_vat_rate,
            'shipment_price_vat': shipment_price_vat,
            'shipment_price_discount_vat': shipment_price_discount_vat,
            'shipment_price_total_vat': shipment_price_total_vat,

            'gift_wrap_price_vat_rate': gift_wrap_price_vat_rate,
            'gift_wrap_price_vat': gift_wrap_price_vat,
            'gift_wrap_price_discount_vat': gift_wrap_price_discount_vat,
            'gift_wrap_price_total_vat': gift_wrap_price_total_vat,

            'total_value_net': total_value_net,
            'total_value_vat': total_value_vat,
            'total_value_gross': total_value_gross,

            'transaction_currency_code': transaction_currency_code,

            'invoice_currency_code': invoice_currency_code,
            'invoice_exchange_rate_date': invoice_exchange_rate_date,
            'invoice_exchange_rate': invoice_exchange_rate,

            'invoice_amount_net': invoice_amount_net,
            'invoice_amount_vat': invoice_amount_vat,
            'invoice_amount_gross': invoice_amount_gross,

            'reverse_charge_vat_rate': reverse_charge_vat_rate,
            'invoice_amount_reverse_charge_vat': invoice_amount_reverse_charge_vat,

            'arrival_seller_vatin_id': arrival_seller_vatin.id if arrival_seller_vatin else None,
            'departure_seller_vatin_id': departure_seller_vatin.id if departure_seller_vatin else None,
            'seller_vatin_id': seller_vatin.id if seller_vatin else None

        }

        try:
            new_transaction = TransactionService.create(transaction_data)

        except:
            db.session.rollback()
            raise

        try:
            TransactionService.create_notifications(
                new_transaction.id,
                transaction_input,
                item,
                customer_vatin,
                tax_calculation_date,
                invoice_currency_code,
                item_tax_code_code,
                calculated_item_tax_code_code,
                tax_date,
                customer_vat_check_required,
                reference_vat_rate=item_price_vat_rate,
                calculated_vat_rate=item_vat_temp.rate,

            )
        except:
            db.session.rollback()
            raise

        return new_transaction



    @staticmethod
    def create(transaction_data: TransactionInterface) -> Transaction:
        new_transaction = Transaction(
            transaction_input_id = transaction_data.get('transaction_input_id'),
            seller_firm_id=transaction_data.get('seller_firm_id'),
            # account_id=transaction_data.get('account_id'),
            item_id = transaction_data.get('item_id'),

            type_code = transaction_data.get('type_code'),
            amazon_vat_calculation_service = transaction_data.get('amazon_vat_calculation_service'),

            customer_relationship_checked = transaction_data.get('customer_relationship_checked'),
            customer_relationship = transaction_data.get('customer_relationship'),
            customer_vatin_id = transaction_data.get('customer_vatin_id'),

            supplier_relationship = transaction_data.get('supplier_relationship'),
            supplier_vatin_id = transaction_data.get('supplier_vatin_id'),

            tax_jurisdiction_code = transaction_data.get('tax_jurisdiction_code'),
            arrival_country_code = transaction_data.get('arrival_country_code'),
            departure_country_code = transaction_data.get('departure_country_code'),

            tax_treatment_code = transaction_data.get('tax_treatment_code'),
            tax_date = transaction_data.get('tax_date'),
            tax_calculation_date = transaction_data.get('tax_calculation_date'),
            item_tax_code_code = transaction_data.get('item_tax_code_code'),
            item_tax_rate_type_code = transaction_data.get('item_tax_rate_type_code'),
            shipment_tax_rate_type_code = transaction_data.get('shipment_tax_rate_type_code'),
            gift_wrap_tax_rate_type_code = transaction_data.get('gift_wrap_tax_rate_type_code'),
            item_price_net = transaction_data.get('item_price_net'),
            item_price_discount_net = transaction_data.get('item_price_discount_net'),
            item_price_total_net = transaction_data.get('item_price_total_net'),
            shipment_price_net = transaction_data.get('shipment_price_net'),
            shipment_price_discount_net = transaction_data.get('shipment_price_discount_net'),
            shipment_price_total_net = transaction_data.get('shipment_price_total_net'),
            gift_wrap_price_net = transaction_data.get('gift_wrap_price_net'),
            gift_wrap_price_discount_net = transaction_data.get('gift_wrap_price_discount_net'),
            gift_wrap_price_total_net = transaction_data.get('gift_wrap_price_total_net'),
            item_price_vat_rate = transaction_data.get('item_price_vat_rate'),
            item_price_vat = transaction_data.get('item_price_vat'),
            item_price_discount_vat = transaction_data.get('item_price_discount_vat'),
            item_price_total_vat = transaction_data.get('item_price_total_vat'),
            gift_wrap_price_vat_rate = transaction_data.get('gift_wrap_price_vat_rate'),
            shipment_price_vat = transaction_data.get('shipment_price_vat'),
            shipment_price_discount_vat = transaction_data.get('shipment_price_discount_vat'),
            shipment_price_total_vat = transaction_data.get('shipment_price_total_vat'),
            shipment_price_vat_rate = transaction_data.get('shipment_price_vat_rate'),
            gift_wrap_price_vat = transaction_data.get('gift_wrap_price_vat'),
            gift_wrap_price_discount_vat = transaction_data.get('gift_wrap_price_discount_vat'),
            gift_wrap_price_total_vat = transaction_data.get('gift_wrap_price_total_vat'),
            total_value_net = transaction_data.get('total_value_net'),
            total_value_vat = transaction_data.get('total_value_vat'),
            total_value_gross = transaction_data.get('total_value_gross'),
            transaction_currency_code = transaction_data.get('transaction_currency_code'),
            invoice_currency_code = transaction_data.get('invoice_currency_code'),
            invoice_exchange_rate_date = transaction_data.get('invoice_exchange_rate_date'),
            invoice_exchange_rate = transaction_data.get('invoice_exchange_rate'),
            invoice_amount_net = transaction_data.get('invoice_amount_net'),
            invoice_amount_vat = transaction_data.get('invoice_amount_vat'),
            invoice_amount_gross = transaction_data.get('invoice_amount_gross'),
            reverse_charge_vat_rate = transaction_data.get('reverse_charge_vat_rate'),
            invoice_amount_reverse_charge_vat = transaction_data.get('invoice_amount_reverse_charge_vat'),
            arrival_seller_vatin_id = transaction_data.get('arrival_seller_vatin_id'),
            departure_seller_vatin_id = transaction_data.get('departure_seller_vatin_id'),
            seller_vatin_id = transaction_data.get('seller_vatin_id')
        )

        db.session.add(new_transaction)
        db.session.commit()

        return new_transaction


    @staticmethod
    def create_notifications(
            transaction_id: int,
            transaction_input: TransactionInput,
            item: Item,
            customer_vatin: VATIN,
            tax_calculation_date: date,
            invoice_currency_code: str,
            item_tax_code_code: str,
            calculated_item_tax_code_code: str,
            tax_date: date,
            customer_vat_check_required: bool,
            reference_vat_rate: float,
            calculated_vat_rate: float,
            ) -> None:

        ItemService.compare_calculation_reference(transaction_id, transaction_input, item)
        TransactionService.compare_calculation_reference_customer_name(transaction_id, transaction_input, customer_vatin)
        # Notification if Customer or Supplier Vat invalid
        TransactionService.compare_calculation_reference_tax_calculation_date(transaction_id, transaction_input, tax_calculation_date)
        TransactionService.compare_calculation_reference_invoice_currency_code(transaction_id, transaction_input, invoice_currency_code)
        VatHistoryService.compare_reference_calculated_vat_rates(transaction_id, transaction_input, reference_vat_rate=reference_vat_rate, calculated_vat_rate=calculated_vat_rate)
        TaxCodeService.compare_calculation_reference(transaction_id, transaction_input.original_filename, calculated_item_tax_code_code, item_tax_code_code)
        VATINService.compare_calculation_reference_old_transaction(transaction_id, transaction_input, customer_vat_check_required, tax_date, transaction_input.customer_vat_number)



    @staticmethod
    def compare_calculation_reference_tax_calculation_date(transaction_id: int, transaction_input: TransactionInput, tax_calculation_date: date) -> None:
        if transaction_input.tax_calculation_date and transaction_input.tax_calculation_date != tax_calculation_date:
            notification_data = NotificationService.create_transaction_notification_data(main_subject='Tax Calculation Date', original_filename=transaction_input.original_filename, status='warning', reference_value=transaction_input.tax_calculation_date, calculated_value=tax_calculation_date, transaction_id=transaction_id)
            NotificationService.create_transaction_notification(notification_data)

    @staticmethod
    def compare_calculation_reference_invoice_currency_code(transaction_id: int, transaction_input: TransactionInput, invoice_currency_code: str) -> None:
        if transaction_input.invoice_currency_code and transaction_input.invoice_currency_code != invoice_currency_code:
            notification_data = NotificationService.create_transaction_notification_data(main_subject='Invoice Currency Code', original_filename=transaction_input.original_filename, status='warning', reference_value=transaction_input.invoice_currency_code, calculated_value=invoice_currency_code, transaction_id=transaction_id)
            NotificationService.create_transaction_notification(notification_data)


    @staticmethod
    def compare_calculation_reference_customer_name(transaction_id: int, transaction_input: 'app.namespaces.transaction_input.TransactionInput', customer_vatin: VATIN):
        if transaction_input.customer_name and customer_vatin.name and transaction_input.customer_name != customer_vatin.name:
            notification_data = NotificationService.create_transaction_notification_data(main_subject='Customer Firm Name', original_filename=transaction_input.original_filename, status='info', reference_value=transaction_input.customer_name, calculated_value=customer_vatin.name, transaction_id=transaction_id)
            NotificationService.create_transaction_notification(notification_data)


    @staticmethod
    def get_tax_treatment_code(
            transaction_type_code: str,
            seller_firm_id: int,
            establishment_country_code: str,
            transaction_input: TransactionInput,
            eu: EU,
            customer_relationship: str,
            departure_country_code: str,
            arrival_country: Country,
            amazon_vat_calculation_service: bool,
            tax_date: date) -> str:


        if transaction_type_code == 'SALE' or transaction_type_code == 'REFUND':

            if (transaction_input.export or arrival_country not in eu.countries):
                tax_treatment_code = 'EXPORT'

            elif customer_relationship == 'B2B':
                if departure_country_code != arrival_country.code:
                    tax_treatment_code = 'INTRA_COMMUNITY_SALE'

                else:
                    if (
                    (departure_country_code in ['ES', 'FR', 'IT', 'PL'] and departure_country_code != establishment_country_code) or
                    (amazon_vat_calculation_service and transaction_input.item_price_vat_rate == 0)
                    ):
                        tax_treatment_code = 'LOCAL_SALE_REVERSE_CHARGE'

                    else:
                        tax_treatment_code='LOCAL_SALE'


            elif customer_relationship == 'B2C':

                distance_sale = DistanceSaleService.get_by_arrival_country_seller_firm_id(arrival_country.code, seller_firm_id)
                distance_sale_history = DistanceSaleHistoryService.get_by_distance_sale_id_date(distance_sale.id, tax_date) if isinstance(distance_sale, DistanceSale) else None

                distance_sale_history_active = (
                    distance_sale_history.active
                    if isinstance(distance_sale_history, DistanceSaleHistory) and isinstance(distance_sale, DistanceSale)
                    else False
                )

                if departure_country_code != arrival_country.code and distance_sale_history_active: #or threshold surpassed
                    tax_treatment_code = 'DISTANCE_SALE'

                else:
                    tax_treatment_code = 'LOCAL_SALE'

        elif transaction_type_code == 'ACQUISITION':
            tax_treatment_code = 'LOCAL_ACQUISITION'


        return tax_treatment_code



    @staticmethod
    def get_transaction_relationship(vatin: VATIN, check_required: bool) -> str:

        if isinstance(vatin, VATIN):
            bool_as_code = 'B2B' if vatin.valid else 'B2C'
            transaction_relationship = 'B2B' if not check_required else bool_as_code
            # Create Notification if bool_as_code != transaction_relationship !!!!

        else:
            transaction_relationship = 'B2C'

        return transaction_relationship

    @staticmethod
    def get_country(transaction_input: TransactionInput, bundle_id: int, transaction_type_code: str, country_type: str) -> Country:
        if transaction_type_code == 'REFUND':
            sale_transaction = TransactionService.get_sale_transaction_by_bundle_id(bundle_id)
            if isinstance(sale_transaction, Transaction):
                if country_type == 'arrival':
                    country = sale_transaction.arrival_country
                elif country_type == 'departure':
                    country = sale_transaction.departure_country
                else:
                    raise

            else:
                if country_type == 'arrival':
                    country_code = transaction_input.sale_arrival_country_code
                elif country_type == 'departure':
                    country_code = transaction_input.sale_departure_country_code

                else:
                    raise

                country = CountryService.get_by_code(country_code)


        else:
            if country_type == 'arrival':
                country = CountryService.get_by_code(transaction_input.arrival_country_code)
            else:
                country = CountryService.get_by_code(transaction_input.departure_country_code)

        if not isinstance(country, Country):
            raise

        else:
            return country


    @staticmethod
    def get_by_validity_tax_jurisdiction_seller_firm(start_date: date, end_date: date, seller_firm_id: int, tax_jurisdiction_code: str) -> List[Transaction]:
        return Transaction.query.filter(
            Transaction.tax_date.between(start_date, end_date),
            Transaction.seller_firm_id==seller_firm_id,
            Transaction.tax_jurisdiction_code==tax_jurisdiction_code
            ).all()


    @staticmethod
    def vat_check_required(tax_date: date, number: str) -> bool:
        OLD_TRANSACTION_TOLERANCE_DAYS = current_app.config.OLD_TRANSACTION_TOLERANCE_DAYS
        if not number:
            return False
        else:
            result: bool = date.today() - tax_date <= timedelta(days=OLD_TRANSACTION_TOLERANCE_DAYS)
            return result



    @staticmethod
    def get_vat_rate(transaction_input: TransactionInput, tax_jurisdiction: Country, tax_treatment_code: str, tax_date: date, tax_rate_type_code: str, **kwargs) -> float:
        # if tax_treatment_code == 'EXPORT' or tax_treatment_code == 'INTRA_COMMUNITY_SALE' or tax_treatment_code == 'LOCAL_SALE_REVERSE_CHARGE' or tax_treatment_code == 'INTRA_COMMUNITY_ACQUISITION':
        #     calculated_vat_rate=float(0)

        if isinstance(kwargs.get('calculated_vat_rate'), (int, float, complex)) and not isinstance(kwargs.get('calculated_vat_rate'), bool):
            calculated_vat_rate=kwargs['calculated_vat_rate']

        else:
            raise

        if isinstance(kwargs.get('reference_vat_rate'), (int, float, complex)) and not isinstance(kwargs.get('reference_vat_rate'), bool):
            reference_vat_rate=kwargs['reference_vat_rate']
            if calculated_vat_rate != reference_vat_rate:
                vat_rate=reference_vat_rate

            else:
                vat_rate = calculated_vat_rate

        else:
            vat_rate=calculated_vat_rate

        return vat_rate




    @staticmethod
    def get_tax_date(transaction_type: TransactionType, transaction_input: TransactionInput) -> date:
        if transaction_type.code == 'SALE':
            tax_date = transaction_input.shipment_date

        elif transaction_type.code == 'REFUND':
            tax_date = transaction_input.complete_date

        elif transaction_type.code == 'MOVEMENT':
            tax_date = transaction_input.shipment_date

        elif transaction_type.code == 'ACQUISITION':
            tax_date = transaction_input.complete_date

        elif transaction_type.code == 'INBOUND':
            tax_date=transaction_input.complete_date

        elif transaction_type.code == 'RETURN':
            tax_date = transaction_input.complete_date

        else:
            raise

        return tax_date





    @staticmethod
    def get_supplier_relationship(tax_treatment_code: str) -> str:
        return 'B2B' if tax_treatment_code == 'INTRA_COMMUNITY_ACQUISITION' or tax_treatment_code == 'LOCAL_ACQUISITION' else None

    @staticmethod
    def get_supplier_vatin(tax_treatment_code: str, departure_country_code: str, seller_firm_id: int, transaction_input_check_departure_seller_vat_country_code: str, transaction_input_check_departure_seller_vat_number: str, tax_date: date) -> VATIN:
        if tax_treatment_code == 'INTRA_COMMUNITY_ACQUISITION':
            return VATINService.get_by_country_code_seller_firm_id(departure_country_code, seller_firm_id)

        elif tax_treatment_code == 'LOCAL_ACQUISITION':
            return VATINService.get_by_country_code_number_date(transaction_input_check_departure_seller_vat_country_code, transaction_input_check_departure_seller_vat_number, tax_date)


    @staticmethod
    def get_invoice_currency_code(departure_country: Country, tax_jurisdiction: Country, tax_treatment_code: str) -> str:
        if tax_treatment_code == 'NON_TAXABLE_DISTANCE_SALE':
            invoice_currency_code = departure_country.currency_code
        else:
            invoice_currency_code = tax_jurisdiction.currency_code

        return invoice_currency_code



    @staticmethod
    def get_transaction_currency(item_history_unit_cost_price_currency_code: str, transaction_type_code: str, input_currency_code: str) -> str:

        if transaction_type_code=="MOVEMENT" or transaction_type_code=="INBOUND" or transaction_type_code=='RETURN':
            transaction_currency_code = item_history_unit_cost_price_currency_code

        else:
            transaction_currency_code = input_currency_code

        return transaction_currency_code


    @staticmethod
    def get_invoice_amount_reverse_charge_vat(invoice_amount_net: float, reverse_charge_vat_rate: float) -> float:
        return invoice_amount_net * reverse_charge_vat_rate


    @staticmethod
    def get_reverse_charge_vat_rate(transaction_input: TransactionInput, arrival_country_code: str, tax_treatment_code: str, tax_date: date, tax_rate_type_code: str, tax_code_code: str) -> float:
        if tax_treatment_code != 'INTRA_COMMUNITY_ACQUISITION':
            reverse_charge_vat_rate=float(0)
        else:
            # tax jurisdiction is arrival country
            reverse_charge_vat_rate = VatHistoryService.get_by_tax_code_country_tax_date(tax_code_code, arrival_country_code, tax_date).rate

        return reverse_charge_vat_rate


    @staticmethod
    def get_sale_transaction_by_bundle_id(bundle_id: int) -> Transaction:
        from app.namespaces.transaction_input.service import TransactionInputService

        sale_transaction_input = TransactionInputService.get_sale_transaction_input_by_bundle_id(bundle_id)
        if sale_transaction_input:
            sale_transaction=TransactionService.get_by_transaction_input_id(sale_transaction_input.id)

            return sale_transaction




    @staticmethod
    def get_invoice_amount(total_value: float, invoice_exchange_rate: float) -> float:
        invoice_amount = float(total_value) * float(invoice_exchange_rate)
        return invoice_amount



    @staticmethod
    def get_invoice_exchange_rate_date(transaction_type_code: str, bundle_id: int, transaction_currency_code: str, invoice_currency_code: str, tax_date: date) -> date:
        if TransactionService.check_exchange_rate_required(transaction_currency_code, invoice_currency_code):

            if transaction_type_code == "REFUND":
                sale_transaction = TransactionService.get_sale_transaction_by_bundle_id(bundle_id)
                if isinstance(sale_transaction, Transaction):
                    exchange_rate_date = sale_transaction.invoice_exchange_rate_date

                else:
                    exchange_rate_date = tax_date - timedelta(days=1)


            else:
                exchange_rate_date = tax_date - timedelta(days=1)

            return exchange_rate_date



    @staticmethod
    def get_invoice_exchange_rate(invoice_exchange_rate_date: date, transaction_currency_code: str, invoice_currency_code: str) -> float:

        if invoice_exchange_rate_date:
            from app.namespaces.exchange_rate.service import ExchangeRateService
            invoice_exchange_rate = ExchangeRateService.get_by_base_target_date(base=transaction_currency_code, target=invoice_currency_code, date=invoice_exchange_rate_date).rate

        else:
            invoice_exchange_rate = float(1)

        return invoice_exchange_rate


    @staticmethod
    def check_exchange_rate_required(transaction_currency_code: str, invoice_currency_code: str) -> bool:
        return transaction_currency_code != invoice_currency_code





    @staticmethod
    def get_price_net(item_history_unit_cost_price_net: float, price_gross: float, price_tax_rate: float, transaction_type_code: str, price_type: str, discount: bool) -> float:
        if transaction_type_code == 'MOVEMENT' or transaction_type_code == 'INBOUND':
            if discount:
                price_net = float(0)

            else:
                if price_type=='item':
                    price_net = float(item_history_unit_cost_price_net)

                elif price_type=='shipment' or price_type=='gift_wrap':
                    price_net = float(0)

        else:
            price_net = float(price_gross) / (1 + float(price_tax_rate))

        return price_net


    @staticmethod
    def get_price_vat(price_gross: float, price_tax_rate: float, transaction_type_code: str) -> float:
        if transaction_type_code == 'MOVEMENT' or transaction_type_code == 'INBOUND':
            price_vat = float(0)

        else:
            price_vat = float(price_gross) / (1 + float(price_tax_rate)) * float(price_tax_rate)
        return price_vat



    @staticmethod
    def get_total_value(item_quantity: int, transaction_type_code: str, item_price_total: float, shipment_price_total: float, gift_wrap_price_total: float, item_unit_cost_price: float) -> float:
        if transaction_type_code == 'MOVEMENT' or transaction_type_code == 'INBOUND':
            return item_unit_cost_price * item_quantity

        else:
            return item_price_total + shipment_price_total + gift_wrap_price_total


    @staticmethod
    def check_amazon_vat_calculation_service(check_tax_calculation_date: date) -> bool:
        return isinstance(check_tax_calculation_date, date)

    @staticmethod
    def get_tax_calculation_date(check_tax_calculation_date: date, tax_date: date, transaction_type_code: str, bundle_id: int) -> date:
        if isinstance(check_tax_calculation_date, date):
            tax_calculation_date = check_tax_calculation_date

        else:
            if transaction_type_code == 'REFUND':
                sale_transaction = TransactionService.get_sale_transaction_by_bundle_id(bundle_id)
                if isinstance(sale_transaction, Transaction):
                    tax_calculation_date = sale_transaction.tax_calculation_date
                else:
                    tax_calculation_date = tax_date - timedelta(days=1)
            else:
                tax_calculation_date = tax_date - timedelta(days=1)

        return tax_calculation_date


    @staticmethod
    def get_tax_jurisdiction(tax_treatment_code: str, departure_country: Country, arrival_country: Country) -> Country:
        if (
            tax_treatment_code == 'DISTANCE_SALE'
            or tax_treatment_code == 'INTRA_COMMUNITY_ACQUISITION'
            or tax_treatment_code == 'LOCAL_ACQUISITION'
            ):
            tax_jurisdiction_code = arrival_country.code
        else:
            tax_jurisdiction_code = departure_country.code

        tax_jurisdiction = CountryService.get_by_code(country_code = tax_jurisdiction_code)

        return tax_jurisdiction


    @staticmethod
    def get_item_tax_code_code(transaction_input: TransactionInput, item_history_tax_code_code: str, platform_code: str, **kwargs) -> str:
        if platform_code == 'AMZ':
            calculated_item_tax_code_code = item_history_tax_code_code

        else:
            raise

        if 'reference_tax_code' in kwargs and kwargs['reference_tax_code'] != None:
            reference_tax_code = kwargs['reference_tax_code']

            if calculated_item_tax_code_code != reference_tax_code:
                item_tax_code_code = reference_tax_code
            else:
                item_tax_code_code = calculated_item_tax_code_code
        else:
            item_tax_code_code = calculated_item_tax_code_code

        return item_tax_code_code, calculated_item_tax_code_code





class TransactionExportService:

    @staticmethod
    def create_df_transactions(transactions: List[Transaction], seller_firm_name: str) -> pd.DataFrame:

        df = pd.DataFrame(
            columns=[
                'created_on',
                'created_on',
                'modified_at',
                'modified_by',
                'notifications',
                'transaction_input',
                'seller_firm',
                'item',
                'type_code',
                'amazon_vat_calculation_service',
                'customer_relationship_checked',
                'customer_relationship',
                'customer_vatin',
                'supplier_relationship',
                'supplier_vatin',
                'tax_jurisdiction_code',
                'arrival_country_code',
                'departure_country_code',
                'tax_treatment_code',
                'tax_date',
                'tax_calculation_date',
                'item_tax_code_code',
                'item_tax_rate_type_code',
                'shipment_tax_rate_type_code',
                'gift_wrap_tax_rate_type_code',
                'item_price_net',
                'item_price_discount_net',
                'item_price_total_net',
                'shipment_price_net',
                'shipment_price_discount_net',
                'shipment_price_total_net',
                'gift_wrap_price_net',
                'gift_wrap_price_discount_net',
                'gift_wrap_price_total_net',
                'item_price_vat_rate',
                'item_price_vat',
                'item_price_discount_vat',
                'item_price_total_vat',
                'shipment_price_vat_rate',
                'shipment_price_vat',
                'shipment_price_discount_vat',
                'shipment_price_total_vat',
                'gift_wrap_price_vat_rate',
                'gift_wrap_price_vat',
                'gift_wrap_price_discount_vat',
                'gift_wrap_price_total_vat',
                'total_value_net',
                'total_value_vat',
                'total_value_gross',
                'transaction_currency_code',
                'invoice_currency_code',
                'invoice_exchange_rate_date',
                'invoice_exchange_rate',
                'invoice_amount_net',
                'invoice_amount_vat',
                'invoice_amount_gross',
                'reverse_charge_vat_rate',
                'invoice_amount_reverse_charge_vat',
                'arrival_seller_vatin',
                'departure_seller_vatin',
                'seller_vatin'
            ]
        )
        for transaction in transactions:
            customer_vatin = '{}-{}'.format(transaction.customer_vatin.country_code,
                                            transaction.customer_vatin.number) if transaction.customer_vatin_id else None,
            supplier_vatin = '{}-{}'.format(transaction.supplier_vatin.country_code,
                                            transaction.supplier_vatin.number) if transaction.supplier_vatin_id else None,
            arrival_seller_vatin = '{}-{}'.format(transaction.arrival_seller_vatin.country_code,
                                                  transaction.arrival_seller_vatin.number) if transaction.arrival_seller_vatin_id else None,
            departure_seller_vatin = '{}-{}'.format(transaction.departure_seller_vatin.country_code,
                                                    transaction.departure_seller_vatin.number) if transaction.departure_seller_vatin_id else None,
            seller_vatin = '{}-{}'.format(transaction.seller_vatin.country_code,
                                          transaction.seller_vatin.number) if transaction.seller_vatin_id else None,

            df = df.append(
                {
                    'created_on': str(transaction.created_on) if transaction.created_on else None,
                    'modified_at': str(transaction.modified_at) if transaction.modified_at else None,
                    'modified_by': transaction.modifier.name if transaction.modified_by else None,
                    'notifications': len(transaction.notifications) > 0,
                    'transaction_input': transaction.transaction_input.public_id if transaction.transaction_input_id else None,
                    'seller_firm': seller_firm_name if transaction.seller_firm_id else None,
                    'item': transaction.item.sku if transaction.item_id else None,
                    'type_code': transaction.type_code if transaction.type_code else None,
                    'amazon_vat_calculation_service': transaction.amazon_vat_calculation_service if transaction.amazon_vat_calculation_service else None,
                    'customer_relationship_checked': transaction.customer_relationship_checked if transaction.customer_relationship_checked else None,
                    'customer_relationship': transaction.customer_relationship if transaction.customer_relationship else None,
                    'customer_vatin': customer_vatin,
                    'supplier_relationship': transaction.supplier_relationship if transaction.supplier_relationship else None,
                    'supplier_vatin': supplier_vatin,
                    'tax_jurisdiction_code': transaction.tax_jurisdiction_code if transaction.tax_jurisdiction_code else None,
                    'arrival_country_code': transaction.arrival_country_code if transaction.arrival_country_code else None,
                    'departure_country_code': transaction.departure_country_code if transaction.departure_country_code else None,
                    'tax_treatment_code': transaction.tax_treatment_code if transaction.tax_treatment_code else None,
                    'tax_date': str(transaction.tax_date) if transaction.tax_date else None,
                    'tax_calculation_date': str(transaction.tax_calculation_date) if transaction.tax_calculation_date else None,
                    'item_tax_code_code': transaction.item_tax_code_code if transaction.item_tax_code_code else None,
                    'item_tax_rate_type_code': transaction.item_tax_rate_type_code if transaction.item_tax_rate_type_code else None,
                    'shipment_tax_rate_type_code': transaction.shipment_tax_rate_type_code if transaction.shipment_tax_rate_type_code else None,
                    'gift_wrap_tax_rate_type_code': transaction.gift_wrap_tax_rate_type_code if transaction.gift_wrap_tax_rate_type_code else None,
                    'item_price_net': transaction.item_price_net if transaction.item_price_net else None,
                    'item_price_discount_net': transaction.item_price_discount_net if transaction.item_price_discount_net else None,
                    'item_price_total_net': transaction.item_price_total_net if transaction.item_price_total_net else None,
                    'shipment_price_net': transaction.shipment_price_net if transaction.shipment_price_net else None,
                    'shipment_price_discount_net': transaction.shipment_price_discount_net if transaction.shipment_price_discount_net else None,
                    'shipment_price_total_net': transaction.shipment_price_total_net if transaction.shipment_price_total_net else None,
                    'gift_wrap_price_net': transaction.gift_wrap_price_net if transaction.gift_wrap_price_net else None,
                    'gift_wrap_price_discount_net': transaction.gift_wrap_price_discount_net if transaction.gift_wrap_price_discount_net else None,
                    'gift_wrap_price_total_net': transaction.gift_wrap_price_total_net if transaction.gift_wrap_price_total_net else None,
                    'item_price_vat_rate': transaction.item_price_vat_rate if transaction.item_price_vat_rate else None,
                    'item_price_vat': transaction.item_price_vat if transaction.item_price_vat else None,
                    'item_price_discount_vat': transaction.item_price_discount_vat if transaction.item_price_discount_vat else None,
                    'item_price_total_vat': transaction.item_price_total_vat if transaction.item_price_total_vat else None,
                    'shipment_price_vat_rate': transaction.shipment_price_vat_rate if transaction.shipment_price_vat_rate else None,
                    'shipment_price_vat': transaction.shipment_price_vat if transaction.shipment_price_vat else None,
                    'shipment_price_discount_vat': transaction.shipment_price_discount_vat if transaction.shipment_price_discount_vat else None,
                    'shipment_price_total_vat': transaction.shipment_price_total_vat if transaction.shipment_price_total_vat else None,
                    'gift_wrap_price_vat_rate': transaction.gift_wrap_price_vat_rate if transaction.gift_wrap_price_vat_rate else None,
                    'gift_wrap_price_vat': transaction.gift_wrap_price_vat if transaction.gift_wrap_price_vat else None,
                    'gift_wrap_price_discount_vat': transaction.gift_wrap_price_discount_vat if transaction.gift_wrap_price_discount_vat else None,
                    'gift_wrap_price_total_vat': transaction.gift_wrap_price_total_vat if transaction.gift_wrap_price_total_vat else None,
                    'total_value_net': transaction.total_value_net if transaction.total_value_net else None,
                    'total_value_vat': transaction.total_value_vat if transaction.total_value_vat else None,
                    'total_value_gross': transaction.total_value_gross if transaction.total_value_gross else None,
                    'transaction_currency_code': transaction.transaction_currency_code if transaction.transaction_currency_code else None,
                    'invoice_currency_code': transaction.invoice_currency_code if transaction.invoice_currency_code else None,
                    'invoice_exchange_rate_date': str(transaction.invoice_exchange_rate_date) if transaction.invoice_exchange_rate_date else None,
                    'invoice_exchange_rate': transaction.invoice_exchange_rate if transaction.invoice_exchange_rate else None,
                    'invoice_amount_net': transaction.invoice_amount_net if transaction.invoice_amount_net else None,
                    'invoice_amount_vat': transaction.invoice_amount_vat if transaction.invoice_amount_vat else None,
                    'invoice_amount_gross': transaction.invoice_amount_gross if transaction.invoice_amount_gross else None,
                    'reverse_charge_vat_rate': transaction.reverse_charge_vat_rate if transaction.reverse_charge_vat_rate else None,
                    'invoice_amount_reverse_charge_vat': transaction.invoice_amount_reverse_charge_vat if transaction.invoice_amount_reverse_charge_vat else None,
                    'arrival_seller_vatin': arrival_seller_vatin,
                    'departure_seller_vatin': departure_seller_vatin,
                    'seller_vatin': seller_vatin,
                },
                ignore_index=True
            )

        return df


    @staticmethod
    def separate_transactions_by_type(transactions: List[Transaction]) -> List[List[Transaction]]:
        sales = [transaction for transaction in transactions if transaction.type_code == 'SALE']
        refunds = [transaction for transaction in transactions if transaction.type_code == 'REFUND']
        acquisitions = [transaction for transaction in transactions if transaction.type_code == 'ACQUISITION']
        movements = [transaction for transaction in transactions if transaction.type_code == 'MOVEMENT']

        return (
            sales,
            refunds,
            acquisitions,
            movements
        )

    @staticmethod
    def separate_transactions_by_tax_treatment(transactions: List[Transaction]) -> List[List[Transaction]]:
        local_sales = [transaction for transaction in transactions if transaction.tax_treatment_code == 'LOCAL_SALE']
        local_sales_reverse_charge = [transaction for transaction in transactions if transaction.tax_treatment_code == 'LOCAL_SALE_REVERSE_CHARGE']
        distance_sales = [transaction for transaction in transactions if transaction.tax_treatment_code == 'DISTANCE_SALE']
        non_taxable_distance_sales = [transaction for transaction in transactions if transaction.tax_treatment_code == 'NON_TAXABLE_DISTANCE_SALE']
        intra_community_sales = [transaction for transaction in transactions if transaction.tax_treatment_code == 'INTRA_COMMUNITY_SALE']
        exports = [transaction for transaction in transactions if transaction.tax_treatment_code == 'EXPORT']
        local_acquisitions = [transaction for transaction in transactions if transaction.tax_treatment_code == 'LOCAL_ACQUISITION']
        intra_community_acquisitions = [transaction for transaction in transactions if transaction.tax_treatment_code == 'INTRA_COMMUNITY_ACQUISITION']

        return (
            local_sales,
            local_sales_reverse_charge,
            distance_sales,
            non_taxable_distance_sales,
            intra_community_sales,
            exports,
            local_acquisitions,
            intra_community_acquisitions
        )
