
import shutil
from pathlib import Path
from typing import List
from datetime import datetime, timedelta, date
import pandas as pd

from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound, RequestEntityTooLarge, UnsupportedMediaType
from app.extensions import db


from . import TransactionType, Transaction
from .interface import TransactionInterface

from ..account import Account
from ..distance_sale import DistanceSale, DistanceSaleHistory
from ..distance_sale.service import DistanceSaleService, DistanceSaleHistoryService
from ..transaction_input import TransactionInput
from ..transaction_input.interface import TransactionInputInterface
from ..bundle import Bundle
from ..bundle.service import BundleService
from ..item import Item, ItemHistory
from ..item.service import ItemService, ItemHistoryService
from ..country import Country, EU
from ..country.service import CountryService
from ..business.service_parent import BusinessService
from ..tax.vatin import VATIN
from ..tax.vatin.service import VATINService
from ..tax.tax_code.service import TaxCodeService
from ..tax.vat.service import VatService
from ..business.seller_firm import SellerFirm
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
    def get_by_tax_record_public_id(tax_record_public_id: str, **kwargs) -> List[Transaction]:
        from ..tax_record import TaxRecord
        base_query = Transaction.query.join(TaxRecord.transactions).filter(TaxRecord.public_id == tax_record_public_id).order_by(Transaction.tax_date.desc())

        if kwargs.get('paginate') == True and isinstance(kwargs.get('page'), int):
            per_page = current_app.config.TRANSACTIONS_PER_QUERY
            page = kwargs.get('page')
            transactions = base_query.paginate(page, per_page, False).items

        else:
            transactions = base_query.all()
        return transactions



    @staticmethod
    def create_transaction_s(transaction_input: TransactionInputInterface) -> Transaction:
        from ..account.service import AccountService
        from ..transaction_input.service import TransactionInputService

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
            transaction_type = TransactionService.get_transaction_type_by_public_code_account(transaction_input.transaction_type_public_code, platform_code)
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
            arrival_country = TransactionService.get_country(transaction_input, platform_code, bundle.id, transaction_type.code, country_type='arrival')
        except:
            SocketService.emit_status_error_unidentifiable_object(object_type, 'arrival country', current)
            return False

        try:
            departure_country = TransactionService.get_country(transaction_input, platform_code, bundle.id, transaction_type.code, country_type='departure')
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

        if transaction_type.code == 'MOVEMENT' or transaction_type.code == 'RETURN':
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
        tax_calculation_date = TransactionService.get_tax_calculation_date(transaction_input.tax_calculation_date, tax_date, transaction_type.code, platform_code, bundle.id)
        tax_jurisdiction: Country = TransactionService.get_tax_jurisdiction(tax_treatment_code, departure_country, arrival_country)

        item_history = ItemHistoryService.get_by_item_id_date(item.id, tax_date)

        item_tax_code_code, calculated_item_tax_code_code = TransactionService.get_item_tax_code_code(transaction_input, item_history.tax_code_code, platform_code, reference_tax_code=transaction_input.item_tax_code_code)
        item_vat_temp = VatService.get_by_tax_code_country_tax_date(item_tax_code_code, tax_jurisdiction.code, tax_date)
        item_tax_rate_type_code=item_vat_temp.tax_rate_type_code

        shipment_tax_rate_type_code = current_app.config.STANDARD_SERVICE_TAX_RATE_TYPE
        shipment_vat_temp = VatService.get_by_tax_rate_type_country_tax_date(tax_jurisdiction.code, shipment_tax_rate_type_code, tax_date)
        gift_wrap_tax_rate_type_code = current_app.config.STANDARD_SERVICE_TAX_RATE_TYPE
        gift_wrap_vat_temp = VatService.get_by_tax_rate_type_country_tax_date(tax_jurisdiction.code, shipment_tax_rate_type_code, tax_date)

        item_price_vat_rate: float = TransactionService.get_vat_rate(transaction_input, tax_jurisdiction, tax_treatment_code, tax_date, tax_rate_type_code=item_tax_rate_type_code, reference_vat_rate=item_vat_temp.rate, calculated_vat_rate=item_vat_temp.rate)
        gift_wrap_price_vat_rate: float = TransactionService.get_vat_rate(transaction_input, tax_jurisdiction, tax_treatment_code, tax_date, tax_rate_type_code=shipment_tax_rate_type_code, calculated_vat_rate=gift_wrap_vat_temp.rate)
        shipment_price_vat_rate: float = TransactionService.get_vat_rate(transaction_input, tax_jurisdiction, tax_treatment_code, tax_date, tax_rate_type_code=gift_wrap_tax_rate_type_code, calculated_vat_rate=shipment_vat_temp.rate)

        item_price_net: float = TransactionService.get_price_net(item_history, transaction_input.item_price_gross, item_price_vat_rate, transaction_type, price_type='item', discount=False)
        item_price_discount_net: float = TransactionService.get_price_net(item_history, transaction_input.item_price_discount_gross, item_price_vat_rate, transaction_type, price_type='item', discount=True)
        item_price_total_net: float = TransactionService.get_price_net(item_history, transaction_input.item_price_total_gross, item_price_vat_rate, transaction_type, price_type='item', discount=False)

        shipment_price_net: float = TransactionService.get_price_net(item_history, transaction_input.shipment_price_gross, shipment_price_vat_rate, transaction_type, price_type='shipment', discount=False)
        shipment_price_discount_net: float = TransactionService.get_price_net(item_history, transaction_input.shipment_price_discount_gross, shipment_price_vat_rate, transaction_type, price_type='shipment', discount=True)
        shipment_price_total_net: float = TransactionService.get_price_net(item_history, transaction_input.shipment_price_total_gross, shipment_price_vat_rate, transaction_type, price_type='shipment', discount=False)

        gift_wrap_price_net: float = TransactionService.get_price_net(item_history, transaction_input.gift_wrap_price_gross, gift_wrap_price_vat_rate, transaction_type, price_type='gift_wrap', discount=False)
        gift_wrap_price_discount_net: float = TransactionService.get_price_net(item_history, transaction_input.gift_wrap_price_discount_gross, gift_wrap_price_vat_rate, transaction_type, price_type='gift_wrap', discount=True)
        gift_wrap_price_total_net: float = TransactionService.get_price_net(item_history, transaction_input.gift_wrap_price_total_gross, gift_wrap_price_vat_rate, transaction_type, price_type='gift_wrap', discount=False)

        item_price_vat: float = TransactionService.get_price_vat(transaction_input.item_price_gross, item_price_vat_rate, transaction_type)
        item_price_discount_vat: float = TransactionService.get_price_vat(transaction_input.item_price_discount_gross, item_price_vat_rate, transaction_type)
        item_price_total_vat: float = TransactionService.get_price_vat(transaction_input.item_price_total_gross, item_price_vat_rate, transaction_type)

        shipment_price_vat: float = TransactionService.get_price_vat(transaction_input.shipment_price_gross, shipment_price_vat_rate, transaction_type)
        shipment_price_discount_vat: float = TransactionService.get_price_vat(transaction_input.shipment_price_discount_gross, shipment_price_vat_rate, transaction_type)
        shipment_price_total_vat: float = TransactionService.get_price_vat(transaction_input.shipment_price_total_gross, shipment_price_vat_rate, transaction_type)

        gift_wrap_price_vat: float = TransactionService.get_price_vat(transaction_input.gift_wrap_price_gross, gift_wrap_price_vat_rate, transaction_type)
        gift_wrap_price_discount_vat: float = TransactionService.get_price_vat(transaction_input.gift_wrap_price_discount_gross, gift_wrap_price_vat_rate, transaction_type)
        gift_wrap_price_total_vat: float = TransactionService.get_price_vat(transaction_input.gift_wrap_price_total_gross, gift_wrap_price_vat_rate, transaction_type)

        total_value_net: float = TransactionService.get_total_value(transaction_input.item_quantity, transaction_type, item_price_total_net, shipment_price_total_net, gift_wrap_price_total_net, item_price_total_net)
        total_value_vat: float = TransactionService.get_total_value(transaction_input.item_quantity, transaction_type, item_price_total_vat, shipment_price_total_vat, gift_wrap_price_total_vat, item_price_total_vat)
        total_value_gross: float = TransactionService.get_total_value(transaction_input.item_quantity, transaction_type, transaction_input.item_price_total_gross, transaction_input.shipment_price_total_gross, transaction_input.gift_wrap_price_total_gross, item_price_total_net)
        # !!! comment: first total_value_gross dann daraus total_value_vat und total_value_net

        transaction_currency_code: str = TransactionService.get_transaction_currency(item_history.unit_cost_price_currency_code, transaction_type, transaction_input.currency_code)


        invoice_currency_code: str = TransactionService.get_invoice_currency_code(departure_country, tax_jurisdiction, tax_treatment_code)
        invoice_exchange_rate_date: date = TransactionService.get_invoice_exchange_rate_date(platform_code, transaction_type, bundle.id, transaction_currency_code, invoice_currency_code, tax_date)
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
        if arrival_seller_vatin in seller_firm.vat_numbers and arrival_seller_vatin.initial_tax_date == None:
            arrival_seller_vatin.initial_tax_date == tax_date
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise

        if departure_seller_vatin in seller_firm.vat_numbers and departure_seller_vatin.initial_tax_date == None:
            departure_seller_vatin.initial_tax_date == tax_date
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise

        if seller_vatin in seller_firm.vat_numbers and seller_vatin.initial_tax_date == None:
            seller_vatin.initial_tax_date == tax_date
            try:
                db.session.commit()
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
        VatService.compare_reference_calculated_vat_rates(transaction_id, transaction_input, reference_vat_rate=reference_vat_rate, calculated_vat_rate=calculated_vat_rate)
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

                if departure_country_code != arrival_country.code and distance_sale_history_active:
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
    def get_country(transaction_input: TransactionInput, platform_code: str, bundle_id: int, transaction_type_code: str, country_type: str) -> Country:
        if transaction_type_code == 'REFUND':
            sale_transaction = TransactionService.get_sale_transaction_by_platform_code_bundle_id(platform_code, bundle_id)
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
    def get_transaction_type_by_public_code_account(transaction_type_public_code: str, platform_code: str) -> TransactionType:
        if platform_code == 'AMZ':
            if transaction_type_public_code == 'SALE' or transaction_type_public_code == 'COMMINGLING_SELL':
                transaction_type = TransactionType.query.filter_by(code="SALE").first()

            elif transaction_type_public_code == 'REFUND':
                transaction_type = TransactionType.query.filter_by(code="REFUND").first()

            elif transaction_type_public_code == 'RETURN':
                transaction_type = TransactionType.query.filter_by(code="RETURN").first()

            elif transaction_type_public_code == 'COMMINGLING_BUY':
                transaction_type = TransactionType.query.filter_by(code="ACQUISITION").first()

            elif transaction_type_public_code == 'FC_TRANSFER':
                transaction_type = TransactionType.query.filter_by(code="MOVEMENT").first()

            elif transaction_type_public_code == 'INBOUND':
                transaction_type = TransactionType.query.filter_by(code="INBOUND").first()

            else:
                print("Function: TransactionService -> get_transaction_type_by_public_code_account", flush=True)
                raise NotFound('The indicated transaction type "{}" is not supported. Please get in touch with one of the administrators.'.format(transaction_type_public_code))
                current_app.logger.warning('Unrecognized public transaction type code: {}'.format(transaction_type_public_code))

        else:
            print("Function: TransactionService -> get_transaction_type_by_public_code_account -> platform not found", flush=True)
            raise NotFound('The platform for the transaction code "{}" is currently not supported. Please get in touch with one of the admins.'.format(transaction_type_public_code))

        return transaction_type


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
    def get_transaction_currency(item_history_unit_cost_price_currency_code: str, transaction_type: TransactionType, input_currency_code: str) -> str:

        if transaction_type.code=="MOVEMENT" or transaction_type.code=="INBOUND" or transaction_type.code=='RETURN':
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
            reverse_charge_vat_rate = VatService.get_by_tax_code_country_tax_date(tax_code_code, arrival_country_code, tax_date).rate

        return reverse_charge_vat_rate


    @staticmethod
    def get_sale_transaction_by_platform_code_bundle_id(platform_code: str, bundle_id: int) -> Transaction:
        from app.namespaces.transaction_input.service import TransactionInputService

        if platform_code == 'AMZ':
            sale_transaction_input = TransactionInputService.get_sale_transaction_input_by_bundle_id(bundle_id)
            if sale_transaction_input:
                sale_transaction=TransactionService.get_by_transaction_input_id(sale_transaction_input.id)

                return sale_transaction




    @staticmethod
    def get_invoice_amount(total_value: float, invoice_exchange_rate: float) -> float:
        invoice_amount = float(total_value) * float(invoice_exchange_rate)
        return invoice_amount



    @staticmethod
    def get_invoice_exchange_rate_date(platform_code: str, transaction_type: TransactionType, bundle_id: int, transaction_currency_code: str, invoice_currency_code: str, tax_date: date) -> date:
        if TransactionService.check_exchange_rate_required(transaction_currency_code, invoice_currency_code):

            if transaction_type.code == "REFUND":
                sale_transaction = TransactionService.get_sale_transaction_by_platform_code_bundle_id(platform_code, bundle_id)
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
            from ..exchange_rate.service import ExchangeRateService
            invoice_exchange_rate = ExchangeRateService.get_by_base_target_date(base=transaction_currency_code, target=invoice_currency_code, date=invoice_exchange_rate_date).rate

        else:
            invoice_exchange_rate = float(1)

        return invoice_exchange_rate


    @staticmethod
    def check_exchange_rate_required(transaction_currency_code: str, invoice_currency_code: str) -> bool:
        return transaction_currency_code != invoice_currency_code





    @staticmethod
    def get_price_net(item_history: ItemHistory, price_gross: float, price_tax_rate: float, transaction_type: TransactionType, price_type: str, discount: bool) -> float:
        if transaction_type.code == 'MOVEMENT' or transaction_type.code == 'INBOUND':
            if discount:
                price_net = float(0)

            else:
                if price_type=='item':
                    price_net = float(item_history.unit_cost_price_net)

                elif price_type=='shipment' or price_type=='gift_wrap':
                    price_net = float(0)

        else:
            price_net = float(price_gross) / (1 + float(price_tax_rate))

        return price_net


    @staticmethod
    def get_price_vat(price_gross: float, price_tax_rate: float, transaction_type: TransactionType) -> float:
        if transaction_type.code == 'MOVEMENT' or transaction_type.code == 'INBOUND':
            price_vat = float(0)

        else:
            price_vat = float(price_gross) / (1 + float(price_tax_rate)) * float(price_tax_rate)
        return price_vat



    @staticmethod
    def get_total_value(item_quantity: int, transaction_type: TransactionType, item_price_total: float, shipment_price_total: float, gift_wrap_price_total: float, item_unit_cost_price: float) -> float:
        if transaction_type.code == 'MOVEMENT' or transaction_type.code == 'INBOUND':
            return item_unit_cost_price * item_quantity

        else:
            return item_price_total + shipment_price_total + gift_wrap_price_total


    @staticmethod
    def check_amazon_vat_calculation_service(check_tax_calculation_date: date) -> bool:
        return isinstance(check_tax_calculation_date, date)

    @staticmethod
    def get_tax_calculation_date(check_tax_calculation_date: date, tax_date: date, transaction_type_code: str, platform_code: str, bundle_id: int) -> date:
        if isinstance(check_tax_calculation_date, date):
            tax_calculation_date = check_tax_calculation_date

        else:
            if transaction_type_code == 'REFUND':
                sale_transaction = TransactionService.get_sale_transaction_by_platform_code_bundle_id(platform_code, bundle_id)
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
