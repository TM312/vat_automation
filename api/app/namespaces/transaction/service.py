
import shutil
from pathlib import Path
from typing import List
from datetime import datetime
import pandas as pd

from flask import current_app
from flask import send_from_directory

from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound, RequestEntityTooLarge, UnsupportedMediaType, Abort


from app.extensions import db

# service classes
!!! from ... import TransactionType
!!! from... import Bundle
AccountService
Account

BASE_PATH_MEDIA = current_app.config["BASE_PATH_MEDIA"]
OLD_TRANSACTION_TOLERANCE_DAYS = current_app.config["OLD_TRANSACTION_TOLERANCE_DAYS"]


class TransactionService:
    # @staticmethod
    # def get_all() -> List[Transaction]:
    #     transaction = Transaction.query.all()
    #     return transactions

    # @staticmethod
    # def get_by_id(public_id: str) -> Transaction:
    #     transaction = Transaction.query.filter(Transaction.public_id == public_id).first()
    #     if transaction:
    #         return transaction
    #     else:
    #         raise NotFound('This tax record does not exist.')

    @staticmethod
    def delete_by_id(public_id: str):
        #check if transaction exists in db
        transaction = Transaction.query.filter(
            Transaction.public_id == public_id).first()
        if transaction:
            db.session.delete(transaction)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Transaction (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This transaction does not exist.')

    @staticmethod
    def get_own(user):
        #transactions = Transaction.query.filter_by(owner_id=user.id).all().order_by(Transaction.created_on.desc())
        !!! -> needs join search
        return transactions

    @staticmethod
    def download_file(transaction, filename):
        dirpath = os.path.join(
            BASE_PATH_MEDIA,
            str(transaction.owner.public_id),
            'transaction',
            transaction.activity_period)
        #filename = '202004_transaction_input_55462838340018328.csv'
        return send_from_directory(dirpath, filename=filename, as_attachment=True)

    # @staticmethod
    # def followed_transactions(tax_auditor):
    #     return Transaction.query.join(
    #         clients, (clients.c.client_id == Transaction.owner_id)).filter(
    #             clients.c.tax_auditor_id == tax_auditor.id).order_by(
    #                 Transaction.created_on.desc())


    @staticmethod
    def create(user, seller_firm, platform, final_dirpath, activity_period) -> Transaction:

        ## A tax record is created by uploading a platform specific input file

        # check if tax record already exists in db
        transaction = Transaction.query.filter_by(owner=seller_firm.id, activity_period=activity_period).first()

        if not transaction:
            # create new tax record
            new_transaction = Transaction(
                creator_id=user.id,
                accounting_firm_id=user.employer_id,
                activity_period=activity_period,
                owner_id=seller_firm.id,
                storage_dir=final_dirpath,
            )
            # add new_transaction to db
            db.session.add(new_transaction)

         else:
            transaction.update(creator_id=user.id, accounting_firm_id=user.employer_id)

        db.session.commit()

        return new_transaction

    @staticmethod
    def create_input(
        platform,
        original_input_name,
        formatted_input_name,
        transaction) -> TransactionInput:

        # check if tax record input already exists in db
        transaction_input = Transaction.query.filter_by(
            platform=platform,
            transaction_id=transaction.id
        ).first()


        if not transaction_input:
            # create new tax record input
            new_transaction_input = TransactionInput(
                platform=platform,
                transaction_id=transaction.id,
                original_input_name=original_input_name,
                formatted_input_name=formatted_input_name
            )

            # add new_transaction to db
            db.session.add(new_transaction_input)

        else:
            transaction_input.update(
                original_input_name=original_input_name,
                formatted_input_name=formatted_input_name
            )

            transaction.update()

        db.session.commit()




##################



class TaxCodeService:
    @staticmethod
    def get_by_code(tax_code_code: str) -> TaxCode:
        tax_code = TaxCode.query.filter_by(code=tax_code_code).first()
        if tax_code:
            return tax_code
        else:
            raise NotFound('The tax code "{}" is currently not supported by our database. Please get in contact with one of the admins.'.format(tax_code_code))

class TaxRateService:
    @staticmethod
    def get_by_tax_code_country_tax_date(tax_code_code: str, country: Country, tax_date: date) -> TaxRate:
        tax_rate: TaxRate = TaxRate.query.filter(TaxRate.tax_code==tax_code_code, TaxRate.country==country, TaxRate.valid_from<=tax_date, TaxRate.valid_to>=tax_date).first()
        if tax_rate:
            return tax_rate
        else:
            raise NotFound('The tax rate for the tax code: "{}" and the country: "{}" could not be found. Please get in contact with one of the admins.'.format(tax_code, country.name))

    @staticmethod
    def get_by_tax_rate_type_country_tax_date(country: Country, tax_rate_type_name: str, tax_date: date) -> TaxRate:
        tax_rate: TaxRate = TaxRate.query.filter(TaxRate.country==country, TaxRate.tax_rate_type_name==tax_rate_type_name, TaxRate.valid_from<=tax_date, TaxRate.valid_to>=tax_date).first()
        if tax_rate:
            return tax_rate
        else:
            raise NotFound('The tax rate for the tax rate type "{}" and the country "{}" could not be found. Please get in contact with one of the admins.'.format(tax_rate_type_name, country.name))





#####




# class OutputService:
#     @staticmethod
#     def check_non_taxable_distance_sale(departure_country, tax_treatment_code):
#         return (departure_country.code == 'PL' and tax_treatment_code == 'DISTANCE_SALE')

#     @staticmethod
#     def calculate_non_taxable_distance_sale(departure_country, total_value_vat, tax_jurisdiction):
#         ExchangeRateService.get_rate_by_base_target_date(base=tax_jurisdiction.currency_code, target=departure_country.currency_code, date=exchange_rate_date)






class TransactionService:

    # TransactionService:
    @staticmethod
    def vat_check_required(date: date, number: str) -> bool:
        if not number:
            return False

        else:
            return date.today() - timedelta(days=OLD_TRANSACTION_TOLERANCE_DAYS) <= date



    @staticmethod
    def get_tax_rate_rate(tax_jurisdiction: Country, tax_treatment_code: str, item_tax_code_code: str, tax_date: date, **kwargs) -> float:
        if tax_treatment_code == 'EXPORT' or tax_treatment_code =='INTRA_COMMUNITY_SALE' or tax_treatment_code =='LOCAL_SALE_REVERSE_CHARGE' !!! #or tax_treatment_code =='INTRA_COMMUNITY_ACQUISITION':
            tax_rate_rate = float(0)

        if 'check_tax_rate_rate' in kwargs:
            tax_rate_rate = kwargs['check_tax_rate_rate']

        elif 'tax_rate_type_name' in kwargs:
            tax_rate_rate = TaxRateService.get_by_tax_rate_type_country_tax_date(country=tax_jurisdiction, tax_rate_type_name=kwargs['tax_rate_type_name'], tax _date=tax_date).rate

        elif 'tax_code_code' in kwargs:
            tax_rate_rate = TaxRateService.get_by_tax_code_country_tax_date(tax_code_code=kwargs['tax_code_code'], country=tax_jurisdiction, tax_date=tax_date).rate

        return tax_rate_rate

        !!! -> was ist stärker? tax_treatment_code=='EXPORT' oder 'check_tax_rate_rate'



    @staticmethod
    def get_tax_treatment_code(transaction_type: TransactionType, account: Account, check_export: bool, eu: EU, customer_type: CustomerType, departure_country: Country, arrival_country: Country, amazon_vat_calculation_service: bool, check_item_price_tax_rate_rate: float, **kwargs) -> str:

        if transaction_type.code == 'SALE' or transaction_type.code == 'REFUND':
            if (check_export == True or arrival_country not in eu.countries):
                tax_treatment_code = 'EXPORT'

            elif customer_type.code == "B2B"
                if departure_country.code != arrival_country.code:
                    tax_treatment_code = 'INTRA_COMMUNITY_SALE'

                else:
                    if (
                    (departure_country.code in ['ES', 'FR', 'IT', 'PL'] and departure_country.code != account.seller_firm.establishment_country_code) or
                    (amazon_vat_calculation_service == True and check_item_price_tax_rate_rate == 0)
                    ):
                    tax_treatment_code = 'LOCAL_SALE_REVERSE_CHARGE'


            elif customer_type.code == "B2C":
                if departure_country.code != arrival_country.code:
                    tax_treatment_code = 'DISTANCE_SALE'

                else:
                    tax_treatment_code = 'LOCAL_SALE'

        elif transaction_type.code == 'ACQUISITION':
            tax_treatment_code = 'DOMESTIC_ACQUISITION'

        elif transaction_type.code == 'MOVEMENT':
            tax_treatment_code = kwargs['tax_treatment_code']

        else:
            !!!! REFUND & INBOUND

        return tax_treatment_code



    @staticmethod
    def get_transaction_type_by_public_code_account(transaction_type_public_code: str, account: Account) -> TransactionType:
        if account.channel.platform_code == 'amazon':
            if transaction_type_code == 'SALE' or transaction_type_public_code == 'COMMINGLING_SELL': !!!!!  transaction_type_code <> transaction_type_public_code
                transaction_type = TransactionType.query.filter_by(code="SALE").first()

            elif transaction_type_code == 'REFUND':
                transaction_type = TransactionType.query.filter_by(code="REFUND").first()

            elif transaction_type_code == 'RETURN':
                transaction_type = TransactionType.query.filter_by(code="RETURN").first()

            elif transaction_type_code == 'COMMINGLING_BUY':
                transaction_type = TransactionType.query.filter_by(code="ACQUISITION").first()

            elif transaction_type_code == 'MOVEMENT':
                transaction_type = TransactionType.query.filter_by(code="MOVEMENT").first()

            elif transaction_type_code == 'INBOUND':
                transaction_type = TransactionType.query.filter_by(code="INBOUND").first()

            else:
                raise NotFound('The indicated transaction type "{}" is not supported. Please get in touch with one of the administrators.'.format(transaction_type_code))
                current_app.logger.warning('Unrecognized transaction type code: {} for account id: {}'.format(transaction_type_code, account.id))

        else:
            raise NotFound('The platform for the transaction account "{}" is currently not supported. Please get in touch with one of the administrators.'.format(account.public_id))

        return transaction_type





    def transaction_processing(source: str) -> List[dict]:

        transaction_inputs: list = TransactionInputService.get_transaction_inputs_by_source(source)

        error_counter = 0
        redundancy_counter = 0

        for transaction_input in transaction_inputs:
            if transaction_input.processed = False:
                transaction = Transaction.query.filter_by(transaction_input_id=transaction_input.id).first()

                if not transaction:
                    try:
                        TransactionService.create_transaction_s_from_input(transaction_input)
                        transaction_input.update_processed()
                        db.session.commit()

                    except:
                        db.session.rollback()
                        current_app.logger.error('Failed to add transaction for transaction input id: {}'.format(transaction_input.id))

                        error_counter += 1

                else:
                    redundancy_counter += 1
                    current_app.logger.warning('A transaction processing was initialized more than once based on transaction input {}.'.format(transaction_input.id))

            else:
                current_app.logger.warning('A transaction input (id: {}) was set for processing altough attribute "processed"==True.'.format(transaction_input.id))

        response_objects = TransactionInputService.create_transaction_response_objects(file, total_number_transactions, error_counter, redundancy_counter)

        current_app.logger.info(response_objects)







    def create_transaction_s_from_input(transaction_input: TransactionInput)

        account: Account = AccountService.get_by_public_id_channel_code(transaction_input.account_public_id, transaction_input.channel_code)
        transaction_type: TransactionType = get_transaction_type_by_public_code_account(transaction_input.transaction_type_public_code, account)

        if transaction_type.code == 'MOVEMENT':
            new_transaction_intra_community_sale = TransactionService.create_calculation_from_input(transaction_input, transaction_type, account, tax_treatment_code='INTRA_COMMUNITY_SALE')
            db.session.add(new_transaction_intra_community_sale)

            new_transaction_intra_community_acquisition = TransactionService.create_calculation_from_input(transaction_input, transaction_type, account, tax_treatment_code='INTRA_COMMUNITY_ACQUISITION')
            db.session.add(new_transaction_intra_community_acquisition)

        else:
            new_transaction = TransactionService.create_calculation_from_input(transaction_input, transaction_type, account)
            db.session.add(new_transaction)



        #response_objects = TransactionInputService.create_input_response_objects(file, total_number_transactions, error_counter, redundancy_counter)


        return response_objects





    def create_calculation_from_input(transaction_input: TransactionInput, transaction_type: TransactionType, account: Account, **kwargs)

        amazon_vat_calculation_service: bool = TransactionService.check_amazon_vat_calculation_service(transaction_input.check_tax_calculation_date)

        account: Account = account
        item: Item = ItemService.get_by_sku_account_date(transaction_input.item_sku, account, transaction_input.tax_date)
        bundle: Bundle = TransactionService.get_or_create_bundle_by_account_item_transaction_public_id(account, item, transaction_input.transaction_public_id)

        transaction_type: TransactionType = transaction_type

        arrival_country: Country = CountryService.get_by_code(transaction_input.arrival_country_code)
        departure_country: Country = CountryService.get_by_code(transaction_input.departure_country_code)
        eu: EU = CountryService.get_eu_by_date(transaction_input.tax_date) #EU

        customer_type_checked: bool = TransactionService.vat_check_required(date=transaction_input.tax_date, number=transaction_input.customer_vat_number)
        customer_type: str = CustomerService.get_customer_type(country_code=transaction_input.customer_vat_number_country_code, number=transaction_input.customer_vat_number, date=transaction_input.tax_date)


        tax_treatment_code: str = TaxRateService.get_tax_treatment_code(transaction_type, account, transaction_input.check_export, eu, customer_type, departure_country, arrival_country, amazon_vat_calculation_service, transaction_input.check_item_price_tax_rate_rate, **kwargs)


        tax_juristdiction: Country = TransactionService.get_tax_jurisdiction(tax_treatment_code, departure_country, arrival_country)
        item_tax_code_code: str = TransactionService.get_item_tax_code_code(item, transaction_input.check_item_tax_code_code)

        item_price_tax_rate_rate: float = TransactionService.get_tax_rate_rate(tax_jurisdiction=tax_jurisdiction, tax_treatment_code=tax_treatment_code, tax_date=transaction_input.tax_date, tax_code_code=item_tax_code_code, check_tax_rate_rate=transaction_input.check_item_price_tax_rate_rate)
        gift_wrap_tax_rate_rate: float = TransactionService.get_tax_rate_rate(tax_jurisdiction=tax_jurisdiction, tax_treatment_code=tax_treatment_code, tax_date=transaction_input.tax_date, tax_rate_type_name='S')
        shipment_price_tax_rate_rate : float= TransactionService.get_tax_rate_rate(tax_jurisdiction=tax_jurisdiction, tax_treatment_code=tax_treatment_code, tax_date=transaction_input.tax_date, tax_rate_type_name='S')


        item_price_net: float = TransactionService.get_price_net(transaction_input.item_price_gross, item_price_tax_rate_rate)
        item_price_discount_net: float = TransactionService.get_price_net(transaction_input.item_price_discount_gross, item_price_tax_rate_rate)
        item_price_total_net: float = TransactionService.get_price_net(transaction_input.item_price_total_gross, item_price_tax_rate_rate)

        shipment_price_net: float = TransactionService.get_price_net(transaction_input.shipment_price_gross, shipment_price_tax_rate_rate)
        shipment_price_discount_net: float = TransactionService.get_price_net(transaction_input.shipment_price_discount_gross, shipment_price_tax_rate_rate)
        shipment_price_total_net: float = TransactionService.get_price_net(transaction_input.shipment_price_total_gross, shipment_price_tax_rate_rate)

        gift_wrap_price_net: float = TransactionService.get_price_net(transaction_input.gift_wrap_price_gross, gift_wrap_price_tax_rate_rate)
        gift_wrap_price_discount_net: float = TransactionService.get_price_net(transaction_input.gift_wrap_price_discount_gross, gift_wrap_price_tax_rate_rate)
        gift_wrap_price_total_net: float = TransactionService.get_price_net(transaction_input.gift_wrap_price_total_gross, gift_wrap_price_tax_rate_rate)

        item_price_vat: float = TransactionService.get_price_vat(transaction_input.item_price_gross, item_price_tax_rate_rate)
        item_price_discount_vat: float = TransactionService.get_price_vat(transaction_input.item_price_discount_gross, item_price_tax_rate_rate)
        item_price_total_vat: float = TransactionService.get_price_vat(transaction_input.item_price_total_gross, item_price_tax_rate_rate)

        shipment_price_vat: float = TransactionService.get_price_vat(transaction_input.shipment_price_gross, shipment_price_tax_rate_rate)
        shipment_price_discount_vat: float = TransactionService.get_price_vat(transaction_input.shipment_price_discount_gross, shipment_price_tax_rate_rate)
        shipment_price_total_vat: float = TransactionService.get_price_vat(transaction_input.shipment_price_total_gross, shipment_price_tax_rate_rate)

        gift_wrap_price_vat: float = TransactionService.get_price_vat(transaction_input.gift_wrap_price_gross, gift_wrap_price_tax_rate_rate)
        gift_wrap_price_discount_vat: float = TransactionService.get_price_vat(transaction_input.gift_wrap_price_discount_gross, gift_wrap_price_tax_rate_rate)
        gift_wrap_price_total_vat: float = TransactionService.get_price_vat(transaction_input.gift_wrap_price_total_gross, gift_wrap_price_tax_rate_rate)

        invoice_currency_code: str = tax_juristdiction.currency_code
        transaction_currency_code: str = get_transaction_currency(item, transaction_type, transaction_input.currency_code)

        total_value_net: float = TransactionService.get_total_value(item, transaction_input.item_quantity, transaction_type, item_price_total_net, shipment_price_total_net, gift_wrap_price_total_net)
        total_value_vat: float = TransactionService.get_total_value(item, transaction_input.item_quantity, transaction_type, item_price_total_vat, shipment_price_total_vat, gift_wrap_price_total_vat)
        total_value_gross: float = TransactionService.get_total_value(item, transaction_input.item_quantity, transaction_type, transaction_input.item_price_total_gross, transaction_input.shipment_price_total_gross, transaction_input.gift_wrap_price_total_gross)

        invoice_currency_code: str = tax_juristdiction.currency_code
        transaction_currency_code: str = get_transaction_currency(item, transaction_type, transaction_input.currency_code)

        invoice_exchange_rate_date: date = get_invoice_exchange_rate_date(transaction_type, bundle, transaction_currency_code, invoice_currency_code, transaction_input.tax_date)
        invoice_exchange_rate: float = get_invoice_exchange_rate(invoice_exchange_rate_date=invoice_exchange_rate_date, transaction_currency_code=transaction_currency_code, invoice_currency_code=invoice_currency_code)


        invoice_amount_net: float = TransactionService.get_invoice_amount(total_value_net, invoice_exchange_rate)
        invoice_amount_vat: float = TransactionService.get_invoice_amount(total_value_vat, invoice_exchange_rate)
        invoice_amount_gross: float = TransactionService.get_invoice_amount(total_value_gross, invoice_exchange_rate)

        tax_rate_rate_reverse_charge: float = get_tax_rate_rate_reverse_charge(tax_treatment_code=tax_treatment_code, arrival_country=arrival_country, tax_date=transaction_input.tax_date, item_tax_code_code=item_tax_code_code) --> 0 ausser bei "intra_community_acquisition": hier: tax_rate des arrival countries
        !!!! invoice_amount_vat_reverse_charge = get_invoice_amount_vat_reverse_charge(invoice_amount_net, tax_rate_rate_reverse_charge)



        # self.arrival_seller_vat_country_code: str = arrival_country.vat_country_code
        # self.departure_seller_vat_country_code: str = departure_country.vat_country_code
        # self.seller_vat_country_code: str = tax_juristdiction.vat_country_code

        arrival_seller_vat_valid: bool = VATINService.check_validity(country_code = arrival_country.vat_country_code, number=transaction_input.check_arrival_seller_vat_number, initial_tax_date=transaction_input.tax_date)
        departure_seller_vat_valid: bool = VATINService.check_validity(country_code = departure_country.vat_country_code, number=transaction_input.check_departure_seller_vat_number, initial_tax_date=transaction_input.tax_date)
        seller_vat_valid: bool = VATINService.check_validity(country_code = tax_juristdiction.vat_country_code, number=transaction_input.check_seller_vat_number, initial_tax_date=input.tax_date)







    def get_transaction_currency(item: Item, transaction_type: TransactionType, input_currency_code: str) -> str:

        if transaction_type.code=="MOVEMENT":
            transaction_currency_code = item.unit_cost_price_currency_code if item.unit_cost_price_currency_code else 'EUR'

        else:
            transaction_currency_code = input_currency_code

        return transaction_currency_code


    def get_invoice_amount_vat_reverse_charge(invoice_amount_net: float, tax_rate_rate_reverse_charge: float) -> float:
        return invoice_amount_net * tax_rate_rate_reverse_charge

    def get_tax_rate_rate_reverse_charge(tax_treatment_code: str, arrival_country: Country, tax_date: date, item_tax_code_code: str) -> float:
        tax_rate_rate_reverse_charge = TransactionService.get_tax_rate_rate(tax_jurisdiction=arrival_country, tax_treatment_code=tax_treatment_code, tax_date=tax_date, tax_code_code=item_tax_code_code)
        !!!! hier muss möglicherweise noch etwas geändert werden !!!!
        return tax_rate_rate_reverse_charge


    @staticmethod
    def get_or_create_bundle_by_account_item_transaction_public_id(account: Account, item: Item, transaction_public_id: str) -> Bundle:
        bundle = Bundle.query.join(Bundle.transactions, aliased=True).filter_by(account_id=account.id, item_id=item.id, public_id=transaction_public_id).first()
        if bundle:
            return bundle

        else:
            new_bundle = Bundle()
            db.session.add(new_bundle)
            return new_bundle


    @staticmethod
    def get_sale_transaction_by_bundle(bundle) -> Transaction:
        sale_transaction = Transaction.query.filter_by(bundle_id=bundle.id, transaction_type_code='SALE').first()
        return sale_transaction


    @staticmethod
    def get_transactions_by_bundle_transaction_type(bundle: Bundle, transaction_type: TransactionType) -> List[Transaction]:
        transactions = Transaction.query.filter_by(bundle_id=bundle.id, transaction_type_code=transaction_type.code).all()
        return transactions


    @staticmethod
    def get_invoice_amount(total_value: float, invoice_exchange_rate: float) -> float:
        invoice_amount: float = total_value * invoice_exchange_rate
        return invoice_amount


    @staticmethod
    def get_invoice_exchange_rate_date(transaction_type: TransactionType, bundle: Bundle, transaction_currency_code: str, invoice_currency_code: str, tax_date: date) -> float or None:
        if check_exchange_rate_required(transaction_currency_code, invoice_currency_code):
            invoice_exchange_rate_date = TransactionService.get_exchange_rate_date(tax_date, transaction_type, bundle)
            return invoice_exchange_rate_date

        else:
            return None


     @staticmethod
    def get_exchange_rate_date(tax_date: date, transaction_type: TransactionType, bundle: Bundle) -> date:
        if transaction_type.code == "REFUND":
            sale_transaction: Transaction = TransactionService.get_sale_transaction_by_bundle(bundle)

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
            invoice_exchange_rate = ExchangeRateService.get_rate_by_base_target_date(base=transaction_currency_code, target=invoice_currency_code, date=invoice_exchange_rate_date)

        else:
            invoice_exchange_rate = float(1)

        return invoice_exchange_rate


    @staticmethod
    def check_exchange_rate_required(transaction_currency_code: str, invoice_currency_code: str) -> bool:
        return not transaction_currency_code == invoice_currency_code


    @staticmethod
    def get_price_net(price_gross: float, price_tax_rate: float) ->float:
        price_net: float = price_gross / (1 + price_tax_rate)
        return price_net


    @staticmethod
    def get_price_vat(price_gross: float, price_tax_rate: float) -> float:
        price_vat: float = price_gross / (1 + price_tax_rate) * price_tax_rate
        return price_vat


    @staticmethod
    def get_total_value(item: Item, item_quantity: int, transaction_type: TransactionType, item_price_total: float, shipment_price_total: float, gift_wrap_price_total: float) -> float:
        if transaction_type.code == 'MOVEMENT':
            item_price_total = item.unit_cost_price_net * item_quantity   !!!! muss hier ggf. noch in transaction_currency umgerechnet werden ???
            shipment_price_total = 0 # könnte man auch weglassen, wenn sie eh 0 sind.
            gift_wrap_price_total = 0 # könnte man auch weglassen, wenn sie eh 0 sind.
        return item_price_total + shipment_price_total + gift_wrap_price_total


    @staticmethod
    def check_amazon_vat_calculation_service(check_tax_calculation_date) -> bool:
        return True if check_tax_calculation_date else False

    @staticmethod
    def get_tax_calculation_date(check_tax_calculation_date, tax_date: date) -> date:
        return check_tax_calculation_date if check_tax_calculation_date else tax_date


    @staticmethod
    def get_tax_jurisdiction(tax_treatment_code: str, departure_country: Country, arrival_country: Country) -> Country:
        if tax_treatment_code == 'DISTANCE_SALE':
            tax_jurisdiction_code = arrival_country.code
        else:
            tax_jurisdiction_code = departure_country.code
        tax_jurisdiction = CountryService.get_by_code(country_code = tax_jurisdiction_code)

        return tax_jurisdiction


    @staticmethod
    def get_item_tax_code_code(item: Item, check_item_tax_code_code) -> str:
        if account.channel.platform_code == 'AMZ':
            if check_item_tax_code_code:
                item_tax_code_code = check_item_tax_code_code

            elif item.tax_code_code:
                item_tax_code_code = item.tax_code_code

            else:
                item_tax_code_code = 'A_GEN_STANDARD'

        return item_tax_code_code
