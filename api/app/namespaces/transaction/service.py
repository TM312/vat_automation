
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
from ... import TransactionType


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
        transactions = Transaction.query.filter_by(owner_id=user.id).all().order_by(
            Transaction.created_on.desc())
        return transactions

    @staticmethod
    def download_file(transaction, filename):
        dirpath = os.path.join(
            current_app.config['BASE_PATH_MEDIA'],
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

class InputService:
    @staticmethod
    def read_amazon_upload_into_df(file):
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



# class OutputService:
#     @staticmethod
#     def check_non_taxable_distance_sale(departure_country, tax_treatment_code):
#         return (departure_country.code == 'PL' and tax_treatment_code == 'DISTANCE_SALE')

#     @staticmethod
#     def calculate_non_taxable_distance_sale(departure_country, total_value_vat, tax_jurisdiction):
#         ExchangeRateService.get_rate_by_base_targe_date(base=tax_jurisdiction.currency_code, target=departure_country.currency_code, date=exchange_rate_date)


class PlatformService:
    @staticmethod
    def get_by_public_id_channel_code(account_public_id, channel_code) -> Account:
        account = Account.query.filter_by(public_id=account_public_id,  channel_code=channel_code).first()
        if account:
            return account
        else:
            raise NotFound('An account for the channel {} and the id {} does not exist in our db. Please add the account before proceeding.'.format(channel_code, account_public_id))



class ItemService:
    @staticmethod
    def get_by_sku_account_date(item_sku, account, date) -> Item:
        if account.channel.platform_name == 'amazon':
            item = Item.query.filter(Item.sku==item_sku, Item.seller_firm_id=account.seller_firm_id, Item.valid_from<=date, Item.valid_to>=date).first()
            if item:
                return item
            else:
                raise NotFound('The item specific SKU "{}" is not listed in the item information of the seller. Please update the item information before proceeding'.format(item_sku))

class TaxCodeService:
    @staticmethod
    def get_by_code(tax_code_code) -> TaxCode:
        tax_code = TaxCode.query.filter_by(code=tax_code_code).first()
        if tax_code:
            return tax_code
        else:
            raise NotFound('The tax code "{}" is currently not supported by our database. Please get in contact with one of the admins.'.format(tax_code_code))

class TaxRateService:
    @staticmethod
    def get_by_tax_code_country_tax_date(tax_code, country, tax_date) -> TaxRate:
        tax_rate = TaxRate.query.filter(TaxRate.tax_code==tax_code, TaxRate.country==country, TaxRate.valid_from<tax_date, TaxRate.valid_to>tax_date).first()
        if tax_rate:
            return tax_rate
        else:
            raise NotFound('The tax rate for the tax code: "{}" and the country: "{}" could not be found. Please get in contact with one of the admins.'.format(tax_code, country.name))

    @staticmethod
    def get_by_tax_rate_type_country_tax_date(country, tax_rate_type_name, tax_date) -> TaxRate:
        tax_rate = TaxRate.query.filter(TaxRate.country==country, TaxRate.tax_rate_type_name==tax_rate_type_name, TaxRate.valid_from<tax_date, TaxRate.valid_to>tax_date).first()
        if tax_rate:
            return tax_rate
        else:
            raise NotFound('The tax rate for the tax rate type "{}" and the country "{}" could not be found. Please get in contact with one of the admins.'.format(tax_rate_type_name, country.name))



class CountryService:
    @staticmethod
    def get_by_code(country_code: str) -> Country:
        country = Country.query.filter_by(code=country_code).first()
        if country:
            return country
        else:
            raise NotFound('The country "{}" is currently not supported by our database. Please get in contact with one of the admins.'.format(country_code))

    @staticmethod
    def get_eu_by_date(date) -> EU:
        eu = EU.query.filter(EU.valid_from<=date, EU.valid_to>=date).first()
        if eu:
            return eu
        else:
            raise NotFound('A constellation of EU countries has not been defined for the requested date ({})'.format(str(date)))



class CustomerService:
    @staticmethod
    def get_type_by_vatin_date(vat_number, date):
    # customer_type_code = 'B2C' if not customer_vat_number else --> CHECK VAT NUMBER
     !!! --> "B2B"
        return customer_type


class TransactionService:

    @staticmethod
    def get_tax_rate_rates(tax_jurisdiction, tax_treatment_code, item_tax_code_code, tax_date):
        if check_item_price_tax_rate_rate:
            item_price_tax_rate_rate = check_item_price_tax_rate_rate
            gift_wrap_tax_rate_rate = shipment_price_tax_rate_rate = TaxRateService.get_by_tax_rate_type_country_tax_date(country=tax_jurisdiction, tax_rate_type_name='S', tax_date=tax_date)

        elif tax_treatment_code == 'EXPORT' or 'INTRA_COMMUNITY_SALE' or 'LOCAL_SALE_REVERSE_CHARGE':
            item_price_tax_rate_rate = gift_wrap_rate_rate = shipment_price_tax_rate_rate = float(0)

        else:
            item_price_tax_rate_rate = TaxRateService.get_by_tax_code_country_tax_date(tax_code=item_tax_code, country=tax_jurisdiction, tax_date=tax_date).rate
            shipment_price_tax_rate_rate = gift_wrap_rate_rate = TaxRateService.get_by_tax_rate_type_country_tax_date(country=tax_jurisdiction, tax_rate_type_name='S', tax_date=tax_date)

        return item_price_tax_rate_rate, gift_wrap_tax_rate_rate, shipment_price_tax_rate_rate



    @staticmethod
    def get_tax_treatment_code(account, check_export, eu, customer_type, departure_country, arrival_country, amazon_vat_calculation_service, check_item_price_tax_rate_rate):
        if (check_export == 'YES' or arrival_country not in eu.countries):
            tax_treatment_code = 'EXPORT'

        elif customer_type.code == "B2B"
            if departure_country.code != arrival_country.code:
                tax_treatment_code = 'INTRA_COMMUNITY_SALE'

            else:
                if (
                (departure_country.code in ['ES', 'FR', 'IT', 'PL'] and departure_country.code != account.seller_firm.establishment_country_code) or
                (amazon_vat_calculation_service and check_item_price_tax_rate_rate == 0)
                ):
                tax_treatment_code = 'LOCAL_SALE_REVERSE_CHARGE'


                else:
                    tax_treatment_code = 'DISTANCE_SALE'

        else:
            tax_treatment_code = 'LOCAL_SALE' ???

        return tax_treatment_code




    # TransactionService
    @staticmethod
    def get_transaction_type_by_public_code_account(transaction_type_public_code: str, account: Account) -> TransactionType:
        if account.channel.platform_name == 'amazon':
            if transaction_type_code == 'SALE' or transaction_type_public_code == 'COMMINGLING_SELL':
                transaction_type = TransactionType.query.filter_by(code="SALE").first()

            elif transaction_type_code == 'REFUND':
                transaction_type = TransactionType.query.filter_by(code="REFUND").first()

            # elif transaction_type_code == 'REFUND':
            #     transaction_type = TransactionType.query.filter_by(name="SALE").first()
            #     return transaction_type


            else:
                raise NotFound('The indicated transaction type "{}" is not supported. Please get in touch with one of the administrators.'.format(transaction_type_code))

        else:
            raise NotFound('The platform for the transaction account "{}" is currently not supported. Please get in touch with one of the administrators.'.format(account.public_id))

        return transaction_type

    # TransactionService
    @staticmethod
    def check_refund_treatment(bundle, item_price_total_gross, shipment_price_total_gross, gift_wrap_price_total_gross):
        if bundle:
            sale_transaction = TransactionService.get_sale_transaction_by_bundle(bundle)
            if sale_transaction:
                if not item_price_total_gross or not shipment_price_total_gross or not gift_wrap_price_total_gross:
                    !!!!!
                else:
                    alles von Sales übernehmen !!!!!

        else:
            return False





## MASTER FUNCTION
def transaction_processing(file) -> Transaction:

   try:
       df = read_amazon_upload_into_df(file)
    except:
        raise UnsupportedMediaType('Error while reading the input file ({}).'.format(str(file))) !!!! filename





    for i in range(len(df.index)):
        input = Input(df, i)

        amazon_vat_calculation_service: bool = TransactionService.check_amazon_vat_calculation_service(input.check_tax_calculation_date)

        account: Account = PlatformService.get_by_public_id_channel_code(input.account_public_id, input.channel_code)
        item: Item = ItemService.get_by_sku_account_date(input.item_sku, account, input.tax_date)
        bundle: Bundle = TransactionService.get_bundle_by_account_item_date(account, item, input.transaction_public_id) !!! #may be empty: in that case need to be created later
        transaction_type: TransactionType = get_transaction_type_by_public_code_account(input.transaction_type_public_code, account)
        arrival_country: Country = CountryService.get_by_code(input.arrival_country_code)
        departure_country: Country = CountryService.get_by_code(input.departure_country_code)
        eu: EU = CountryService.get_eu_by_date(input.tax_date) #EU


        if transaction_type == 'REFUND':
            check_refund_treatment(calculation.bundle, input.item_price_total_gross, input.shipment_price_total_gross, input.gift_wrap_price_total_gross)





        !!!!! #customer_type = CustomerService.get_type_by_vatin_date(vat_number=input.customer_vat_number, date=input.tax_date, !!!!! )



        tax_treatment_code: str = TaxRateService.define_tax_treatment_code(account, input.check_export, eu, customer_type, departure_country, arrival_country, amazon_vat_calculation_service, input.check_item_price_tax_rate_rate)

        tax_juristdiction: Country = TransactionService.define_tax_jurisdiction(tax_treatment_code, departure_country, arrival_country)
        item_tax_code_code: str = TransactionService.get_item_tax_code_code(item, input.check_item_tax_code_code)

        item_price_tax_rate_rate, gift_wrap_tax_rate_rate, shipment_price_tax_rate_rate = TransactionService.get_tax_rate_rates(tax_jurisdiction, tax_treatment_code, item_tax_code_code, input.tax_date)

        item_price_net: float = TransactionService.get_price_net(input.item_price_gross, item_price_tax_rate_rate)
        item_price_discount_net: float = TransactionService.get_price_net(input.item_price_discount_gross, item_price_tax_rate_rate)
        item_price_total_net: float = TransactionService.get_price_net(input.item_price_total_gross, item_price_tax_rate_rate)

        shipment_price_net: float = TransactionService.get_price_net(input.shipment_price_gross, shipment_price_tax_rate_rate)
        shipment_price_discount_net: float = TransactionService.get_price_net(input.shipment_price_discount_gross, shipment_price_tax_rate_rate)
        shipment_price_total_net: float = TransactionService.get_price_net(input.shipment_price_total_gross, shipment_price_tax_rate_rate)

        gift_wrap_price_net: float = TransactionService.get_price_net(input.gift_wrap_price_gross, gift_wrap_price_tax_rate_rate)
        gift_wrap_price_discount_net: float = TransactionService.get_price_net(input.gift_wrap_price_discount_gross, gift_wrap_price_tax_rate_rate)
        gift_wrap_price_total_net: float = TransactionService.get_price_net(input.gift_wrap_price_total_gross, gift_wrap_price_tax_rate_rate)

        item_price_vat: float = TransactionService.get_price_vat(input.item_price_gross, item_price_tax_rate_rate)
        item_price_discount_vat: float = TransactionService.get_price_vat(input.item_price_discount_gross, item_price_tax_rate_rate)
        item_price_total_vat: float = TransactionService.get_price_vat(input.item_price_total_gross, item_price_tax_rate_rate)

        shipment_price_vat: float = TransactionService.get_price_vat(input.shipment_price_gross, shipment_price_tax_rate_rate)
        shipment_price_discount_vat: float = TransactionService.get_price_vat(input.shipment_price_discount_gross, shipment_price_tax_rate_rate)
        shipment_price_total_vat: float = TransactionService.get_price_vat(input.shipment_price_total_gross, shipment_price_tax_rate_rate)

        gift_wrap_price_vat: float = TransactionService.get_price_vat(input.gift_wrap_price_gross, gift_wrap_price_tax_rate_rate)
        gift_wrap_price_discount_vat: float = TransactionService.get_price_vat(input.gift_wrap_price_discount_gross, gift_wrap_price_tax_rate_rate)
        gift_wrap_price_total_vat: float = TransactionService.get_price_vat(input.gift_wrap_price_total_gross, gift_wrap_price_tax_rate_rate)

        total_value_net: float = TransactionService.get_total_value(item_price_total_net, shipment_price_total_net, gift_wrap_price_total_net)
        total_value_vat: float = TransactionService.get_total_value(item_price_total_vat, shipment_price_total_vat, gift_wrap_price_total_vat)
        total_value_gross: float = TransactionService.get_total_value(input.item_price_total_gross, input.shipment_price_total_gross, input.gift_wrap_price_total_gross)

        invoice_currency_code: str = tax_juristdiction.currency_code

        invoice_exchange_rate: float = get_invoice_exchange_rate(input.currency_code, invoice_currency_code, input.tax_date)

        invoice_amount_net: float = TransactionService.get_invoice_amount(total_value_net, invoice_exchange_rate)
        invoice_amount_vat: float = TransactionService.get_invoice_amount(total_value_vat, invoice_exchange_rate)
        invoice_amount_gross: float = TransactionService.get_invoice_amount(total_value_gross, invoice_exchange_rate)

        # self.arrival_seller_vat_country_code: str = arrival_country.vat_country_code
        # self.departure_seller_vat_country_code: str = departure_country.vat_country_code
        # self.seller_vat_country_code: str = tax_juristdiction.vat_country_code








## END MASTER FUNCTION ##



    class ExchangeRateService:
    def get_rate_by_base_targe_date(base, target, date):
        if base == 'EUR':
            exchange_rates = ExchangeRatesEUR.query.filter_by(date=date).first()
        elif base == 'GBP':
            exchange_rates = ExchangeRatesGBP.query.filter_by(date=date).first()
        elif base == 'PLN':
            exchange_rates = ExchangeRatesPLN.query.filter_by(date=date).first()
        elif base == 'CZK':
            exchange_rates = ExchangeRatesCZK.query.filter_by(date=date).first()
        else:
            raise NotFound('The base currency "{}" is currently not supported. Please get in touch with one of the administrators.'.format(base))

        if target == 'EUR':
            exchange_rate = exchange_rates.eur
        elif target == 'PLN':
            exchange_rate = exchange_rates.pln
        elif target == 'GBP':
            exchange_rate = exchange_rates.gbp
        elif target == 'CZK':
            exchange_rate = exchange_rates.czk
        else:
            raise NotFound('The target currency "{}" is currently not supported. Please get in touch with one of the administrators.'.format(base))

        return exchange_rate

#####

    @staticmethod
    def get_bundle_by_account_item_transaction_public_id(account, item, transaction_public_id) -> Bundle:
        bundle = Bundle.query.join(Bundle.transactions, aliased=True).filter_by(account_id=account.id, item_id=item.id, public_id=transaction_public_id).first()
        return bundle


    @staticmethod
    def get_sale_transaction_by_bundle(bundle) -> Transaction:
        sale_transaction = Transaction.query.filter_by(bundle_id=bundle.id, t_type='sale').first()
        return sale_transaction


    @staticmethod
    def get_transactions_by_bundle_transaction_type(bundle, transaction_type) -> List[Transaction]:
        transactions = Transaction.query.filter_by(bundle_id=bundle.id, t_type=transaction_type.code).all()
        return transactions


    @staticmethod
    def get_invoice_amount(total_value, invoice_exchange_rate):
        invoice_amount = total_value * invoice_exchange_rate
        return invoice_amount

    @staticmethod
    def get_invoice_exchange_rate(currency_code, invoice_currency_code, tax_date):
        if check_exchange_rate_required(currency_code, invoice_currency_code):
            exchange_rate_date = TransactionService.get_exchange_rate_date(tax_date)
            invoice_exchange_rate = ExchangeRateService.get_rate_by_base_targe_date(base=currency_code, target=invoice_currency_code, date=exchange_rate_date)

        else:
            invoice_exchange_rate = float(1)

        return invoice_exchange_rate

    @staticmethod
    def get_exchange_rate_date(tax_date):
        exchange_rate_date = tax_date - datetime.timedelta(days=1)
        return exchange_rate_date

    @staticmethod
    def check_exchange_rate_required(currency_code, invoice_currency_code) -> bool:
        return not currency_code == invoice_currency_code


    @staticmethod
    def get_price_net(price_gross, price_tax_rate):
        price_net = float(price_gross / (1 + price_tax_rate))
        return price_net

    @staticmethod
    def get_price_vat(price_gross, price_tax_rate):
        price_vat = float(price_gross / (1 + price_tax_rate) * price_tax_rate)
        return price_vat

    @staticmethod
    def get_total_value(item_price_total, shipment_price_total, gift_wrap_price_total):
        return item_price_total + shipment_price_total + gift_wrap_price_total



    @staticmethod
    def check_amazon_vat_calculation_service(check_tax_calculation_date) -> bool:
        return True if check_tax_calculation_date else False

    @staticmethod
    def get_tax_calculation_date(check_tax_calculation_date, tax_date):
        return check_tax_calculation_date if check_tax_calculation_date else tax_date


    #TransactioService
    @staticmethod
    def define_tax_jurisdiction(tax_treatment_code, departure_country, arrival_country) -> Country:
        if tax_treatment_code == 'DISTANCE_SALE':
            tax_jurisdiction_code = arrival_country.code
        else:
            tax_jurisdiction_code = departure_country.code
        tax_jurisdiction = CountryService.get_by_code(country_code = tax_jurisdiction_code)

        return tax_jurisdiction

    @staticmethod
    def get_item_tax_code_code(item, check_item_tax_code_code) -> str:
        if account.channel.platform_name == 'amazon':
            if check_item_tax_code_code:
                item_tax_code_code = check_item_tax_code_code

            elif item.tax_code_code:
                item_tax_code_code = item.tax_code_code

            else:
                item_tax_code_code = 'A_GEN_STANDARD'

        return item_tax_code_code



















input.account_public_id,
input.public_activity_period,
input.channel_code,
input.marketplace_name,
input.transaction_type_public_code,
input.transaction_public_id,
input.transaction_activity_id,
input.shipment_date,
input.arrival_date,
input.tax_date,
input.item_sku,
input.item_name,
input.item_manufacture_country,
input.item_quantity,
input.item_weight_kg,
input.item_weight_kg_total,
input.unit_cost_price_net,
input.item_price_discount_gross,
input.item_price_gross,
input.item_price_total_gross,
input.shipment_price_discount_gross,
input.shipment_price_gross,
input.shipment_price_total_gross,
input.sale_total_value_gross,
input.gift_wrap_price_discount_gross,
input.gift_wrap_price_gross,
input.gift_wrap_price_total_gross,
input.currency_code,
input.departure_country_code,
input.departure_postal_code,
input.departure_city,
input.arrival_country_code,
input.arrival_postal_code,
input.arrival_city,
input.arrival_address,
input.shipment_mode,
input.shipment_conditions,
input.invoice_number,
input.invoice_url,
input.customer_name,
input.customer_vat_number,
input.customer_vat_number_country,
input.supplier_vat_number,
input.supplier_name

input.check_tax_calculation_date,
input.check_item_price_discount_net,
input.check_item_price_discount_vat,
input.check_item_price_net,
input.check_item_price_vat,
input.check_item_price_total_net,
input.check_item_price_total_vat,
input.check_item_price_tax_rate_rate,
input.check_shipment_price_discount_net,
input.check_shipment_price_discount_vat,
input.check_shipment_price_net,
input.check_shipment_price_vat,
input.check_shipment_price_total_net,
input.check_shipment_price_total_vat,
input.check_shipment_price_tax_rate_rate,
input.check_sale_total_value_net,
input.check_sale_total_value_vat,
input.check_gift_wrap_price_discount_net,
input.check_gift_wrap_price_discount_vat,
input.check_gift_wrap_price_net,
input.check_gift_wrap_price_vat,
input.check_gift_wrap_price_total_net,
input.check_gift_wrap_price_total_vat,
input.check_gift_wrap_price_tax_rate,
input.check_item_tax_code_code,
input.check_departure_seller_vat_country_code,
input.check_departure_seller_vat_number,
input.check_arrival_seller_vat_country_code,
input.check_arrival_seller_vat_number,
input.check_seller_vat_country_code,
input.check_seller_vat_number,
input.check_tax_calculation_imputation_country,
input.check_tax_jurisdiction,
input.check_tax_jurisdiction_level,
input.check_invoice_amount_vat,
input.check_invoice_currency_code,
input.check_invoice_exchange_rate,
input.check_invoice_exchange_rate_date,
input.check_export,










# write a smart sanitizing function when time available
class Input:
    def __init__(self,df, i):
        self.account_public_id = str(df.iloc[i]['UNIQUE_ACCOUNT_IDENTIFIER']).upper()
        self.public_activity_period = str(df.iloc[i]['ACTIVITY_PERIOD']).upper() # --> OUTPUT
        self.channel_code = str(df.iloc[i]['SALES_CHANNEL']).upper() # str #-->PlatformService.retrieve_account()
        self.marketplace_name = str(df.iloc[i]['MARKETPLACE']).lower() # str #-->transaction
        self.transaction_type_public_code = str(df.iloc[i]['TRANSACTION_TYPE']).upper() #-->TransactionService.retrieve_transaction_type()
        self.transaction_public_id = str(df.iloc[i]['TRANSACTION_EVENT_ID']) # str #-->transaction
        self.transaction_activity_id = str(df.iloc[i]['ACTIVITY_TRANSACTION_ID'])  # str #-->transaction --> becomes shipment_id/return_id , etc.

        self.check_tax_calculation_date = datetime.strptime(df.iloc[i]['TAX_CALCULATION_DATE'], '%d-%m-%Y').date() if not pd.isnull(df.iloc[i]['TAX_CALCULATION_DATE']) else None  #NoneType/datetime.date object #-->transaction
        self.shipment_date = datetime.strptime(df.iloc[i]['TRANSACTION_DEPART_DATE'], '%d-%m-%Y').date() if not pd.isnull(df.iloc[i]['TRANSACTION_DEPART_DATE']) else None #datetime.date object #-->transaction
        self.arrival_date = datetime.strptime(df.iloc[i]['TRANSACTION_ARRIVAL_DATE'], '%d-%m-%Y').date() if not pd.isnull(df.iloc[i]['TRANSACTION_ARRIVAL_DATE']) else None #datetime.date object #-->transaction
        self.tax_date = datetime.strptime(df.iloc[i]['TRANSACTION_COMPLETE_DATE'], '%d-%m-%Y').date() if not pd.isnull(df.iloc[i]['TRANSACTION_COMPLETE_DATE']) else None #datetime.date object #-->transaction

        self.item_sku = str(df.iloc[i]['SELLER_SKU']) # str --> ItemService.retrieve_item() --> transaction
        self.item_name = str(df.iloc[i]['ITEM_DESCRIPTION']) #str
        self.item_manufacture_country = str(df.iloc[i]['ITEM_MANUFACTURE_COUNTRY']) if not pd.isnull(df.iloc[i]['ITEM_MANUFACTURE_COUNTRY']) else None #str/NoneType
        self.item_quantity = int(df.iloc[i]['QTY']) #-->transaction
        self.item_weight_kg = float(df.iloc[i]['ITEM_WEIGHT']) if not pd.isnull(df.iloc[i]['ITEM_WEIGHT']) else None #float/NoneType
        self.item_weight_kg_total = float(df.iloc[i]['TOTAL_ACTIVITY_WEIGHT']) if not pd.isnull(df.iloc[i]['TOTAL_ACTIVITY_WEIGHT']) else None

        self.unit_cost_price_net = float(df.iloc[i]['COST_PRICE_OF_ITEMS']) if not pd.isnull(df.iloc[i]['COST_PRICE_OF_ITEMS']) else None

        self.check_item_price_discount_net = float(df.iloc[i]['PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None
        self.check_item_price_discount_vat = float(df.iloc[i]['PROMO_PRICE_OF_ITEMS_VAT_AMT']) if not pd.isnull(df.iloc[i]['PROMO_PRICE_OF_ITEMS_VAT_AMT']) else None
        self.item_price_discount_gross = float(df.iloc[i]['PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL']) else None #-->transaction

        self.check_item_price_net = float(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None
        self.check_item_price_vat = float(df.iloc[i]['PRICE_OF_ITEMS_VAT_AMT']) if not pd.isnull(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None
        self.item_price_gross = float(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None #-->transaction

        self.check_item_price_total_net = float(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None
        self.check_item_price_total_vat = float(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_VAT_AMT']) if not pd.isnull(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_VAT_AMT']) else None
        self.item_price_total_gross = float(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL']) else None #-->transaction

        self.check_item_price_tax_rate_rate = float(df.iloc[i]['PRICE_OF_ITEMS_VAT_RATE_PERCENT']) if not pd.isnull(df.iloc[i]['PRICE_OF_ITEMS_VAT_RATE_PERCENT']) else None

        self.check_shipment_price_discount_net = float(df.iloc[i]['PROMO_SHIP_CHARGE_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) else None
        self.check_shipment_price_discount_vat = float(df.iloc[i]['PROMO_SHIP_CHARGE_VAT_AMT']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) else None
        self.shipment_price_discount_gross = float(df.iloc[i]['PROMO_SHIP_CHARGE_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) else None #-->transaction

        self.check_shipment_price_net = float(df.iloc[i]['SHIP_CHARGE_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['SHIP_CHARGE_AMT_VAT_EXCL']) else None
        self.check_shipment_price_vat = float(df.iloc[i]['SHIP_CHARGE_VAT_AMT']) if not pd.isnull(df.iloc[i]['SHIP_CHARGE_VAT_AMT']) else None
        self.shipment_price_gross = float(df.iloc[i]['SHIP_CHARGE_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['SHIP_CHARGE_AMT_VAT_INCL']) else None #-->transaction

        self.check_shipment_price_total_net = float(df.iloc[i]['TOTAL_SHIP_CHARGE_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['TOTAL_SHIP_CHARGE_AMT_VAT_EXCL']) else None
        self.check_shipment_price_total_vat = float(df.iloc[i]['TOTAL_SHIP_CHARGE_VAT_AMT']) if not pd.isnull(df.iloc[i]['TOTAL_SHIP_CHARGE_VAT_AMT']) else None
        self.shipment_price_total_gross = float(df.iloc[i]['TOTAL_SHIP_CHARGE_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['TOTAL_SHIP_CHARGE_AMT_VAT_INCL']) else None #-->transaction

        self.check_shipment_price_tax_rate_rate = float(df.iloc[i]['SHIP_CHARGE_VAT_RATE_PERCENT']) if not pd.isnull(df.iloc[i]['SHIP_CHARGE_VAT_RATE_PERCENT']) else None

        self.check_sale_total_value_net = float(df.iloc[i]['TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL']) else None
        self.check_sale_total_value_vat = float(df.iloc[i]['TOTAL_ACTIVITY_VALUE_VAT_AMT']) if not pd.isnull(df.iloc[i]['TOTAL_ACTIVITY_VALUE_VAT_AMT']) else None
        self.sale_total_value_gross = float(df.iloc[i]['TOTAL_ACTIVITY_VALUE_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['TOTAL_ACTIVITY_VALUE_AMT_VAT_INCL']) else None #-->transaction

        self.check_gift_wrap_price_discount_net = float(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) else None
        self.check_gift_wrap_price_discount_vat = float(df.iloc[i]['PROMO_GIFT_WRAP_VAT_AMT']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_VAT_AMT']) else None
        self.gift_wrap_price_discount_gross = float(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_INCL']) else None #-->transaction

        self.check_gift_wrap_price_net = float(df.iloc[i]['GIFT_WRAP_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['GIFT_WRAP_AMT_VAT_EXCL']) else None
        self.check_gift_wrap_price_vat = float(df.iloc[i]['GIFT_WRAP_VAT_AMT']) if not pd.isnull(df.iloc[i]['GIFT_WRAP_VAT_AMT']) else None
        self.gift_wrap_price_gross = float(df.iloc[i]['GIFT_WRAP_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['GIFT_WRAP_AMT_VAT_INCL']) else None #-->transaction

        self.check_gift_wrap_price_total_net = float(df.iloc[i]['TOTAL_GIFT_WRAP_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['TOTAL_GIFT_WRAP_AMT_VAT_EXCL']) else None
        self.check_gift_wrap_price_total_vat = float(df.iloc[i]['TOTAL_GIFT_WRAP_VAT_AMT']) if not pd.isnull(df.iloc[i]['TOTAL_GIFT_WRAP_VAT_AMT']) else None
        self.gift_wrap_price_total_gross = float(df.iloc[i]['TOTAL_GIFT_WRAP_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['TOTAL_GIFT_WRAP_AMT_VAT_INCL']) else None #-->transaction

        self.check_gift_wrap_price_tax_rate = float(df.iloc[i]['GIFT_WRAP_VAT_RATE_PERCENT']) if not pd.isnull(df.iloc[i]['GIFT_WRAP_VAT_RATE_PERCENT']) else None


        self.currency_code = str(df.iloc[i]['TRANSACTION_CURRENCY_CODE']) if not pd.isnull(df.iloc[i]['TRANSACTION_CURRENCY_CODE']) else None #str/NoneType

        self.check_item_tax_code_code = str(df.iloc[i]['PRODUCT_TAX_CODE']) if not pd.isnull(df.iloc[i]['PRODUCT_TAX_CODE']) else None #str/NoneType


        self.departure_country_code = str(df.iloc[i]['DEPARTURE_COUNTRY']) #str
        self.departure_postal_code = str(df.iloc[i]['DEPARTURE_POST_CODE']) #str
        self.departure_city = str(df.iloc[i]['DEPATURE_CITY']) #str

        self.arrival_country_code = str(df.iloc[i]['ARRIVAL_COUNTRY']) #str
        self.arrival_postal_code = str(df.iloc[i]['ARRIVAL_POST_CODE']) #str
        self.arrival_city = str(df.iloc[i]['ARRIVAL_CITY']) #str
        self.arrival_address = str(df.iloc[i]['ARRIVAL_ADDRESS']) if not pd.isnull(df.iloc[i]['ARRIVAL_ADDRESS']) else None #str/NoneType

        self.shipment_mode = str(df.iloc[i]['TRANSPORTATION_MODE']) if not pd.isnull(df.iloc[i]['TRANSPORTATION_MODE']) else None #str/NoneType
        self.shipment_conditions = str(df.iloc[i]['DELIVERY_CONDITIONS']) if not pd.isnull(df.iloc[i]['DELIVERY_CONDITIONS']) else None #str/NoneType


        self.check_departure_seller_vat_country_code = str(df.iloc[i]['SELLER_DEPART_VAT_NUMBER_COUNTRY']) if not pd.isnull(df.iloc[i]['SELLER_DEPART_VAT_NUMBER_COUNTRY']) else None
        self.check_departure_seller_vat_number = str(df.iloc[i]['SELLER_DEPART_COUNTRY_VAT_NUMBER']) if not pd.isnull(df.iloc[i]['SELLER_DEPART_COUNTRY_VAT_NUMBER']) else None

        self.check_arrival_seller_vat_country_code = str(df.iloc[i]['SELLER_ARRIVAL_VAT_NUMBER_COUNTRY']) if not pd.isnull(df.iloc[i]['SELLER_ARRIVAL_VAT_NUMBER_COUNTRY']) else None
        self.check_arrival_seller_vat_number = str(df.iloc[i]['SELLER_ARRIVAL_COUNTRY_VAT_NUMBER']) if not pd.isnull(df.iloc[i]['SELLER_ARRIVAL_COUNTRY_VAT_NUMBER']) else None

        self.check_seller_vat_country_code = str(df.iloc[i]['TRANSACTION_SELLER_VAT_NUMBER_COUNTRY']) if not pd.isnull(df.iloc[i]['TRANSACTION_SELLER_VAT_NUMBER_COUNTRY']) else None
        self.check_seller_vat_number = str(df.iloc[i]['TRANSACTION_SELLER_VAT_NUMBER']) if not pd.isnull(df.iloc[i]['TRANSACTION_SELLER_VAT_NUMBER']) else None


        self.check_tax_calculation_imputation_country = str(df.iloc[i]['VAT_CALCULATION_IMPUTATION_COUNTRY']) if not pd.isnull(df.iloc[i]['VAT_CALCULATION_IMPUTATION_COUNTRY']) else None
        self.check_tax_jurisdiction = str(df.iloc[i]['TAXABLE_JURISDICTION']) if not pd.isnull(df.iloc[i]['TAXABLE_JURISDICTION']) else None
        self.check_tax_jurisdiction_level = str(df.iloc[i]['TAXABLE_JURISDICTION_LEVEL']) if not pd.isnull(df.iloc[i]['TAXABLE_JURISDICTION_LEVEL']) else None

        self.invoice_number = str(df.iloc[i]['VAT_INV_NUMBER']) if not pd.isnull(df.iloc[i]['VAT_INV_NUMBER']) else None
        self.check_invoice_amount_vat = float(df.iloc[i]['VAT_INV_CONVERTED_AMT']) if not pd.isnull(df.iloc[i]['VAT_INV_CONVERTED_AMT']) else None
        self.check_invoice_currency_code = str(df.iloc[i]['VAT_INV_CURRENCY_CODE']) if not pd.isnull(df.iloc[i]['VAT_INV_CURRENCY_CODE']) else None
        self.check_invoice_exchange_rate = float(df.iloc[i]['VAT_INV_EXCHANGE_RATE']) if not pd.isnull(df.iloc[i]['VAT_INV_EXCHANGE_RATE']) else None
        self.check_invoice_exchange_rate_date = datetime.strptime(str(df.iloc[i]['VAT_INV_EXCHANGE_RATE_DATE']), '%d-%m-%Y').date() if not pd.isnull(df.iloc[i]['VAT_INV_EXCHANGE_RATE_DATE']) else None #datetime.date object
        self.invoice_url = str(df.iloc[i]['INVOICE_URL']) if not pd.isnull(df.iloc[i]['INVOICE_URL']) else None


        self.check_export = str(df.iloc[i]['EXPORT_OUTSIDE_EU']) if not pd.isnull(df.iloc[i]['EXPORT_OUTSIDE_EU']) else None #str #-->transaction

        self.customer_name = str(df.iloc[i]['BUYER_NAME']) if not pd.isnull(df.iloc[i]['BUYER_NAME']) else None
        self.customer_vat_number = str(df.iloc[i]['BUYER_VAT_NUMBER']) if not pd.isnull(df.iloc[i]['BUYER_VAT_NUMBER']) else None
        self.customer_vat_number_country = str(df.iloc[i]['BUYER_VAT_NUMBER_COUNTRY'])

        self.supplier_vat_number = str(df.iloc[i]['SUPPLIER_VAT_NUMBER']) if not pd.isnull(df.iloc[i]['SUPPLIER_VAT_NUMBER']) else None # #NoneType/str object #-->transaction
        self.supplier_name = str(df.iloc[i]['SUPPLIER_NAME']) if not pd.isnull(df.iloc[i]['SUPPLIER_NAME']) else None #NoneType/str object #-->transaction























new_sale_transaction = Sale(
    public_id=public_id,
    shipment_id=shipment_id,
    tax_calculation_date=tax_calculation_date,
    shipment_date=shipment_date,
    tax_date=tax_date

)

new_transaction_calculation_reference = TransactionCalculationReference(
    export = export,
    tax_code = tax_code,
    arrival_seller_vat_number_country = arrival_seller_vat_number_country,
    arrival_seller_vat_number = arrival_seller_vat_number,
    departure_seller_vat_number_country = departure_seller_vat_number_country,
    departure_seller_vat_number = departure_seller_vat_number,
    gift_wrap_price_discount_net = gift_wrap_price_discount_net,
    gift_wrap_price_discount_vat = gift_wrap_price_discount_vat,
    gift_wrap_price_net = gift_wrap_price_net,
    gift_wrap_price_vat = gift_wrap_price_vat,
    gift_wrap_price_total_net = gift_wrap_price_total_net,
    gift_wrap_price_total_vat = gift_wrap_price_total_vat,
    gift_wrap_price_vat_rate = gift_wrap_price_vat_rate,
    invoice_amount_vat = invoice_amount_vat,
    invoice_currency_code = invoice_currency_code,
    invoice_exchange_rate = invoice_exchange_rate,
    invoice_exchange_rate_date = invoice_exchange_rate_date,
    item_price_discount_net = item_price_discount_net,
    item_price_discount_vat = item_price_discount_vat,
    item_price_net = item_price_net,
    item_price_vat = item_price_vat,
    item_price_total_net = item_price_total_net,
    item_price_total_vat = item_price_total_vat,
    seller_vat_number = seller_vat_number,
    seller_vat_country_code = seller_vat_country_code,
    shipment_price_discount_net = shipment_price_discount_net,
    shipment_price_discount_vat = shipment_price_discount_vat,
    shipment_price_discount_net = shipment_price_discount_net,
    shipment_price_discount_vat = shipment_price_discount_vat,
    shipment_price_discount_net = shipment_price_discount_net,
    shipment_price_discount_vat = shipment_price_discount_vat,
    check_shipment_price_tax_rate_rate = check_shipment_price_tax_rate_rate,
    sale_total_value_net = sale_total_value_net,
    sale_total_value_vat = sale_total_value_vat,
    tax_jurisdiction = tax_jurisdiction,
    tax_jurisdiction_level = tax_jurisdiction_level,
    vat_calculation_imputation_country = vat_calculation_imputation_country
)
