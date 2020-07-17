
import shutil
from pathlib import Path
from typing import List
from datetime import datetime, timedelta, date
import pandas as pd
from decimal import Decimal

from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound, RequestEntityTooLarge, UnsupportedMediaType
from app.extensions import db


from . import TransactionType, Transaction

from ..account import Account
from ..transaction_input import TransactionInput
from ..transaction_input.interface import TransactionInputInterface
from ..bundle import Bundle
from ..bundle.service import BundleService
from ..item import Item
from ..item.service import ItemService
from ..country import Country, EU
from ..country.service import CountryService
from ..business.customer_firm import CustomerFirm
from ..business.customer_firm.service import CustomerFirmService
from ..tax.vatin import VATIN
from ..business.seller_firm import SellerFirm
from ..utils.service import HelperService, NotificationService





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
    def create_transaction_s(transaction_input_data: TransactionInputInterface) -> Transaction:
        from ..account.service import AccountService
        from ..transaction_input.service import TransactionInputService

        print("", flush=True)

        account_given_id = transaction_input_data.get('account_given_id')
        channel_code = transaction_input_data.get('channel_code')
        given_id = transaction_input_data.get('given_id')
        activity_id = transaction_input_data.get('activity_id')
        item_sku = transaction_input_data.get('item_sku')

        transaction_input = TransactionInputService.get_by_identifiers(account_given_id, channel_code, given_id, activity_id, item_sku)

        account = AccountService.get_by_given_id_channel_code(transaction_input.account_given_id, transaction_input.channel_code)
        transaction_type = TransactionService.get_transaction_type_by_public_code_account(transaction_input.transaction_type_public_code, account)

        # define foundational vars
        tax_date = TransactionService.get_tax_date(transaction_type, transaction_input)
        item = ItemService.get_by_sku_account_date(transaction_input.item_sku, account, tax_date)
        bundle = BundleService.get_by_id(transaction_input.bundle_id)
        arrival_country = CountryService.get_by_code(transaction_input.arrival_country_code)
        departure_country = CountryService.get_by_code(transaction_input.departure_country_code)
        eu = CountryService.get_eu_by_date(tax_date)

        customer_vat_check_required: bool = TransactionService.vat_check_required(transaction_input, date=tax_date, number=transaction_input.customer_firm_vat_number)

        amazon_vat_calculation_service: bool = TransactionService.check_amazon_vat_calculation_service(transaction_input.check_tax_calculation_date)

        print('transaction_input.customer_firm_vat_number_country_code: ', transaction_input.customer_firm_vat_number_country_code, flush=True)
        print('transaction_input.customer_firm_vat_number: ', transaction_input.customer_firm_vat_number, flush=True)

        customer_firm_vatin: VATIN = CustomerFirmService.get_vatin_or_None(customer_vat_check_required, country_code_temp=transaction_input.customer_firm_vat_number_country_code, number_temp=transaction_input.customer_firm_vat_number, date=tax_date)
        customer_relationship, customer_relationship_checked = CustomerFirmService.get_customer_relationship(customer_firm_vatin, check_required=customer_vat_check_required)


        print("Transaction Type Code", transaction_type.code, flush=True)
        print('customer_firm_vatin: ', customer_firm_vatin, flush=True)
        print('customer_relationship: ', customer_relationship, flush=True)

        if transaction_type.code == 'SALE' or transaction_type.code == 'REFUND':
            print('CASE SALE', flush=True)
            tax_treatment_code = TransactionService.get_tax_treatment_code(transaction_type, account, transaction_input, eu, customer_relationship, departure_country, arrival_country, amazon_vat_calculation_service, tax_date)
            print("tax_treatment_code:", tax_treatment_code, flush=True)

            new_transaction = TransactionService.calculate_transaction_vars(transaction_input, transaction_type, account, tax_treatment_code, tax_date, item, bundle, arrival_country, departure_country, eu, customer_relationship, customer_firm_vatin, customer_relationship_checked, amazon_vat_calculation_service)

            # check for special case: non taxable distance sale
            if new_transaction.tax_treatment_code == 'DISTANCE_SALE':
                tax_treatment_code = 'NON_TAXABLE_DISTANCE_SALE'
                new_non_taxable_distance_sale = TransactionService.calculate_transaction_vars(transaction_input, transaction_type, account, tax_treatment_code, tax_date, item, bundle, arrival_country, departure_country, eu, customer_relationship, customer_firm_vatin, customer_relationship_checked, amazon_vat_calculation_service)

        elif transaction_type.code == 'RETURN':
            pass

        elif transaction_type.code == 'ACQUISITION':
            tax_treatment_code: str = TransactionService.get_tax_treatment_code(transaction_type, account, transaction_input, eu, customer_relationship, departure_country, arrival_country, amazon_vat_calculation_service, tax_date)
            new_transaction = TransactionService.calculate_transaction_vars(transaction_input, transaction_type, account, tax_treatment_code, tax_date, item, bundle, arrival_country, departure_country, eu, customer_relationship, customer_firm_vatin, customer_relationship_checked, amazon_vat_calculation_service)


        elif transaction_type.code == 'MOVEMENT' or transaction_type.code == 'INBOUND':
            tax_treatment_codes = ['INTRA_COMMUNITY_SALE', 'INTRA_COMMUNITY_ACQUISITION']
            for tax_treatment_code in tax_treatment_codes:
                new_transaction = TransactionService.calculate_transaction_vars(transaction_input, transaction_type, account, tax_treatment_code, tax_date, item, bundle, arrival_country, departure_country, eu, customer_relationship, customer_firm_vatin, customer_relationship_checked, amazon_vat_calculation_service)

        transaction_input.update_processed()
        db.session.commit()




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
            customer_firm_vatin: VATIN,
            customer_relationship_checked: bool,
            amazon_vat_calculation_service: bool):

        from ..tax.vatin.service import VATINService
        from ..tax.vat.service import VatService
        print("Here we go TransactionService: calculate_transaction_vars", flush=True)

        customer_firm: CustomerFirm = CustomerFirmService.get_customer_firm_or_None(customer_firm_vatin, customer_relationship)

        tax_calculation_date = TransactionService.get_tax_calculation_date(transaction_input.check_tax_calculation_date, tax_date)
        tax_jurisdiction: Country = TransactionService.get_tax_jurisdiction(tax_treatment_code, departure_country, arrival_country)

        item_tax_code_code: str = TransactionService.get_item_tax_code_code(transaction_input, item, account, reference_tax_code=transaction_input.check_item_tax_code_code)
        item_vat_temp = VatService.get_by_tax_code_country_tax_date(item_tax_code_code, tax_jurisdiction, tax_date)
        item_tax_rate_type_code=item_vat_temp.tax_rate_type_code

        shipment_tax_rate_type_code = current_app.config['STANDARD_SERVICE_TAX_RATE_TYPE']
        shipment_vat_temp = VatService.get_by_tax_rate_type_country_tax_date(tax_jurisdiction, shipment_tax_rate_type_code, tax_date)
        gift_wrap_tax_rate_type_code = current_app.config['STANDARD_SERVICE_TAX_RATE_TYPE']
        gift_wrap_vat_temp = VatService.get_by_tax_rate_type_country_tax_date(tax_jurisdiction, shipment_tax_rate_type_code, tax_date)


        item_price_vat_rate: float = TransactionService.get_vat_rate(transaction_input, tax_jurisdiction, tax_treatment_code, tax_date, tax_rate_type_code=item_tax_rate_type_code, reference_vat_rate=item_vat_temp.rate, calculated_vat_rate=item_vat_temp.rate)
        gift_wrap_price_vat_rate: float = TransactionService.get_vat_rate(transaction_input, tax_jurisdiction, tax_treatment_code, tax_date, tax_rate_type_code=shipment_tax_rate_type_code, calculated_vat_rate=gift_wrap_vat_temp.rate)
        shipment_price_vat_rate: float = TransactionService.get_vat_rate(transaction_input, tax_jurisdiction, tax_treatment_code, tax_date, tax_rate_type_code=gift_wrap_tax_rate_type_code, calculated_vat_rate=shipment_vat_temp.rate)

        item_price_net: float = TransactionService.get_price_net(transaction_input.item_price_gross, item_price_vat_rate)
        item_price_discount_net: float = TransactionService.get_price_net(transaction_input.item_price_discount_gross, item_price_vat_rate)
        item_price_total_net: float = TransactionService.get_price_net(transaction_input.item_price_total_gross, item_price_vat_rate)

        shipment_price_net: float = TransactionService.get_price_net(transaction_input.shipment_price_gross, shipment_price_vat_rate)
        shipment_price_discount_net: float = TransactionService.get_price_net(transaction_input.shipment_price_discount_gross, shipment_price_vat_rate)
        shipment_price_total_net: float = TransactionService.get_price_net(transaction_input.shipment_price_total_gross, shipment_price_vat_rate)

        gift_wrap_price_net: float = TransactionService.get_price_net(transaction_input.gift_wrap_price_gross, gift_wrap_price_vat_rate)
        gift_wrap_price_discount_net: float = TransactionService.get_price_net(transaction_input.gift_wrap_price_discount_gross, gift_wrap_price_vat_rate)
        gift_wrap_price_total_net: float = TransactionService.get_price_net(transaction_input.gift_wrap_price_total_gross, gift_wrap_price_vat_rate)

        item_price_vat: float = TransactionService.get_price_vat(transaction_input.item_price_gross, item_price_vat_rate)
        item_price_discount_vat: float = TransactionService.get_price_vat(transaction_input.item_price_discount_gross, item_price_vat_rate)
        item_price_total_vat: float = TransactionService.get_price_vat(transaction_input.item_price_total_gross, item_price_vat_rate)

        shipment_price_vat: float = TransactionService.get_price_vat(transaction_input.shipment_price_gross, shipment_price_vat_rate)
        shipment_price_discount_vat: float = TransactionService.get_price_vat(transaction_input.shipment_price_discount_gross, shipment_price_vat_rate)
        shipment_price_total_vat: float = TransactionService.get_price_vat(transaction_input.shipment_price_total_gross, shipment_price_vat_rate)

        gift_wrap_price_vat: float = TransactionService.get_price_vat(transaction_input.gift_wrap_price_gross, gift_wrap_price_vat_rate)
        gift_wrap_price_discount_vat: float = TransactionService.get_price_vat(transaction_input.gift_wrap_price_discount_gross, gift_wrap_price_vat_rate)
        gift_wrap_price_total_vat: float = TransactionService.get_price_vat(transaction_input.gift_wrap_price_total_gross, gift_wrap_price_vat_rate)

        total_value_net: float = TransactionService.get_total_value(item, transaction_input.item_quantity, transaction_type, item_price_total_net, shipment_price_total_net, gift_wrap_price_total_net)
        total_value_vat: float = TransactionService.get_total_value(item, transaction_input.item_quantity, transaction_type, item_price_total_vat, shipment_price_total_vat, gift_wrap_price_total_vat)
        total_value_gross: float = TransactionService.get_total_value(item, transaction_input.item_quantity, transaction_type, transaction_input.item_price_total_gross, transaction_input.shipment_price_total_gross, transaction_input.gift_wrap_price_total_gross)

        transaction_currency_code: str = TransactionService.get_transaction_currency(item, transaction_type, transaction_input.currency_code)

        invoice_currency_code: str = TransactionService.get_invoice_currency_code(departure_country, tax_jurisdiction, tax_treatment_code)
        invoice_exchange_rate_date: date = TransactionService.get_invoice_exchange_rate_date(account, transaction_type, bundle, transaction_currency_code, invoice_currency_code, tax_date)
        invoice_exchange_rate: float = TransactionService.get_invoice_exchange_rate(invoice_exchange_rate_date=invoice_exchange_rate_date, transaction_currency_code=transaction_currency_code, invoice_currency_code=invoice_currency_code)

        invoice_amount_net: float = TransactionService.get_invoice_amount(total_value_net, invoice_exchange_rate)
        invoice_amount_vat: float = TransactionService.get_invoice_amount(total_value_vat, invoice_exchange_rate)
        invoice_amount_gross: float = TransactionService.get_invoice_amount(total_value_gross, invoice_exchange_rate)

        vat_rate_reverse_charge: float = TransactionService.get_vat_rate_reverse_charge(transaction_input, arrival_country, tax_treatment_code, tax_date, tax_rate_type_code=item_tax_rate_type_code)
        invoice_amount_vat_reverse_charge: float = TransactionService.get_invoice_amount_vat_reverse_charge(invoice_amount_net, vat_rate_reverse_charge)


        arrival_seller_vatin: VATINService.get_vatin_or_None_and_verify(transaction_input, arrival_country.vat_country_code, transaction_input.check_arrival_seller_vat_number, date=tax_date)
        departure_seller_vatin: VATINService.get_vatin_or_None_and_verify(transaction_input, departure_country.vat_country_code, transaction_input.check_departure_seller_vat_number, date=tax_date)
        seller_vatin: VATINService.get_vatin_or_None_and_verify(transaction_input, tax_jurisdiction.vat_country_code, transaction_input.check_seller_vat_number, date=tax_date)


        TransactionService.create_notifications(transaction_input, item, customer_firm_vatin, tax_calculation_date, invoice_currency_code)



        transaction_data= {
            'account_id': account.id,

            'type_code': transaction_type.code,
            'amazon_vat_calculation_service': amazon_vat_calculation_service,

            'customer_relationship_checked': customer_relationship_checked,
            'customer_relationship': customer_relationship,
            'customer_firm_id': customer_firm.id if customer_firm else None,
            'customer_firm_vatin_id': customer_firm_vatin.id if customer_firm_vatin else None,

            'tax_jurisdiction_code': tax_jurisdiction.code,

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

            'gift_wrap_vat_rate': gift_wrap_vat_rate,
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

            'vat_rate_reverse_charge': vat_rate_reverse_charge,
            'invoice_amount_vat_reverse_charge': invoice_amount_vat_reverse_charge,


            'arrival_seller_vatin_id': arrival_seller_vatin.id,
            'departure_seller_vatin_id': departure_seller_vatin.id,
            'seller_vatin_id': seller_vatin.id

        }

        print("", flush=True)
        print("transaction_data:", transaction_data, flush=True)
        print("", flush=True)


        try:
            new_transaction = TransactionService.create_transaction(transaction_data)

        except:
            db.session.rollback()



        return new_transaction


        def create_transaction(transaction_data: TransactionInterface) -> Transaction:
            new_transaction = Transaction(
                account_id = transaction_data.get('account_id'),
                transaction_type = transaction_data.get('transaction_type'),
                amazon_vat_calculation_service = transaction_data.get('amazon_vat_calculation_service'),
                customer_relationship_checked = transaction_data.get('customer_relationship_checked'),
                customer_relationship = transaction_data.get('customer_relationship'),
                customer_firm_id = transaction_data.get('customer_firm_id'),
                customer_firm_vatin_id = transaction_data.get('customer_firm_vatin_id'),
                tax_jurisdiction_code = transaction_data.get('tax_jurisdiction_code'),
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
                gift_wrap_vat_rate = transaction_data.get('gift_wrap_vat_rate'),
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
                vat_rate_reverse_charge = transaction_data.get('vat_rate_reverse_charge'),
                invoice_amount_vat_reverse_charge = transaction_data.get('invoice_amount_vat_reverse_charge'),
                arrival_seller_vatin_id = transaction_data.get('arrival_seller_vatin_id'),
                departure_seller_vatin_id = transaction_data.get('departure_seller_vatin_id'),
                seller_vatin_id = transaction_data.get('seller_vatin_id')
            )

            db.session.add(new_transaction)
            db.session.commit()

            return new_transaction


    @staticmethod
    def create_notifications(transaction_input: TransactionInput, item: Item, customer_firm_vatin: VATIN, tax_calculation_date: date, invoice_currency_code) -> None:
        ItemService.compare_calculation_reference(transaction_input, item)
        CustomerFirmService.compare_calculation_reference(transaction_input, customer_firm_vatin)
        TransactionService.compare_calculation_reference_tax_calculation_date(transaction_input, tax_calculation_date)
        TransactionService.compare_calculation_reference_invoice_currency_code(transaction_input, invoice_currency_code)


    @staticmethod
    def compare_calculation_reference_tax_calculation_date(transaction_input: TransactionInput, tax_calculation_date: date) -> None:
        if transaction_input.check_tax_calculation_date and transaction_input.check_tax_calculation_date != tax_calculation_date:
            notification_data = NotificationService.create_notification_data(main_subject='Tax Calculation Date', original_filename=transaction_input.original_filename, status='warning', reference_value=transaction_input.check_tax_calculation_date, calculated_value=tax_calculation_date, transaction_input_id=transaction_input.id)
            NotificationService.create_transaction_notification(notification_data)

    @staticmethod
    def compare_calculation_reference_invoice_currency_code(transaction_input: TransactionInput, invoice_currency_code: str) -> None:
        if transaction_input.check_invoice_currency_code and transaction_input.check_invoice_currency_code != invoice_currency_code:
            notification_data = NotificationService.create_notification_data(main_subject='Invoice Currency Code', original_filename=transaction_input.original_filename, status='warning', reference_value=transaction_input.check_invoice_currency_code, calculated_value=invoice_currency_code, transaction_input_id=transaction_input.id)
            NotificationService.create_transaction_notification(notification_data)




    @staticmethod
    def get_tax_treatment_code(
            transaction_type: TransactionType,
            account: Account,
            transaction_input: TransactionInput,
            eu: EU,
            customer_relationship: str,
            departure_country: Country,
            arrival_country: Country,
            amazon_vat_calculation_service: bool,
            tax_date: date,
            **kwargs) -> str:
        from ..distance_sale.service import DistanceSaleService

        if transaction_type.code == 'SALE' or transaction_type.code == 'REFUND':

            if (transaction_input.check_export or arrival_country not in eu.countries):
                tax_treatment_code = 'EXPORT'

            elif customer_relationship == "B2B":
                if departure_country.code != arrival_country.code:
                    tax_treatment_code = 'INTRA_COMMUNITY_SALE'

                else:
                    if (
                    (departure_country.code in ['ES', 'FR', 'IT', 'PL'] and departure_country.code != account.seller_firm.establishment_country_code) or
                    (amazon_vat_calculation_service and transaction_input.check_item_price_vat_rate == 0)
                    ):
                        tax_treatment_code = 'LOCAL_SALE_REVERSE_CHARGE'

                    else:
                        tax_treatment_code='LOCAL_SALE'


            elif customer_relationship == "B2C":
                if departure_country.code != arrival_country.code and DistanceSaleService.get_status(platform_code=account.channel.platform_code, seller_firm_id=account.seller_firm_id, arrival_country_code=arrival_country.code, tax_date=tax_date):
                    tax_treatment_code = 'DISTANCE_SALE'

                else:
                    tax_treatment_code = 'LOCAL_SALE'

        elif transaction_type.code == 'ACQUISITION':
            tax_treatment_code = 'DOMESTIC_ACQUISITION'

        elif transaction_type.code == 'MOVEMENT' or transaction_type.code == 'INBOUND':
            tax_treatment_code = kwargs.get('tax_treatment_code')

        return tax_treatment_code




    @staticmethod
    def get_by_validity_public_id(start_date_str: str, end_date_str: str, seller_firm_public_id: str, tax_jurisdiction_code: str) -> List[Transaction]:

        seller_firm = SellerFirm.query.filter_by(public_id = seller_firm_public_id).first()
        date_start: date = HelperService.get_date_from_str(start_date_str, '%d-%m-%Y')
        date_end: date = HelperService.get_date_from_str(end_date_str, '%d-%m-%Y')

        transactions = Transaction.query.filter(Transaction.account.has(seller_firm_id=seller_firm.id), Transaction.date>=date_start, Transaction.date<=date_end, Transaction.tax_jurisdiction_code==tax_jurisdiction_code).all()
        return transactions


    @staticmethod
    def vat_check_required(transaction_input: TransactionInput, date: date, number: str) -> bool:
        OLD_TRANSACTION_TOLERANCE_DAYS = current_app.config['OLD_TRANSACTION_TOLERANCE_DAYS']
        if not number:
            return False
        else:
            result: bool = date.today() - timedelta(days=OLD_TRANSACTION_TOLERANCE_DAYS) <= date

            if not result:
                notification_data = {
                    'subject': 'Old Transaction',
                    'original_filename': transaction_input.original_filename,
                    'status': 'info',
                    'message': 'Due to the age (>{} days) of the tax date the customer firm VAT Number ({}) it is assumed to be valid without further checks.'.format(OLD_TRANSACTION_TOLERANCE_DAYS, number),
                    'transaction_input_id': transaction_input.id
                }
                try:
                    NotificationService.create_transaction_notification(notification_data)
                except:
                    db.session.rollback()
                    raise

            return result



    @staticmethod
    def get_vat_rate(transaction_input: TransactionInput, tax_jurisdiction: Country, tax_treatment_code: str, tax_date: date, tax_rate_type_code: str, **kwargs) -> float:
        print("", flush=True)
        print('Enter get_vat_rate:', flush=True)
        print('transaction_input:', transaction_input, flush=True)
        print('tax_jurisdiction:', tax_jurisdiction, flush=True)
        print('tax_rate_type_code:', tax_rate_type_code, flush=True)
        print('calculated_vat_rate:', kwargs.get('calculated_vat_rate'), flush=True)
        print('type calculated_vat_rate:', type(kwargs.get('calculated_vat_rate')), flush=True)
        print('reference_vat_rate:', kwargs.get('reference_vat_rate'), flush=True)
        print('type reference_vat_rate:', type(kwargs.get('reference_vat_rate')), flush=True)
        print("isinstance(kwargs.get('calculated_vat_rate'), (Decimal)): ", isinstance(kwargs.get('calculated_vat_rate'), (Decimal)), flush=True)
        print("isinstance(kwargs.get('reference_vat_rate'), (Decimal)): ", isinstance(kwargs.get('reference_vat_rate'), (Decimal)), flush=True)


        if tax_treatment_code == 'EXPORT' or tax_treatment_code == 'INTRA_COMMUNITY_SALE' or tax_treatment_code == 'LOCAL_SALE_REVERSE_CHARGE' or tax_treatment_code == 'INTRA_COMMUNITY_ACQUISITION':
            calculated_vat_rate=float(0)

        elif isinstance(kwargs.get('calculated_vat_rate'), (Decimal, int, float, complex)) and not isinstance(kwargs.get('calculated_vat_rate'), bool):
            calculated_vat_rate=kwargs['calculated_vat_rate']

        else:
            raise

        if isinstance(kwargs.get('reference_vat_rate'), (Decimal, int, float, complex)) and not isinstance(kwargs.get('reference_vat_rate'), bool):
            # print('Check reference_vat_rate float', flush=True)
            reference_vat_rate=kwargs['reference_vat_rate']
            if calculated_vat_rate != reference_vat_rate:
                notification_data = NotificationService.create_notification_data(main_subject='Tax Rate', original_filename=transaction_input.original_filename, status='warning', reference_value=str(reference_vat_rate), calculated_value=str(calculated_vat_rate), transaction_input_id=transaction_input.id)
                try:
                    NotificationService.create_transaction_notification(notification_data)
                except:
                    db.session.rollback()
                    raise

                vat_rate=reference_vat_rate

            else:
                vat_rate = calculated_vat_rate

        else:
            vat_rate=calculated_vat_rate

        print('vat_rate: ', vat_rate, flush=True)
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

        else:
            raise

        return tax_date




    @staticmethod
    def get_transaction_type_by_public_code_account(transaction_type_public_code: str, account: Account) -> TransactionType:
        if account.channel.platform_code == 'AMZ':
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
                raise NotFound('The indicated transaction type "{}" is not supported. Please get in touch with one of the administrators.'.format(transaction_type_code))
                current_app.logger.warning('Unrecognized public transaction type code: {} for account id: {}'.format(transaction_type_code, account.id))

        else:
            raise NotFound('The platform for the transaction account "{}" is currently not supported. Please get in touch with one of the administrators.'.format(account.given_id))

        return transaction_type



    @staticmethod
    def get_invoice_currency_code(departure_country: Country, tax_jurisdiction: Country, tax_treatment_code: str) -> str:
        if tax_treatment_code == 'NON_TAXABLE_DISTANCE_SALE':
            invoice_currency_code = departure_country.currency_code
        else:
            invoice_currency_code = tax_jurisdiction.currency_code

        return invoice_currency_code



    @staticmethod
    def get_transaction_currency(item: Item, transaction_type: TransactionType, input_currency_code: str) -> str:

        if transaction_type.code=="MOVEMENT" or transaction_type.code=="INBOUND":
            transaction_currency_code = item.unit_cost_price_currency_code if item.unit_cost_price_currency_code else 'EUR'

        else:
            transaction_currency_code = input_currency_code

        return transaction_currency_code


    @staticmethod
    def get_invoice_amount_vat_reverse_charge(invoice_amount_net: float, vat_rate_reverse_charge: float) -> float:
        return invoice_amount_net * vat_rate_reverse_charge


    @staticmethod

    def get_vat_rate_reverse_charge(transaction_input: TransactionInput, arrival_country: Country, tax_treatment_code: str, tax_date: date, tax_rate_type_code: str) -> float:
        if not tax_treatment_code == 'INTRA_COMMUNITY_ACQUISITION':
            vat_rate_reverse_charge=float(0)
        else:
            # tax jurisdiction is arrival country
            vat_rate_reverse_charge = TransactionService.get_vat_rate(transaction_input, arrival_country, tax_treatment_code, tax_date, tax_rate_type_code)
        return vat_rate_reverse_charge




    @staticmethod
    def get_sale_transaction_by_bundle(account: Account, bundle: Bundle) -> Transaction:
        if account.platform_code == 'AMZ':
            sale_transaction_input_type_public_codes = ['SALE', 'COMMINGLING_BUY']
            sale_transaction_input = TransactionInput.query.filter_by(bundle_id=bundle.id, transaction_type_public_code='SALE').first()
            if not sale_transaction_input:
                sale_transaction_input = TransactionInput.query.filter_by(bundle_id=bundle.id, transaction_type_public_code='COMMINGLING_BUY').first()

            if not sale_transaction_input:
                return None

            sale_transaction=Transaction.query.filter_by(transaction_input_id=sale_transaction_input.id).first()

            return sale_transaction



    # @staticmethod
    # def get_transaction_input_by_bundle_transaction_type(account: Account, bundle: Bundle, transaction_type: TransactionType) -> List[Transaction]:
    #     if account.platform_code == 'AMZ':
    #         transaction_type_code

    #     transaction_inputs = TransactionInput.query.filter_by(bundle_id=bundle.id, transaction_type_code=transaction_type.code).all()
    #     return transaction_inputs


    @staticmethod
    def get_invoice_amount(total_value: float, invoice_exchange_rate: Decimal) -> float:
        invoice_amount: float = float(total_value) * float(invoice_exchange_rate)
        return invoice_amount



    @staticmethod
    def get_invoice_exchange_rate_date(account: Account, transaction_type: TransactionType, bundle: Bundle, transaction_currency_code: str, invoice_currency_code: str, tax_date: date) -> date:
        if TransactionService.check_exchange_rate_required(transaction_currency_code, invoice_currency_code):

            if transaction_type.code == "REFUND":
                sale_transaction: Transaction = TransactionService.get_sale_transaction_by_bundle(account, bundle)

                if sale_transaction:
                    exchange_rate_date = sale_transaction.invoice_exchange_rate_date

                else:
                    exchange_rate_date = tax_date - datetime.timedelta(days=1)

            else:
                exchange_rate_date = tax_date - datetime.timedelta(days=1)

            return exchange_rate_date



    @staticmethod
    def get_invoice_exchange_rate(invoice_exchange_rate_date: date, transaction_currency_code: str, invoice_currency_code: str) -> float:

        if invoice_exchange_rate_date:
            from ..exchange_rate.service import ExchangeRateService
            invoice_exchange_rate = ExchangeRateService.get_rate_by_base_target_date(base=transaction_currency_code, target=invoice_currency_code, date=invoice_exchange_rate_date).rate

        else:
            invoice_exchange_rate = float(1)

        return invoice_exchange_rate


    @staticmethod
    def check_exchange_rate_required(transaction_currency_code: str, invoice_currency_code: str) -> bool:
        return transaction_currency_code != invoice_currency_code


    @staticmethod
    def get_price_net(price_gross: float, price_tax_rate: float) -> float:
        price_net: float = price_gross / (1 + price_tax_rate)
        return price_net


    @staticmethod
    def get_price_vat(price_gross: float, price_tax_rate: float) -> float:
        price_vat: float = price_gross / (1 + price_tax_rate) * price_tax_rate
        return price_vat


    @staticmethod
    def get_total_value(item: Item, item_quantity: int, transaction_type: TransactionType, item_price_total: float, shipment_price_total: float, gift_wrap_price_total: float) -> float:
        if transaction_type.code == 'MOVEMENT' or transaction_type.code == 'INBOUND':
            item_price_total = item.unit_cost_price_net * item_quantity
            shipment_price_total = 0 # könnte man auch weglassen, wenn sie eh 0 sind.
            gift_wrap_price_total = 0 # könnte man auch weglassen, wenn sie eh 0 sind.
        return item_price_total + shipment_price_total + gift_wrap_price_total


    @staticmethod
    def check_amazon_vat_calculation_service(check_tax_calculation_date: date) -> bool:
        return isinstance(check_tax_calculation_date, date)

    @staticmethod
    def get_tax_calculation_date(check_tax_calculation_date: date, tax_date: date) -> date:
        return check_tax_calculation_date if isinstance(check_tax_calculation_date, date) else tax_date - timedelta(days=1)


    @staticmethod
    def get_tax_jurisdiction(tax_treatment_code: str, departure_country: Country, arrival_country: Country) -> Country:
        if (
            tax_treatment_code == 'DISTANCE_SALE'
            or tax_treatment_code == 'NON_TAXABLE_DISTANCE_SALE'
            or tax_treatment_code == 'INTRA_COMMUNITY_ACQUISITION'
            or tax_treatment_code == 'DOMESTIC_ACQUISITION'
            ):
            tax_jurisdiction_code = arrival_country.code
        else:
            tax_jurisdiction_code = departure_country.code

        tax_jurisdiction = CountryService.get_by_code(country_code = tax_jurisdiction_code)

        return tax_jurisdiction


    @staticmethod
    def get_item_tax_code_code(transaction_input: TransactionInput, item: Item, account: Account, **kwargs) -> str:
        print('account.channel.platform_code: ', account.channel.platform_code, flush=True)
        if account.channel.platform_code == 'AMZ':
            calculated_item_tax_code_code = item.tax_code_code if item.tax_code_code else 'A_GEN_STANDARD'

        else:
            raise

        if 'reference_tax_code' in kwargs and kwargs['reference_tax_code'] != None:
            reference_tax_code = kwargs['reference_tax_code']
            print('calculated_item_tax_code_code: ', calculated_item_tax_code_code, flush=True)
            print('reference_tax_code: ', reference_tax_code, flush=True)


            if calculated_item_tax_code_code != reference_tax_code:
                notification_data=NotificationService.create_notification_data(main_subject='Item Tax Code', original_filename=transaction_input.original_filename, status='warning', reference_value=str(reference_tax_code), calculated_value=str(calculated_item_tax_code_code), transaction_input_id=transaction_input.id)
                try:
                    NotificationService.create_transaction_notification(notification_data)
                    item_tax_code_code = reference_tax_code
                except:
                    db.session.rollback()
                    raise
            else:
                item_tax_code_code = calculated_item_tax_code_code
        else:
            item_tax_code_code = calculated_item_tax_code_code

        return item_tax_code_code
