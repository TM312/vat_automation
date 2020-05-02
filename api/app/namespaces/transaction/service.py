
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

class ExchangeRateService:
    def get_rate_by_base_target_date(base, target, date):
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


    @staticmethod
    def get_date_or_None(df, i:int, column:str):
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
    def get_str_or_None(df, i:int, column:str):
        if pd.isnull(df.iloc[i][column]):
            return None
        else:
            try:
                string = str(df.iloc[i][column])
            except:
                raise UnsupportedMediaType('Can not read date format.')

        return string


# class OutputService:
#     @staticmethod
#     def check_non_taxable_distance_sale(departure_country, tax_treatment_code):
#         return (departure_country.code == 'PL' and tax_treatment_code == 'DISTANCE_SALE')

#     @staticmethod
#     def calculate_non_taxable_distance_sale(departure_country, total_value_vat, tax_jurisdiction):
#         ExchangeRateService.get_rate_by_base_target_date(base=tax_jurisdiction.currency_code, target=departure_country.currency_code, date=exchange_rate_date)


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
    def get_by_tax_code_country_tax_date(tax_code_code, country, tax_date) -> TaxRate:
        tax_rate: Rate = TaxRate.query.filter(TaxRate.tax_code==tax_code_code, TaxRate.country==country, TaxRate.valid_from<tax_date, TaxRate.valid_to>tax_date).first()
        if tax_rate:
            return tax_rate
        else:
            raise NotFound('The tax rate for the tax code: "{}" and the country: "{}" could not be found. Please get in contact with one of the admins.'.format(tax_code, country.name))

    @staticmethod
    def get_by_tax_rate_type_country_tax_date(country, tax_rate_type_name, tax_date) -> TaxRate:
        tax_rate: TaxRate = TaxRate.query.filter(TaxRate.country==country, TaxRate.tax_rate_type_name==tax_rate_type_name, TaxRate.valid_from<tax_date, TaxRate.valid_to>tax_date).first()
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


    # TransactionService:
    @staticmethod
    def vat_check_required(date: date, number: str) -> bool:
        if not number:
            return False

        else:
            return date.today() - timedelta(days=current_app.config['OLD_TRANSACTION_TOLERANCE_DAYS']) <= date



class CustomerService:

    @staticmethod
    def get_customer_type(check_required: bool, country_code: str, number: str, date: date) -> str:
        if not number:
            customer_type = 'B2C'

        elif number and check_required:
            customer_type = 'B2B' if VATINService.check_validity(country_code, number, date) else 'B2C'

        elif number and not check_required:
            customer_type = 'B2B'

        return customer_type






class TransactionService:

    @staticmethod
    def get_tax_rate_rate(tax_jurisdiction: Country, tax_treatment_code: str, item_tax_code_code: str, tax_date: date, **kwargs) -> float:
        if tax_treatment_code == 'EXPORT' or 'INTRA_COMMUNITY_SALE' or 'LOCAL_SALE_REVERSE_CHARGE':
            tax_rate_rate = float(0)

        if 'check_tax_rate_rate' in kwargs:
            tax_rate_rate = kwargs['check_tax_rate_rate']


        elif 'tax_rate_type_name' in kwargs:
            tax_rate_rate = TaxRateService.get_by_tax_rate_type_country_tax_date(country=tax_jurisdiction, tax_rate_type_name=kwargs['tax_rate_type_name'], tax_date=tax_date).rate

        elif 'tax_code_code' in kwargs:
            tax_rate_rate = TaxRateService.get_by_tax_code_country_tax_date(tax_code_code=kwargs['tax_code_code'], country=tax_jurisdiction, tax_date=tax_date).rate

        return tax_rate_rate



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
            #     transaction_type = TransactionType.query.filter_by(cide="SALE").first()
            #     return transaction_type


            else:
                raise NotFound('The indicated transaction type "{}" is not supported. Please get in touch with one of the administrators.'.format(transaction_type_code))

        else:
            raise NotFound('The platform for the transaction account "{}" is currently not supported. Please get in touch with one of the administrators.'.format(account.public_id))

        return transaction_type



## MASTER FUNCTION
def transaction_processing(file) -> Transaction:

   try:
       df = read_amazon_upload_into_df(file)
    except:
        raise UnsupportedMediaType('Error while reading the input file ({}).'.format(str(file))) !!!! filename


    validity_dict_customer, validity_dict_departure_seller, validity_dict_arrival_seller, validity_dict_seller = check_and_create_vatin(df)


    for i in range(len(df.index)):
        input = Input(df, i)
        calculation = TransactionService.create_calculation_from_input(input)

        create_transaction_from_input_calculation(input, calculation)

        create_transaction_reference_from_input_calculation(input)


## END MASTER FUNCTION ##


    def create_calculation_from_input(input)

        amazon_vat_calculation_service: bool = TransactionService.check_amazon_vat_calculation_service(input.check_tax_calculation_date)

        account: Account = PlatformService.get_by_public_id_channel_code(input.account_public_id, input.channel_code)
        item: Item = ItemService.get_by_sku_account_date(input.item_sku, account, input.tax_date)
        bundle: Bundle = TransactionService.get_bundle_by_account_item_transaction_public_id(account, item, input.transaction_public_id) !!! #may be empty: in that case need to be created later





        transaction_type: TransactionType = get_transaction_type_by_public_code_account(input.transaction_type_public_code, account)

        arrival_country: Country = CountryService.get_by_code(input.arrival_country_code)
        departure_country: Country = CountryService.get_by_code(input.departure_country_code)
        eu: EU = CountryService.get_eu_by_date(input.tax_date) #EU

        customer_type_checked: bool = TransactionService.vat_check_required(date=input.tax_date, number=input.customer_vat_number)
        customer_type: str = CustomerService.get_customer_type(country_code=input.customer_vat_number_country_code, number=input.customer_vat_number, date=input.tax_date)



        tax_treatment_code: str = TaxRateService.define_tax_treatment_code(account, input.check_export, eu, customer_type, departure_country, arrival_country, amazon_vat_calculation_service, input.check_item_price_tax_rate_rate)

        tax_juristdiction: Country = TransactionService.define_tax_jurisdiction(tax_treatment_code, departure_country, arrival_country)
        item_tax_code_code: str = TransactionService.get_item_tax_code_code(item, input.check_item_tax_code_code)

        item_price_tax_rate_rate: float = TransactionService.get_tax_rate_rate(tax_jurisdiction=tax_jurisdiction, tax_treatment_code=tax_treatment_code, tax_date=input.tax_date, tax_code_code=item_tax_code_code, check_tax_rate_rate=input.check_item_price_tax_rate_rate)
        gift_wrap_tax_rate_rate: float = TransactionService.get_tax_rate_rate(tax_jurisdiction=tax_jurisdiction, tax_treatment_code=tax_treatment_code, tax_date=input.tax_date, tax_rate_type_name='S')
        shipment_price_tax_rate_rate : float= TransactionService.get_tax_rate_rate(tax_jurisdiction=tax_jurisdiction, tax_treatment_code=tax_treatment_code, tax_date=input.tax_date, tax_rate_type_name='S')


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

        invoice_exchange_rate_date: date = get_invoice_exchange_rate_date(transaction_type, bundle, input.currency_code, invoice_currency_code, input.tax_date)
        invoice_exchange_rate: float = get_invoice_exchange_rate(invoice_exchange_rate_date=invoice_exchange_rate_date, currency_code=input.currency_code, invoice_currency_code=invoice_currency_code)


        invoice_amount_net: float = TransactionService.get_invoice_amount(total_value_net, invoice_exchange_rate)
        invoice_amount_vat: float = TransactionService.get_invoice_amount(total_value_vat, invoice_exchange_rate)
        invoice_amount_gross: float = TransactionService.get_invoice_amount(total_value_gross, invoice_exchange_rate)

        # self.arrival_seller_vat_country_code: str = arrival_country.vat_country_code
        # self.departure_seller_vat_country_code: str = departure_country.vat_country_code
        # self.seller_vat_country_code: str = tax_juristdiction.vat_country_code

        arrival_seller_vat_valid: bool = VATINService.check_validity(country_code: arrival_country.vat_country_code, number=input.check_arrival_seller_vat_number, date=input.tax_date)
        departure_seller_vat_valid: bool = VATINService.check_validity(country_code: departure_country.vat_country_code, number=input.check_departure_seller_vat_number, date=input.tax_date)
        seller_vat_valid: bool = VATINService.check_validity(country_code: tax_juristdiction.vat_country_code, number=input.check_seller_vat_number, date=input.tax_date)





    @staticmethod
    def get_bundle_by_account_item_transaction_public_id(account: Account, item: Item, transaction_public_id: str) -> Bundle:
        bundle = Bundle.query.join(Bundle.transactions, aliased=True).filter_by(account_id=account.id, item_id=item.id, public_id=transaction_public_id).first()
        return bundle


    @staticmethod
    def get_sale_transaction_by_bundle(bundle) -> Transaction:
        sale_transaction = Transaction.query.filter_by(bundle_id=bundle.id, t_type='sale').first()
        return sale_transaction


    @staticmethod
    def get_transactions_by_bundle_transaction_type(bundle: Bundle, transaction_type: TransactionType) -> List[Transaction]:
        transactions = Transaction.query.filter_by(bundle_id=bundle.id, t_type=transaction_type.code).all()
        return transactions


    @staticmethod
    def get_invoice_amount(total_value: float, invoice_exchange_rate: float) -> float:
        invoice_amount = float(total_value * invoice_exchange_rate)
        return invoice_amount


    @staticmethod
    def get_invoice_exchange_rate_date(transaction_type: TransactionType, bundle: Bundle, currency_code: str, invoice_currency_code: str, tax_date: date) -> float or None:
        if check_exchange_rate_required(currency_code, invoice_currency_code):
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
    def get_invoice_exchange_rate(invoice_exchange_rate_date: date, currency_code: str, invoice_currency_code: str) -> float:
        if invoice_exchange_rate_date:
            invoice_exchange_rate = ExchangeRateService.get_rate_by_base_target_date(base=currency_code, target=invoice_currency_code, date=invoice_exchange_rate_date)

        else:
            invoice_exchange_rate = float(1)

        return invoice_exchange_rate


    @staticmethod
    def check_exchange_rate_required(currency_code: str, invoice_currency_code: str) -> bool:
        return not currency_code == invoice_currency_code


    @staticmethod
    def get_price_net(price_gross: float, price_tax_rate: float) ->float:
        price_net = float(price_gross / (1 + price_tax_rate))
        return price_net

    @staticmethod
    def get_price_vat(price_gross: float, price_tax_rate: float) -> float:
        price_vat = float(price_gross / (1 + price_tax_rate) * price_tax_rate)
        return price_vat

    @staticmethod
    def get_total_value(item_price_total: float, shipment_price_total: float, gift_wrap_price_total: float) -> float:
        return item_price_total + shipment_price_total + gift_wrap_price_total



    @staticmethod
    def check_amazon_vat_calculation_service(check_tax_calculation_date) -> bool:
        return True if check_tax_calculation_date else False

    @staticmethod
    def get_tax_calculation_date(check_tax_calculation_date, tax_date: date) -> date:
        return check_tax_calculation_date if check_tax_calculation_date else tax_date


    #TransactioService
    @staticmethod
    def define_tax_jurisdiction(tax_treatment_code: str, departure_country: Country, arrival_country: Country) -> Country:
        if tax_treatment_code == 'DISTANCE_SALE':
            tax_jurisdiction_code = arrival_country.code
        else:
            tax_jurisdiction_code = departure_country.code
        tax_jurisdiction = CountryService.get_by_code(country_code = tax_jurisdiction_code)

        return tax_jurisdiction

    @staticmethod
    def get_item_tax_code_code(item: Item, check_item_tax_code_code) -> str:
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
input.customer_vat_number_country_code,
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
class Input(db.Model):
account_public_id = db.Column(db.String(128))
public_activity_period = db.Column(db.String(128))
channel_code = db.Column(db.String(128))
marketplace_name = db.Column(db.String(128))
transaction_type_public_code = db.Column(db.String(128))
transaction_public_id = db.Column(db.String(128))
transaction_activity_id = db.Column(db.String(128))
shipment_date = db.Column(db.Date)
arrival_date = db.Column(db.Date)
tax_date = db.Column(db.Date)
item_sku = db.Column(db.String(128))
item_name = db.Column(db.String(128))
item_manufacture_country = db.Column(db.String(128))
item_quantity = db.Column(db.Integer)
item_weight_kg = db.Float(precision=)
item_weight_kg_total
unit_cost_price_net
item_price_discount_gross
item_price_gross
item_price_total_gross
shipment_price_discount_gross
shipment_price_gross
shipment_price_total_gross
sale_total_value_gross
gift_wrap_price_discount_gross
gift_wrap_price_gross
gift_wrap_price_total_gross
currency_code
departure_country_code
departure_postal_code
departure_city
arrival_country_code
arrival_postal_code
arrival_city
arrival_address
shipment_mode
shipment_conditions
invoice_number
invoice_url
customer_name
customer_vat_number
customer_vat_number_country_code
supplier_vat_number
supplier_name

check_tax_calculation_date
check_item_price_discount_net
check_item_price_discount_vat
check_item_price_net
check_item_price_vat
check_item_price_total_net
check_item_price_total_vat
check_item_price_tax_rate_rate
check_shipment_price_discount_net
check_shipment_price_discount_vat
check_shipment_price_net
check_shipment_price_vat
check_shipment_price_total_net
check_shipment_price_total_vat
check_shipment_price_tax_rate_rate
check_sale_total_value_net
check_sale_total_value_vat
check_gift_wrap_price_discount_net
check_gift_wrap_price_discount_vat
check_gift_wrap_price_net
check_gift_wrap_price_vat
check_gift_wrap_price_total_net
check_gift_wrap_price_total_vat
check_gift_wrap_price_tax_rate
check_item_tax_code_code
check_departure_seller_vat_country_code
check_departure_seller_vat_number
check_arrival_seller_vat_country_code
check_arrival_seller_vat_number
check_seller_vat_country_code
check_seller_vat_number
check_tax_calculation_imputation_country
check_tax_jurisdiction
check_tax_jurisdiction_level
check_invoice_amount_vat
check_invoice_currency_code
check_invoice_exchange_rate
check_invoice_exchange_rate_date
check_export












    def __init__(self,df, i):
        self.account_public_id = InputService.get_str_or_None(df, i, column='UNIQUE_ACCOUNT_IDENTIFIER').upper()
        self.public_activity_period = InputService.get_str_or_None(df, i, column='ACTIVITY_PERIOD').upper() # --> OUTPUT
        self.channel_code = InputService.get_str_or_None(df, i, column='SALES_CHANNEL').upper() # str #-->PlatformService.retrieve_account()
        self.marketplace_name = InputService.get_str_or_None(df, i, column='MARKETPLACE') # str #-->transaction
        self.transaction_type_public_code = InputService.get_str_or_None(df, i, column='TRANSACTION_TYPE') #-->TransactionService.retrieve_transaction_type()
        self.transaction_public_id = str(df.iloc[i]['TRANSACTION_EVENT_ID']) # str #-->transaction
        self.transaction_activity_id = str(df.iloc[i]['ACTIVITY_TRANSACTION_ID'])  # str #-->transaction --> becomes shipment_id/return_id , etc.

        self.check_tax_calculation_date = InputService.get_date_or_None(df, i, column='TAX_CALCULATION_DATE')
        self.shipment_date = InputService.get_date_or_None(df, i, column='TRANSACTION_DEPART_DATE')
        self.arrival_date = InputService.get_date_or_None(df, i, column='TRANSACTION_ARRIVAL_DATE')
        self.tax_date = InputService.get_date_or_None(df, i, column='TRANSACTION_COMPLETE_DATE')

        self.item_sku = str(df.iloc[i]['SELLER_SKU']) # str --> ItemService.retrieve_item() --> transaction
        self.item_name = str(df.iloc[i]['ITEM_DESCRIPTION']) #str
        self.item_manufacture_country = InputService.get_str_or_None(df, i, column='ITEM_MANUFACTURE_COUNTRY') #str/NoneType
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


        self.currency_code = InputService.get_str_or_None(df, i, column='TRANSACTION_CURRENCY_CODE') #str/NoneType

        self.check_item_tax_code_code = InputService.get_str_or_None(df, i, column='PRODUCT_TAX_CODE') #str/NoneType


        self.departure_country_code = str(df.iloc[i]['DEPARTURE_COUNTRY']) #str
        self.departure_postal_code = str(df.iloc[i]['DEPARTURE_POST_CODE']) #str
        self.departure_city = str(df.iloc[i]['DEPATURE_CITY']) #str

        self.arrival_country_code = str(df.iloc[i]['ARRIVAL_COUNTRY']) #str
        self.arrival_postal_code = str(df.iloc[i]['ARRIVAL_POST_CODE']) #str
        self.arrival_city = str(df.iloc[i]['ARRIVAL_CITY']) #str
        self.arrival_address = InputService.get_str_or_None(df, i, column='ARRIVAL_ADDRESS')  #str/NoneType

        self.shipment_mode = InputService.get_str_or_None(df, i, column='TRANSPORTATION_MODE') #str/NoneType
        self.shipment_conditions = InputService.get_str_or_None(df, i, column='DELIVERY_CONDITIONS') #str/NoneType


        self.check_departure_seller_vat_country_code = InputService.get_str_or_None(df, i, column='SELLER_DEPART_VAT_NUMBER_COUNTRY')
        self.check_departure_seller_vat_number = InputService.get_str_or_None(df, i, column='SELLER_DEPART_COUNTRY_VAT_NUMBER')

        self.check_arrival_seller_vat_country_code = InputService.get_str_or_None(df, i, column='SELLER_ARRIVAL_VAT_NUMBER_COUNTRY')
        self.check_arrival_seller_vat_number = InputService.get_str_or_None(df, i, column='SELLER_ARRIVAL_COUNTRY_VAT_NUMBER')

        self.check_seller_vat_country_code = InputService.get_str_or_None(df, i, column='TRANSACTION_SELLER_VAT_NUMBER_COUNTRY')
        self.check_seller_vat_number = InputService.get_str_or_None(df, i, column='TRANSACTION_SELLER_VAT_NUMBER')


        self.check_tax_calculation_imputation_country = InputService.get_str_or_None(df, i, column='VAT_CALCULATION_IMPUTATION_COUNTRY')
        self.check_tax_jurisdiction = InputService.get_str_or_None(df, i, column='TAXABLE_JURISDICTION')
        self.check_tax_jurisdiction_level = InputService.get_str_or_None(df, i, column='TAXABLE_JURISDICTION_LEVEL')

        self.invoice_number = InputService.get_str_or_None(df, i, column='VAT_INV_NUMBER')
        self.check_invoice_amount_vat = float(df.iloc[i]['VAT_INV_CONVERTED_AMT'])
        self.check_invoice_currency_code = InputService.get_str_or_None(df, i, column='VAT_INV_CURRENCY_CODE')
        self.check_invoice_exchange_rate = float(df.iloc[i]['VAT_INV_EXCHANGE_RATE']) if not pd.isnull(df.iloc[i]['VAT_INV_EXCHANGE_RATE']) else None
        self.check_invoice_exchange_rate_date = InputService.get_date_or_None(df, i, column='VAT_INV_EXCHANGE_RATE_DATE')
        self.invoice_url = InputService.get_str_or_None(df, i, column='INVOICE_URL')


        self.check_export = InputService.get_str_or_None(df, i, column='EXPORT_OUTSIDE_EU')  #str #-->transaction

        self.customer_name = InputService.get_str_or_None(df, i, column='BUYER_NAME')
        self.customer_vat_number = InputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER')
        self.customer_vat_number_country_code = InputService.get_str_or_None(df, i, column='BUYER_VAT_NUMBER_COUNTRY')

        self.supplier_vat_number = InputService.get_str_or_None(df, i, column='SUPPLIER_VAT_NUMBER') # #NoneType/str object #-->transaction
        self.supplier_name = InputService.get_str_or_None(df, i, column='SUPPLIER_NAME') #NoneType/str object #-->transaction



















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
