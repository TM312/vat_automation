
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
    def create(
            user,
            seller_firm,
            platform,
            final_dirpath,
            activity_period) -> Transaction:

        ## A tax record is created by uploading a platform specific input file

        # check if tax record already exists in db
        transaction = Transaction.query.filter_by(
            owner=seller_firm.id
            activity_period=activity_period,
        ).first()

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
            transaction.update(
                creator_id=user.id,
                accounting_firm_id=user.employer_id
            )

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
def read_amazon_txt_upload_into_df(txt_file):
    try:
        df = pd.read_csv(txt_file, encoding='latin-1', delimiter='\t')
        return df
    except:
        raise UnsupportedMediaType('Cannot read file {}.'.format(txt_file))

# MOVE TO PLATFORM --> PlatformService
#   from .model import Account

def get_by_public_id_channel_code(account_public_id, channel_code):
    account = Account.query.filter_by(public_id=account_public_id,  channel_code=channel_code).first()
    if account:
        return account
    else:
        raise NotFound('An account for the channel {} and the id {} does not exist in our db. Please add the account before proceeding.'.format(channel_code, account_public_id))


# ItemService
def get_by_sku_account(item_sku, account):
    if account.channel.platform_name == 'amazon':
        item = Item.query.filter_by(sku=item_sku, seller_firm_id=account.seller_firm_id.).first()
        if item:
            return item
        else:
            raise NotFound('The item specific SKU "{}" is not listed in the item information of the seller. Please update the item information before proceeding'.format(item_sku))

#TaxRateService
def get_tax_code_by_code(tax_code_code):
    tax_code = TaxCode.query.filter_by(code=tax_code_code).first()
    if tax_code_obj:
        return tax_code
    else:
        raise NotFound('The tax code "{}" is currently not supported by our database. Please get in contact with one of the admins.'.format(tax_code_code))

#CountryService
def get_by_code(country_code):
    country = Country.query.filter_by(code=country_code).first()
    if country:
        return country
    else:
        raise NotFound('The country "{}" is currently not supported by our database. Please get in contact with one of the admins.'.format(country_code))

#TaxRateService
def get_by_tax_code_country_tax_date(tax_code, country, tax_date):
    tax_rate = TaxRate.query.filter(TaxRate.tax_code==tax_code, TaxRate.country==country, TaxRate.valid_from<tax_date, TaxRate.valid_to>tax_date).first()
    if tax_rate:
        return tax_rate
    else:
        raise NotFound('The tax rate for the tax code: "{}" and the country: "{}" could not be found. Please get in contact with one of the admins.'.format(tax_code, country.name))

#TaxRateService
def get_by_tax_rate_type_country_tax_date(country, tax_rate_type_name, tax_date)
    tax_rate = TaxRate.query.filter(TaxRate.country==country, TaxRate.tax_rate_type_name==tax_rate_type_name, TaxRate.valid_from<tax_date, TaxRate.valid_to>tax_date).first()
    if tax_rate:
        return tax_rate
    else:
        raise NotFound('The tax rate for the tax rate type "{}" and the country "{}" could not be found. Please get in contact with one of the admins.'.format(tax_rate_type_name, country.name))


def get_transaction_type_by_public_code_account(transaction_type_public_code, account):
    if account.channel.platform_name == 'amazon':
        if transaction_type_code == 'SALE' or transaction_type_public_code == 'COMMINGLING_SELL':
            transaction_type = TransactionType.query.filter_by(name="SALE").first()
            return transaction_type

        # elif transaction_type_code == 'REFUND':
        #     transaction_type = TransactionType.query.filter_by(name="SALE").first()
        #     return transaction_type

        # elif transaction_type_code == 'REFUND':
        #     transaction_type = TransactionType.query.filter_by(name="SALE").first()
        #     return transaction_type


        else:
            raise NotFound('The indicated transaction type "{}" is not supported. Please get in touch with one of the administrators.'.format(transaction_type_code))

    else:
        raise NotFound('The platform for the transaction account "{}" is currently not supported. Please get in touch with one of the administrators.'.format(account.public_id))


## MASTER FUNCTION
def transaction_processing():

    df =

    for i in len(df.index):
        account_public_id, public_activity_period, channel_code, marketplace_name, transaction_type_public_code, transaction_public_id, transaction_activity_public_id, tax_calculation_date, shipment_date, arrival_date, tax_date, item_sku, item_name, item_manufacture_country, item_quantity, item_weight_kg, item_weight_kg_total, unit_cost_price_net, item_price_discount_net, item_price_discount_vat, item_price_discount_gross, item_price_net, item_price_vat, item_price_gross, item_price_total_net, item_price_total_vat, item_price_total_gross, shipment_price_discount_net, shipment_price_discount_vat, shipment_price_discount_gross, shipment_price_net, shipment_price_vat, shipment_price_gross, shipment_price_total_net, shipment_price_total_vat, shipment_price_total_gross, shipment_price_vat_rate, sale_total_value_net, sale_total_value_vat, sale_total_value_gross, gift_wrap_price_discount_net, gift_wrap_price_discount_vat, gift_wrap_price_discount_gross, gift_wrap_price_net, gift_wrap_price_vat, gift_wrap_price_gross, gift_wrap_price_total_net, gift_wrap_price_total_vat, gift_wrap_price_total_gross, gift_wrap_price_vat_rate, currency_code, tax_code, departure_country_code, departure_postal_code, departure_city, arrival_country_code, arrival_postal_code, arrival_city, arrival_address, shipment_mode, shipment_conditions, departure_seller_vat_number_country, departure_seller_vat_number, arrival_seller_vat_number_country, arrival_seller_vat_number, seller_vat_number_country, seller_vat_number, tax_calculation_imputation_country, tax_jurisdiction, tax_jurisdiction_level, invoice_number, invoice_amount_vat, invoice_currency_code, invoice_exchange_rate, invoice_exchange_rate_date, invoice_url, export, customer_name, customer_vat_number, customer_vat_number_country, supplier_vat_number, supplier_name = TransactionService.load_transaction_vars_from_df(df, i)

        #amazon_vat_calculation_service = TransactionService.check_amazon_vat_calculation_service(tax_calculation_date)


        arrival_country = CountryService.get_by_code(arrival_country_code)
        departure_country = CountryService.get_by_code(departure_country_code)


def check_amazon_vat_calculation_service(tax_calculation_date):
    amazon_vat_calculation_service = True if tax_calculation_date else False
    return amazon_vat_calculation_service

def define_customer_type(customer_vat_number):
    customer_type_code = 'B2C' if not customer_vat_number else --> CHECK VAT NUMBER
    !!! --> "B2B"
    return customer_type_code

#CountryService
def get_eu_by_date(date):
    eu = EU.query.filter(EU.valid_from<=date, EU.valid_to>=date).first()
    if eu:
        return eu
    else:
        raise NotFound('A constellation of EU countries has not been defined for the requested date ({})'.format(str(date)))



#def get_by_code(country_code)


def define_tax_treatment_code(account, check_export, eu, customer_type, departure_country, arrival_country, amazon_vat_calculation_service, check_item_price_vat_rate):
    if (check_export == 'YES' or arrival_country not in eu.countries):
        tax_treatment_code = 'EXPORT'

    elif customer_type.code == "B2B"
        if departure_country.code != arrival_country.code:
            tax_treatment_code = 'INTRA_COMMUNITY_SALE'

        else:
            if (
            (departure_country.code in ['ES', 'FR', 'IT', 'PL'] and departure_country.code != account.seller_firm.establishment_country_code) or
            (amazon_vat_calculation_service and check_item_price_vat_rate == 0)
            ):
            tax_treatment_code = 'LOCAL_SALE_REVERSE_CHARGE'


            else:
                tax_treatment_code = 'DISTANCE_SALE'

    else:
        tax_treatment_code = 'LOCAL_SALE' ???

    return tax_treatment_code


def define_tax_jurisdiction(tax_treatment_code, departure_country, arrival_country):
    tax_treatment_code == 'DISTANCE_SALE':
        tax_jurisdiction = arrival_country.code
    else:
        tax_jurisdiction = departure_country.code

    return tax_jurisdiction


def get_vat_rates(tax_jurisdiction, tax_treatment_code, tax_code, tax_date):
    if tax_treatment_code == 'EXPORT' or 'INTRA_COMMUNITY_SALE' or 'LOCAL_SALE_REVERSE_CHARGE':
        item_price_vat_rate, gift_wrap_rate, shipment_price_vat_rate = 0
    else:
        item_price_vat_rate = TaxRateService.get_by_tax_code_country_tax_date(tax_code=tax_code, country=tax_jurisdiction, tax_date=tax_date)
        shipment_price_vat_rate = gift_wrap_rate = TaxRateService.get_by_tax_rate_type_country_tax_date(country=tax_jurisdiction, tax_rate_type_name='S', tax_date=tax_dat = TaxRateService.get_by_tax_rate_type_country_tax_date(country=tax_jurisdiction, tax_rate_type_name='S', tax_date=tax_date)

    return item_price_vat_rate, gift_wrap_rate, shipment_price_vat_rate


# write a smart sanitizing function when time available
def load_transaction_vars_from_df(df, i):
    account_public_id = str(df.iloc[i]['UNIQUE_ACCOUNT_IDENTIFIER']).upper() #-->PlatformService.retrieve_account()
    public_activity_period = str(df.iloc[i]['ACTIVITY_PERIOD']).upper() # --> OUTPUT
    channel_code = str(df.iloc[i]['SALES_CHANNEL']).upper() # str #-->PlatformService.retrieve_account()
    marketplace_name = str(df.iloc[i]['MARKETPLACE']).lower() # str #-->transaction
    transaction_type_public_code = str(df.iloc[i]['TRANSACTION_TYPE']).upper() #-->TransactionService.retrieve_transaction_type()
    transaction_public_id = str(df.iloc[i]['TRANSACTION_EVENT_ID']) # str #-->transaction
    transaction_activity_public_id = str(df.iloc[i]['ACTIVITY_TRANSACTION_ID'])  # str #-->transaction --> becomes shipment_id/return_id , etc.

    tax_calculation_date = datetime.strptime(df.iloc[i]['TAX_CALCULATION_DATE'], '%d-%m-%Y').date() if not pd.isnull(df.iloc[i]['TAX_CALCULATION_DATE']) else None  #NoneType/datetime.date object #-->transaction
    shipment_date = datetime.strptime(df.iloc[i]['TRANSACTION_DEPART_DATE'], '%d-%m-%Y').date() if not pd.isnull(df.iloc[i]['TRANSACTION_DEPART_DATE']) else None #datetime.date object #-->transaction
    arrival_date = datetime.strptime(df.iloc[i]['TRANSACTION_ARRIVAL_DATE'], '%d-%m-%Y').date() if not pd.isnull(df.iloc[i]['TRANSACTION_ARRIVAL_DATE']) else None #datetime.date object #-->transaction
    tax_date = datetime.strptime(df.iloc[i]['TRANSACTION_COMPLETE_DATE'], '%d-%m-%Y').date() if not pd.isnull(df.iloc[i]['TRANSACTION_COMPLETE_DATE']) else None #datetime.date object #-->transaction

    item_sku = str(df.iloc[i]['SELLER_SKU']) # str --> ItemService.retrieve_item() --> transaction
    item_name = str(df.iloc[i]['ITEM_DESCRIPTION']) #str
    item_manufacture_country = str(df.iloc[i]['ITEM_MANUFACTURE_COUNTRY']) if not pd.isnull(df.iloc[i]['ITEM_MANUFACTURE_COUNTRY']) else None #str/NoneType
    item_quantity = int(df.iloc[i]['QTY']) #-->transaction
    item_weight_kg = float(df.iloc[i]['ITEM_WEIGHT']) if not pd.isnull(df.iloc[i]['ITEM_WEIGHT']) else None #float/NoneType
    item_weight_kg_total = float(df.iloc[i]['TOTAL_ACTIVITY_WEIGHT']) if not pd.isnull(df.iloc[i]['TOTAL_ACTIVITY_WEIGHT']) else None

    unit_cost_price_net = float(df.iloc[i]['COST_PRICE_OF_ITEMS']) if not pd.isnull(df.iloc[i]['COST_PRICE_OF_ITEMS']) else None

    item_price_discount_net = float(df.iloc[i]['PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None
    item_price_discount_vat = float(df.iloc[i]['PROMO_PRICE_OF_ITEMS_VAT_AMT']) if not pd.isnull(df.iloc[i]['PROMO_PRICE_OF_ITEMS_VAT_AMT']) else None
    item_price_discount_gross = float(df.iloc[i]['PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL']) else None #-->transaction

    item_price_net = float(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None
    item_price_vat = float(df.iloc[i]['PRICE_OF_ITEMS_VAT_AMT']) if not pd.isnull(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None
    item_price_gross = float(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None #-->transaction

    item_price_total_net = float(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL']) else None
    item_price_total_vat = float(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_VAT_AMT']) if not pd.isnull(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_VAT_AMT']) else None
    item_price_total_gross = float(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL']) else None #-->transaction

    check_item_price_vat_rate = float(df.iloc[i]['PRICE_OF_ITEMS_VAT_RATE_PERCENT']) if not pd.isnull(df.iloc[i]['PRICE_OF_ITEMS_VAT_RATE_PERCENT']) else None


    shipment_price_discount_net = float(df.iloc[i]['PROMO_SHIP_CHARGE_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) else None
    shipment_price_discount_vat = float(df.iloc[i]['PROMO_SHIP_CHARGE_VAT_AMT']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) else None
    shipment_price_discount_gross = float(df.iloc[i]['PROMO_SHIP_CHARGE_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['PROMO_GIFT_WRAP_AMT_VAT_EXCL']) else None #-->transaction

    shipment_price_net = float(df.iloc[i]['SHIP_CHARGE_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['SHIP_CHARGE_AMT_VAT_EXCL']) else None
    shipment_price_vat = float(df.iloc[i]['SHIP_CHARGE_VAT_AMT']) if not pd.isnull(df.iloc[i]['SHIP_CHARGE_VAT_AMT']) else None
    shipment_price_gross = float(df.iloc[i]['SHIP_CHARGE_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['SHIP_CHARGE_AMT_VAT_INCL']) else None #-->transaction

    shipment_price_total_net = float(df.iloc[i]['TOTAL_SHIP_CHARGE_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['TOTAL_SHIP_CHARGE_AMT_VAT_EXCL']) else None
    shipment_price_total_vat = float(df.iloc[i]['TOTAL_SHIP_CHARGE_VAT_AMT']) if not pd.isnull(df.iloc[i]['TOTAL_SHIP_CHARGE_VAT_AMT']) else None
    shipment_price_total_gross = float(df.iloc[i]['TOTAL_SHIP_CHARGE_AMT_VAT_INCL']) if not pd.isnull(df.iloc[i]['TOTAL_SHIP_CHARGE_AMT_VAT_INCL']) else None #-->transaction

    shipment_price_vat_rate = float(df.iloc[i]['SHIP_CHARGE_VAT_RATE_PERCENT']) if not pd.isnull(df.iloc[i]['SHIP_CHARGE_VAT_RATE_PERCENT']) else None

    sale_total_value_net = float(df.iloc[i]['TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL']) if not pd.isnull(df.iloc[i]['TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL']) else None
    sale_total_value_vat = float(df.iloc[i]['TOTAL_ACTIVITY_VALUE_VAT_AMT']) if not pd.isnull(df.iloc[i]['TOTAL_ACTIVITY_VALUE_VAT_AMT']) else None
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

    check_gift_wrap_price_vat_rate = float(df.iloc[i]['GIFT_WRAP_VAT_RATE_PERCENT']) if not pd.isnull(df.iloc[i]['GIFT_WRAP_VAT_RATE_PERCENT']) else None


    currency_code = str(df.iloc[i]['TRANSACTION_CURRENCY_CODE']) if not pd.isnull(df.iloc[i]['TRANSACTION_CURRENCY_CODE']) else None #str/NoneType

    check_item_tax_code_code = str(df.iloc[i]['PRODUCT_TAX_CODE']) if not pd.isnull(df.iloc[i]['PRODUCT_TAX_CODE']) else None #str/NoneType


    departure_country_code = str(df.iloc[i]['DEPARTURE_COUNTRY']) #str
    departure_postal_code = str(df.iloc[i]['DEPARTURE_POST_CODE']) #str
    departure_city = str(df.iloc[i]['DEPATURE_CITY']) #str

    arrival_country_code = str(df.iloc[i]['ARRIVAL_COUNTRY']) #str
    arrival_postal_code = str(df.iloc[i]['ARRIVAL_POST_CODE']) #str
    arrival_city = str(df.iloc[i]['ARRIVAL_CITY']) #str
    arrival_address = str(df.iloc[i]['ARRIVAL_ADDRESS']) if not pd.isnull(df.iloc[i]['ARRIVAL_ADDRESS']) else None #str/NoneType

    shipment_mode = str(df.iloc[i]['TRANSPORTATION_MODE']) if not pd.isnull(df.iloc[i]['TRANSPORTATION_MODE']) else None #str/NoneType
    shipment_conditions = str(df.iloc[i]['DELIVERY_CONDITIONS']) if not pd.isnull(df.iloc[i]['DELIVERY_CONDITIONS']) else None #str/NoneType

    departure_seller_vat_number_country = str(df.iloc[i]['SELLER_DEPART_VAT_NUMBER_COUNTRY']) if not pd.isnull(df.iloc[i]['SELLER_DEPART_VAT_NUMBER_COUNTRY']) else None
    departure_seller_vat_number = str(df.iloc[i]['SELLER_DEPART_COUNTRY_VAT_NUMBER']) if not pd.isnull(df.iloc[i]['SELLER_DEPART_COUNTRY_VAT_NUMBER']) else None

    check_arrival_seller_vat_number_country = str(df.iloc[i]['SELLER_ARRIVAL_VAT_NUMBER_COUNTRY']) if not pd.isnull(df.iloc[i]['SELLER_ARRIVAL_VAT_NUMBER_COUNTRY']) else None
    check_arrival_seller_vat_number = str(df.iloc[i]['SELLER_ARRIVAL_COUNTRY_VAT_NUMBER']) if not pd.isnull(df.iloc[i]['SELLER_ARRIVAL_COUNTRY_VAT_NUMBER']) else None

    check_seller_vat_number_country = str(df.iloc[i]['TRANSACTION_SELLER_VAT_NUMBER_COUNTRY']) if not pd.isnull(df.iloc[i]['TRANSACTION_SELLER_VAT_NUMBER_COUNTRY']) else None
    check_seller_vat_number = str(df.iloc[i]['TRANSACTION_SELLER_VAT_NUMBER']) if not pd.isnull(df.iloc[i]['TRANSACTION_SELLER_VAT_NUMBER']) else None


    tax_calculation_imputation_country = str(df.iloc[i]['VAT_CALCULATION_IMPUTATION_COUNTRY']) if not pd.isnull(df.iloc[i]['VAT_CALCULATION_IMPUTATION_COUNTRY']) else None
    check_tax_jurisdiction = str(df.iloc[i]['TAXABLE_JURISDICTION']) if not pd.isnull(df.iloc[i]['TAXABLE_JURISDICTION']) else None
    tax_jurisdiction_level = str(df.iloc[i]['TAXABLE_JURISDICTION_LEVEL']) if not pd.isnull(df.iloc[i]['TAXABLE_JURISDICTION_LEVEL']) else None

    invoice_number = str(df.iloc[i]['VAT_INV_NUMBER']) if not pd.isnull(df.iloc[i]['VAT_INV_NUMBER']) else None
    check_invoice_amount_vat = float(df.iloc[i]['VAT_INV_CONVERTED_AMT']) if not pd.isnull(df.iloc[i]['VAT_INV_CONVERTED_AMT']) else None
    check_invoice_currency_code = str(df.iloc[i]['VAT_INV_CURRENCY_CODE']) if not pd.isnull(df.iloc[i]['VAT_INV_CURRENCY_CODE']) else None
    check_invoice_exchange_rate = float(df.iloc[i]['VAT_INV_EXCHANGE_RATE']) if not pd.isnull(df.iloc[i]['VAT_INV_EXCHANGE_RATE']) else None
    invoice_exchange_rate_date = datetime.strptime(str(df.iloc[i]['VAT_INV_EXCHANGE_RATE_DATE']), '%d-%m-%Y').date() if not pd.isnull(df.iloc[i]['VAT_INV_EXCHANGE_RATE_DATE']) else None #datetime.date object
    invoice_url = str(df.iloc[i]['INVOICE_URL']) if not pd.isnull(df.iloc[i]['INVOICE_URL']) else None


    check_export = str(df.iloc[i]['EXPORT_OUTSIDE_EU']) if not pd.isnull(df.iloc[i]['EXPORT_OUTSIDE_EU']) else None #str #-->transaction

    customer_name = str(df.iloc[i]['BUYER_NAME']) if not pd.isnull(df.iloc[i]['BUYER_NAME']) else None
    customer_vat_number = str(df.iloc[i]['BUYER_VAT_NUMBER']) if not pd.isnull(df.iloc[i]['BUYER_VAT_NUMBER']) else None
    customer_vat_number_country = str(df.iloc[i]['BUYER_VAT_NUMBER_COUNTRY'])

    supplier_vat_number = str(df.iloc[i]['SUPPLIER_VAT_NUMBER']) if not pd.isnull(df.iloc[i]['SUPPLIER_VAT_NUMBER']) else None # #NoneType/str object #-->transaction
    supplier_name = str(df.iloc[i]['SUPPLIER_NAME']) if not pd.isnull(df.iloc[i]['SUPPLIER_NAME']) else None #NoneType/str object #-->transaction


    return account_public_id, public_activity_period, channel_code, marketplace_name, transaction_type_public_code, transaction_public_id, transaction_activity_public_id, tax_calculation_date, shipment_date, arrival_date, tax_date, item_sku, item_name, item_manufacture_country, item_quantity, item_weight_kg, item_weight_kg_total, unit_cost_price_net, item_price_discount_net, item_price_discount_vat, item_price_discount_gross, item_price_net, item_price_vat, item_price_gross, item_price_total_net, item_price_total_vat, item_price_total_gross, check_item_price_vat_rate, shipment_price_discount_net, shipment_price_discount_vat, shipment_price_discount_gross, shipment_price_net, shipment_price_vat, shipment_price_gross, shipment_price_total_net, shipment_price_total_vat, shipment_price_total_gross, shipment_price_vat_rate, shipment_price_vat_rate, sale_total_value_net, sale_total_value_vat, sale_total_value_gross, gift_wrap_price_discount_net, gift_wrap_price_discount_vat, gift_wrap_price_discount_gross, gift_wrap_price_net, gift_wrap_price_vat, gift_wrap_price_gross, gift_wrap_price_total_net, gift_wrap_price_total_vat, gift_wrap_price_total_gross, gift_wrap_price_vat_rate, currency_code, tax_code_code, departure_country_code, departure_postal_code, departure_city, arrival_country_code, arrival_postal_code, arrival_city, arrival_address, shipment_mode, shipment_conditions, departure_seller_vat_number_country, departure_seller_vat_number, arrival_seller_vat_number_country, arrival_seller_vat_number, seller_vat_number_country, seller_vat_number, tax_calculation_imputation_country, check_tax_jurisdiction, tax_jurisdiction_level, invoice_number, invoice_amount_vat, invoice_currency_code, invoice_exchange_rate, invoice_exchange_rate_date, invoice_url, check_export, customer_name, customer_vat_number, customer_vat_number_country, supplier_vat_number, supplier_name
