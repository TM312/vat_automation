from typing import List
from datetime import date, datetime
import pandas as pd

from werkzeug.exceptions import UnprocessableEntity

from app.namespaces.utils.service import InputService
from app.namespaces.exchange_rate.service import ExchangeRateService

var_config = dict(
    TI_AMZ_2020=AMZ2020,
    TI_AMZ_2021=AMZ2021
)

class AMZ2020:
    account_given_id = 'UNIQUE_ACCOUNT_IDENTIFIER'
    channel_code = 'SALES_CHANNEL'
    given_id = 'TRANSACTION_EVENT_ID'
    activity_id = 'ACTIVITY_TRANSACTION_ID'
    item_sku = 'SELLER_SKU'
    item_name = 'ITEM_DESCRIPTION'
    item_asin = 'ASIN'
    shipment_date = 'TRANSACTION_DEPART_DATE'
    arrival_date = 'TRANSACTION_ARRIVAL_DATE'
    complete_date = 'TRANSACTION_COMPLETE_DATE'
    public_activity_period = 'ACTIVITY_PERIOD'
    marketplace = 'MARKETPLACE'
    transaction_type_public_code = 'TRANSACTION_TYPE
    tax_calculation_date = 'TAX_CALCULATION_DATE'
    item_manufacture_country = 'ITEM_MANUFACTURE_COUNTRY'
    item_quantity = 'QTY'
    item_weight_kg = vc.item_weight_kg
    item_weight_kg_total = 'TOTAL_ACTIVITY_WEIGHT'
    unit_cost_price_net = 'COST_PRICE_OF_ITEMS'

    item_price_discount_net = 'PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL'

    item_price_discount_vat = 'PROMO_PRICE_OF_ITEMS_VAT_AMT'
    item_price_discount_gross = 'PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL'

    item_price_net = 'PRICE_OF_ITEMS_AMT_VAT_EXCL'
    item_price_vat = 'PRICE_OF_ITEMS_VAT_AMT'
    item_price_gross = 'PRICE_OF_ITEMS_AMT_VAT_INCL'

    item_price_total_net = 'TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL'
    item_price_total_vat = 'TOTAL_PRICE_OF_ITEMS_VAT_AMT'
    item_price_total_gross = 'TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL'

    item_price_vat_rate = 'PRICE_OF_ITEMS_VAT_RATE_PERCENT'

    shipment_price_discount_net = 'PROMO_SHIP_CHARGE_AMT_VAT_EXCL'
    shipment_price_discount_vat = 'PROMO_SHIP_CHARGE_VAT_AMT'
    shipment_price_discount_gross = 'PROMO_SHIP_CHARGE_AMT_VAT_INCL'

    shipment_price_net = 'SHIP_CHARGE_AMT_VAT_EXCL'
    shipment_price_vat = 'SHIP_CHARGE_VAT_AMT'
    shipment_price_gross = 'SHIP_CHARGE_AMT_VAT_INCL'

    shipment_price_total_net = 'TOTAL_SHIP_CHARGE_AMT_VAT_EXCL'
    shipment_price_total_vat = 'TOTAL_SHIP_CHARGE_VAT_AMT'
    shipment_price_total_gross = 'TOTAL_SHIP_CHARGE_AMT_VAT_INCL'

    shipment_price_vat_rate = 'SHIP_CHARGE_VAT_RATE_PERCENT'

    sale_total_value_net = 'TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL'
    sale_total_value_vat = 'TOTAL_ACTIVITY_VALUE_VAT_AMT'
    sale_total_value_gross = 'TOTAL_ACTIVITY_VALUE_AMT_VAT_INCL'

    gift_wrap_price_discount_net = 'PROMO_GIFT_WRAP_AMT_VAT_EXCL'
    gift_wrap_price_discount_vat = 'PROMO_GIFT_WRAP_VAT_AMT'
    gift_wrap_price_discount_gross = 'PROMO_GIFT_WRAP_AMT_VAT_INCL'

    gift_wrap_price_net = 'GIFT_WRAP_AMT_VAT_EXCL'
    gift_wrap_price_vat = 'GIFT_WRAP_VAT_AMT'
    gift_wrap_price_gross = 'GIFT_WRAP_AMT_VAT_INCL'

    gift_wrap_price_total_net = 'TOTAL_GIFT_WRAP_AMT_VAT_EXCL'
    gift_wrap_price_total_vat = 'TOTAL_GIFT_WRAP_VAT_AMT'
    gift_wrap_price_total_gross = 'TOTAL_GIFT_WRAP_AMT_VAT_INCL'

    gift_wrap_price_tax_rate ='GIFT_WRAP_VAT_RATE_PERCENT'

    currency_code = 'TRANSACTION_CURRENCY_CODE'

    item_given_tax_code_code = 'PRODUCT_TAX_CODE'

    departure_country_code = 'DEPARTURE_COUNTRY'
    departure_postal_code = 'DEPARTURE_POST_CODE'
    departure_city = 'DEPATURE_CITY'

    arrival_country_code = 'ARRIVAL_COUNTRY'
    arrival_postal_code = 'ARRIVAL_POST_CODE'
    arrival_city = 'ARRIVAL_CITY'
    arrival_address = 'ARRIVAL_ADDRESS'

    sale_departure_country_code = 'SALE_DEPART_COUNTRY'
    sale_arrival_country_code = 'SALE_ARRIVAL_COUNTRY'

    shipment_mode = 'TRANSPORTATION_MODE'
    shipment_conditions = 'DELIVERY_CONDITIONS'

    departure_seller_vat_country_code = 'SELLER_DEPART_VAT_NUMBER_COUNTRY'
    departure_seller_vat_number = 'SELLER_DEPART_COUNTRY_VAT_NUMBER'

    arrival_seller_vat_country_code = 'SELLER_ARRIVAL_VAT_NUMBER_COUNTRY'
    arrival_seller_vat_number = 'SELLER_ARRIVAL_COUNTRY_VAT_NUMBER'

    seller_vat_country_code = 'TRANSACTION_SELLER_VAT_NUMBER_COUNTRY'
    seller_vat_number = 'TRANSACTION_SELLER_VAT_NUMBER'

    tax_calculation_imputation_country = 'VAT_CALCULATION_IMPUTATION_COUNTRY'
    tax_jurisdiction = 'TAXABLE_JURISDICTION'
    tax_jurisdiction_level = 'TAXABLE_JURISDICTION_LEVEL'

    invoice_number = 'VAT_INV_NUMBER'
    invoice_amount_vat = 'VAT_INV_CONVERTED_AMT'
    invoice_currency_code = 'VAT_INV_CURRENCY_CODE'
    invoice_exchange_rate = 'VAT_INV_EXCHANGE_RATE'
    invoice_exchange_rate_date = 'VAT_INV_EXCHANGE_RATE_DATE'
    invoice_url = 'INVOICE_URL'

    export = 'EXPORT_OUTSIDE_EU'

    customer_name = 'BUYER_NAME'
    customer_vat_number = 'BUYER_VAT_NUMBER'
    customer_vat_number_country_code = 'BUYER_VAT_NUMBER_COUNTRY'

    supplier_vat_number = 'SUPPLIER_VAT_NUMBER'
    supplier_name = 'SUPPLIER_NAME'

    #unprovided vars
    item_brand_name = None

class AMZ2021(AMZ2020):
    pass





class AMZReader:

    @staticmethod
    def get_item_gross_prices(df: pd.DataFrame, target_currency_code: str, file_type: str) -> List[float, int]:
        vc = var_config[file_type]
        item_gross_prices = []
        for i in range(len(df.index)):
            sale_total_value_gross_raw = InputService.get_float_or_None(df, i, column=vc.item_price_gross)
            base_currency_code = InputService.get_str(df, i, column=vc.currency_code)
            if isinstance(sale_total_value_gross_raw, float) and isinstance(base_currency_code, str):
                item_quantity = InputService.get_float_or_None(df, i, column=vc.item_quantity) #always provided
                exchange_rate_date = InputService.get_date_or_None(df, i, column=vc.complete_date) #always provided

                #convert to target currency
                exchange_rate_rate = ExchangeRateService.get_by_base_target_date(base_currency_code, target_currency_code, exchange_rate_date).rate if base_currency_code != target_currency_code else 1
                sale_total_value_gross = sale_total_value_gross_raw * exchange_rate_rate

                item_gross_prices.append(sale_total_value_gross)

        return item_gross_prices


    @staticmethod
    def get_all_dates_in_df(df: pd.DataFrame, file_type: str) -> List[date]:
        vc = var_config[file_type]
        #!!! when expanding to other platforms should be tested for case if certain columns not existent
        dates_all = df[[vc.shipment_date, vc.arrival_date, vc.complete_date, vc.tax_calculation_date, vc.invoice_exchange_rate_date]].values.ravel('K')
        dates_raw = pd.unique(dates_all).tolist()
        #remove nan and transform to datetime.date object
        dates = [
            datetime.strptime(d, '%d-%m-%Y').date()
            for d in dates_raw
            if str(d) != 'nan'
            ]

        return dates


    @staticmethod
    def get_unique_vatin_numbers(df: pd.DataFrame, file_type: str) -> List[str]:
        vc = var_config[file_type]
        #!!! when expanding to other platforms should be tested for case if certain columns not existent
        column_values = df[[vc.departure_seller_vat_number, vc.arrival_seller_vat_number, vc.seller_vat_number]].values.ravel('K')

        # general/platform-independent proceeding
        #unique values
        unique_vatin_numbers_raw = pd.unique(column_values).tolist()
        # drop nan
        unique_vatin_numbers = [vatin_number for vatin_number in unique_vatin_numbers_raw if str(vatin_number) != 'nan']

        return unique_vatin_numbers


    @staticmethod
    def get_unique_accounts(df: pd.DataFrame, file_type: str) -> pd.DataFrame:
        vc = var_config[file_type]
        return df.drop_duplicates(subset=[vc.account_given_id, vc.channel_code])[[vc.account_given_id, vc.channel_code]]

    @staticmethod
    def get_unique_items(df: pd.DataFrame, file_type: str) -> pd.DataFrame:
        vc = var_config[file_type]
        return df.drop_duplicates(subset=[vc.item_asin])[[vc.item_sku, vc.item_asin, vc.item_name, vc.item_weight_kg, vc.item_given_tax_code_code]]



    @staticmethod
    def verify_transaction_order(df: pd.DataFrame, total: int, file_type: str) -> bool:
        vc = var_config[file_type]
        complete_date_top = InputService.get_date_or_None(df, 0, column=vc.complete_date)
        complete_date_bottom = InputService.get_date_or_None(df, total-1, column=vc.complete_date)

        return complete_date_top >= complete_date_bottom


    @staticmethod
    def get_account_vars(df_accounts: pd.DataFrame, i: int, file_type: str) -> List:
        vc = var_config[file_type]
        try:
            account_given_id = InputService.get_str(df_accounts, i, column=vc.account_given_id)
        except:
            raise UnprocessableEntity(vc.account_given_id)

        try:
            channel_code = InputService.get_str(df_accounts, i, column=vc.channel_code)
        except:
            raise UnprocessableEntity(vc.channel_code)

        return account_given_id, channel_code


    @staticmethod
    def get_item_vars(df_items: pd.DataFrame, i: int, file_type: str) -> List:
        vc = var_config[file_type]
        try:
            item_sku = InputService.get_str(df_items, i, column=vc.item_sku)
        except:
            raise UnprocessableEntity(vc.item_sku)

        try:
            item_name = InputService.get_str_or_None(df_items, i, column=vc.item_name)
        except:
            raise UnprocessableEntity(vc.item_name)

        try:
            item_asin = InputService.get_str_or_None(df_items, i, column=vc.item_asin)
        except:
            raise UnprocessableEntity(vc.item_asin)

        try:
            item_weight_kg = InputService.get_float_or_None(df_items, i, column=vc.item_weight_kg)
        except:
            raise UnprocessableEntity(vc.item_weight_kg)

        try:
            item_given_tax_code_code = InputService.get_str_or_None(df_items, i, column=vc.item_given_tax_code_code)
        except:
            raise UnprocessableEntity(vc.item_given_tax_code_code)

        return item_sku, item_name, item_asin, item_weight_kg, item_given_tax_code_code


    @staticmethod
    def get_df_vars(df: pd.DataFrame, i: int, current: int, object_type: str, file_type: str) -> List:
        vc = var_config[file_type]

        try:
            account_given_id = InputService.get_str(df, i, column=vc.account_given_id)
        except:
            raise UnprocessableEntity(vc.account_given_id)

        try:
            channel_code = InputService.get_str(df, i, column=vc.channel_code)
        except:
            raise UnprocessableEntity(vc.channel_code)

        try:
            given_id = InputService.get_str(df, i, column=vc.given_id)
        except:
            raise UnprocessableEntity(vc.given_id)

        try:
            activity_id = InputService.get_str(df, i, column=vc.activity_id)
        except:
            raise UnprocessableEntity(vc.activity_id)

        try:
            item_sku = InputService.get_str(df, i, column=vc.item_sku)
        except:
            raise UnprocessableEntity(vc.item_sku)

        try:
            item_name = InputService.get_str_or_None(df, i, column=vc.item_name)
        except:
            raise UnprocessableEntity(vc.item_name)

        try:
            item_asin = InputService.get_str_or_None(df, i, column=vc.item_asin)
        except:
            raise UnprocessableEntity(vc.item_asin)

        try:
            shipment_date = InputService.get_date_or_None(
                df, i, column=vc.shipment_date)
        except:
            raise UnprocessableEntity(vc.shipment_date)

        try:
            arrival_date = InputService.get_date_or_None(
                df, i, column=vc.arrival_date)
        except:
            raise UnprocessableEntity(vc.arrival_date)

        try:
            complete_date = InputService.get_date_or_None(
                df, i, column=vc.complete_date)
        except:
            raise UnprocessableEntity(vc.complete_date)

        try:
            public_activity_period = InputService.get_str(
                df, i, column=vc.public_activity_period)
        except:
            raise UnprocessableEntity(vc.public_activity_period)
        try:
            marketplace = InputService.get_str_or_None(
                df, i, column=vc.marketplace)
        except:
            raise UnprocessableEntity(vc.marketplace)
        try:
            transaction_type_public_code = InputService.get_str_or_None(
                df, i, column=vc.transaction_type_public_code)
        except:
            raise UnprocessableEntity(vc.transaction_type_public_code)

        try:
            tax_calculation_date = InputService.get_date_or_None(
                df, i, column=vc.tax_calculation_date)
        except:
            raise UnprocessableEntity(vc.tax_calculation_date)

        try:
            item_manufacture_country = InputService.get_str_or_None(
                df, i, column=vc.item_manufacture_country)
        except:
            raise UnprocessableEntity(vc.item_manufacture_country)
        try:
            item_quantity = int(df.iloc[i][vc.item_quantity])
        except:
            raise UnprocessableEntity(vc.item_quantity)

        try:
            item_weight_kg = InputService.get_float_or_None(df, i, column=vc.item_weight_kg)
        except:
            raise UnprocessableEntity(vc.item_weight_kg)
        try:
            item_weight_kg_total = InputService.get_float_or_None(df, i, column=vc.item_weight_kg_total)
        except:
            raise UnprocessableEntity(vc.item_weight_kg_total)

        try:
            unit_cost_price_net = InputService.get_float_or_None(df, i, column=vc.unit_cost_price_net)
        except:
            raise UnprocessableEntity(vc.unit_cost_price_net)

        try:
            item_price_discount_net = InputService.get_float_or_None(df, i, column=vc.item_price_discount_net)
        except:
            raise UnprocessableEntity(vc.item_price_discount_net)
        try:
            item_price_discount_vat = InputService.get_float_or_None(df, i, column=vc.item_price_discount_vat)
        except:
            raise UnprocessableEntity(vc.item_price_discount_vat)
        try:
            item_price_discount_gross = InputService.get_float_or_None(df, i, column=vc.item_price_discount_gross)
        except:
            raise UnprocessableEntity(vc.item_price_discount_gross)

        try:
            item_price_net = InputService.get_float_or_None(df, i, column=vc.item_price_net)
        except:
            raise UnprocessableEntity(vc.item_price_net)
        try:
            item_price_vat = InputService.get_float_or_None(df, i, column=vc.item_price_vat)
        except:
            raise UnprocessableEntity(vc.item_price_vat)
        try:
            item_price_gross = InputService.get_float_or_None(df, i, column=vc.item_price_gross)
        except:
            raise UnprocessableEntity(vc.item_price_gross)

        try:
            item_price_total_net = InputService.get_float_or_None(df, i, column=vc.item_price_total_net)
        except:
            raise UnprocessableEntity(vc.item_price_total_net)
        try:
            item_price_total_vat = InputService.get_float_or_None( df, i, column=vc.item_price_total_vat)
        except:
            raise UnprocessableEntity(vc.item_price_total_vat)
        try:
            item_price_total_gross = InputService.get_float_or_None( df, i, column=vc.item_price_total_gross)
        except:
            raise UnprocessableEntity(vc.item_price_total_gross)

        try:
            item_price_vat_rate = InputService.get_float_or_None(df, i, column=vc.item_price_vat_rate)
        except:
            raise UnprocessableEntity(vc.item_price_vat_rate)

        try:
            shipment_price_discount_net = InputService.get_float_or_None(
                df, i, column=vc.shipment_price_discount_net)
        except:
            raise UnprocessableEntity(vc.shipment_price_discount_net)
        try:
            shipment_price_discount_vat = InputService.get_float_or_None(
                df, i, column=vc.shipment_price_discount_vat)
        except:
            raise UnprocessableEntity(vc.shipment_price_discount_vat)
        try:
            shipment_price_discount_gross = InputService.get_float_or_None(
                df, i, column=vc.shipment_price_discount_gross)
        except:
            raise UnprocessableEntity(vc.shipment_price_discount_gross)

        try:
            shipment_price_net = InputService.get_float_or_None(
                df, i, column=vc.shipment_price_net)
        except:
            raise UnprocessableEntity(vc.shipment_price_net)
        try:
            shipment_price_vat = InputService.get_float_or_None(
                df, i, column=vc.shipment_price_vat)
        except:
            raise UnprocessableEntity(vc.shipment_price_vat)
        try:
            shipment_price_gross = InputService.get_float_or_None(
                df, i, column=vc.shipment_price_gross)
        except:
            raise UnprocessableEntity(vc.shipment_price_gross)

        try:
            shipment_price_total_net = InputService.get_float_or_None(
                df, i, column=vc.shipment_price_total_net)
        except:
            raise UnprocessableEntity(vc.shipment_price_total_net)
        try:
            shipment_price_total_vat = InputService.get_float_or_None(
                df, i, column=vc.shipment_price_total_vat)
        except:
            raise UnprocessableEntity(vc.shipment_price_total_vat)
        try:
            shipment_price_total_gross = InputService.get_float_or_None(
                df, i, column=vc.shipment_price_total_gross)
        except:
            raise UnprocessableEntity(vc.shipment_price_total_gross)

        try:
            shipment_price_vat_rate = InputService.get_float_or_None(
                df, i, column=vc.shipment_price_vat_rate)
        except:
            raise UnprocessableEntity(vc.shipment_price_vat_rate)

        try:
            sale_total_value_net = InputService.get_float_or_None(
                df, i, column=vc.sale_total_value_net)
        except:
            raise UnprocessableEntity(vc.sale_total_value_net)
        try:
            sale_total_value_vat = InputService.get_float_or_None(
                df, i, column=vc.sale_total_value_vat)
        except:
            raise UnprocessableEntity(vc.sale_total_value_vat)
        try:
            sale_total_value_gross = InputService.get_float_or_None(
                df, i, column=vc.sale_total_value_gross)
        except:
            raise UnprocessableEntity(vc.sale_total_value_gross)

        try:
            gift_wrap_price_discount_net = InputService.get_float_or_None(
                df, i, column=vc.gift_wrap_price_discount_net)
        except:
            raise UnprocessableEntity(vc.gift_wrap_price_discount_net)
        try:
            gift_wrap_price_discount_vat = InputService.get_float_or_None(
                df, i, column=vc.gift_wrap_price_discount_vat)
        except:
            raise UnprocessableEntity(vc.gift_wrap_price_discount_vat)
        try:
            gift_wrap_price_discount_gross = InputService.get_float_or_None(
                df, i, column=vc.gift_wrap_price_discount_gross)
        except:
            raise UnprocessableEntity(vc.gift_wrap_price_discount_gross)

        try:
            gift_wrap_price_net = InputService.get_float_or_None(
                df, i, column=vc.gift_wrap_price_net)
        except:
            raise UnprocessableEntity(vc.gift_wrap_price_net)
        try:
            gift_wrap_price_vat = InputService.get_float_or_None(
                df, i, column=vc.gift_wrap_price_vat)
        except:
            raise UnprocessableEntity(vc.gift_wrap_price_vat)
        try:
            gift_wrap_price_gross = InputService.get_float_or_None(
                df, i, column=vc.gift_wrap_price_gross)
        except:
            raise UnprocessableEntity(vc.gift_wrap_price_gross)

        try:
            gift_wrap_price_total_net = InputService.get_float_or_None(
                df, i, column=vc.gift_wrap_price_total_net)
        except:
            raise UnprocessableEntity(vc.gift_wrap_price_total_net)
        try:
            gift_wrap_price_total_vat = InputService.get_float_or_None(
                df, i, column=vc.gift_wrap_price_total_vat)
        except:
            raise UnprocessableEntity(vc.gift_wrap_price_total_vat)
        try:
            gift_wrap_price_total_gross = InputService.get_float_or_None(
                df, i, column=vc.gift_wrap_price_total_gross)
        except:
            raise UnprocessableEntity(vc.gift_wrap_price_total_gross)

        try:
            gift_wrap_price_tax_rate = InputService.get_float_or_None(
                df, i, column=vc.gift_wrap_price_tax_rate)
        except:
            raise UnprocessableEntity(vc.gift_wrap_price_tax_rate)

        try:
            currency_code = InputService.get_str_or_None(df, i, column=vc.currency_code)
        except:
            raise UnprocessableEntity(vc.currency_code)

        try:
            item_given_tax_code_code = InputService.get_str_or_None(
                df, i, column=vc.item_given_tax_code_code)
        except:
            raise UnprocessableEntity(vc.item_given_tax_code_code)

        try:
            departure_country_code = InputService.get_str_or_None(
                df, i, column=vc.departure_country_code)
        except:
            raise UnprocessableEntity(vc.departure_country_code)
        try:
            departure_postal_code = InputService.get_single_str_compact(
                df, i, column=vc.departure_postal_code)
        except:
            raise UnprocessableEntity(vc.departure_postal_code)
        try:
            departure_city = InputService.get_str_or_None(
                df, i, column=vc.departure_city)
        except:
            raise UnprocessableEntity(vc.departure_city)

        try:
            arrival_country_code = InputService.get_str_or_None(
                df, i, column=vc.arrival_country_code)
        except:
            raise UnprocessableEntity(vc.arrival_country_code)
        try:
            arrival_postal_code = InputService.get_single_str_compact(
                df, i, column=vc.arrival_postal_code)
        except:
            raise UnprocessableEntity(vc.arrival_postal_code)
        try:
            arrival_city = InputService.get_str_or_None(
                df, i, column=vc.arrival_city)
        except:
            raise UnprocessableEntity(vc.arrival_city)
        try:
            arrival_address = InputService.get_str_or_None(
                df, i, column=vc.arrival_address)
        except:
            raise UnprocessableEntity(vc.arrival_address)

        try:
            sale_departure_country_code = InputService.get_str_or_None(
                df, i, column=vc.sale_departure_country_code)
        except:
            raise UnprocessableEntity(vc.sale_departure_country_code)
        try:
            sale_arrival_country_code = InputService.get_str_or_None(
                df, i, column=vc.sale_arrival_country_code)
        except:
            raise UnprocessableEntity(vc.sale_arrival_country_code)

        try:
            shipment_mode = InputService.get_str_or_None(
                df, i, column=vc.shipment_mode)
        except:
            raise UnprocessableEntity(vc.shipment_mode)
        try:
            shipment_conditions = InputService.get_str_or_None(
                df, i, column=vc.shipment_conditions)
        except:
            raise UnprocessableEntity(vc.shipment_conditions)

        try:
            departure_seller_vat_country_code = InputService.get_str_or_None(
                df, i, column=vc.departure_seller_vat_country_code)
        except:
            raise UnprocessableEntity(vc.departure_seller_vat_country_code)
        try:
            departure_seller_vat_number = InputService.get_str_or_None(
                df, i, column=vc.departure_seller_vat_number)
        except:
            raise UnprocessableEntity(vc.departure_seller_vat_number)

        try:
            arrival_seller_vat_country_code = InputService.get_str_or_None(
                df, i, column=vc.arrival_seller_vat_country_code)
        except:
            raise UnprocessableEntity(vc.arrival_seller_vat_country_code)
        try:
            arrival_seller_vat_number = InputService.get_str_or_None(
                df, i, column=vc.arrival_seller_vat_number)
        except:
            raise UnprocessableEntity(vc.arrival_seller_vat_number)

        try:
            seller_vat_country_code = InputService.get_str_or_None(
                df, i, column=vc.seller_vat_country_code)
        except:
            raise UnprocessableEntity(vc.seller_vat_country_code)
        try:
            seller_vat_number = InputService.get_str_or_None(
                df, i, column=vc.seller_vat_number)
        except:
            raise UnprocessableEntity(vc.seller_vat_number)

        try:
            tax_calculation_imputation_country = InputService.get_str_or_None(
                df, i, column=vc.tax_calculation_imputation_country)
        except:
            raise UnprocessableEntity(vc.tax_calculation_imputation_country)
        try:
            tax_jurisdiction = InputService.get_str_or_None(
                df, i, column=vc.tax_jurisdiction)
        except:
            raise UnprocessableEntity(vc.tax_jurisdiction)
        try:
            tax_jurisdiction_level = InputService.get_str_or_None(
                df, i, column=vc.tax_jurisdiction)
        except:
            raise UnprocessableEntity(vc.tax_jurisdiction)

        try:
            invoice_number = InputService.get_str_or_None(
                df, i, column=vc.invoice_number)
        except:
            raise UnprocessableEntity(vc.invoice_number)
        try:
            invoice_amount_vat = InputService.get_float_or_None(
                df, i, column=vc.invoice_amount_vat)
        except:
            raise UnprocessableEntity(vc.invoice_amount_vat)
        try:
            invoice_currency_code = InputService.get_str_or_None(
                df, i, column=vc.invoice_currency_code)
        except:
            raise UnprocessableEntity(vc.invoice_currency_code)
        try:
            invoice_exchange_rate = InputService.get_float_or_None(
                df, i, column=vc.invoice_exchange_rate)
        except:
            raise UnprocessableEntity(vc.invoice_exchange_rate)
        try:
            invoice_exchange_rate_date = InputService.get_date_or_None(
                df, i, column=vc.invoice_exchange_rate_date)
        except:
            raise UnprocessableEntity(vc.invoice_exchange_rate_date)
        try:
            invoice_url = InputService.get_str_or_None(
                df, i, column=vc.invoice_url)
        except:
            raise UnprocessableEntity(vc.invoice_url)

        try:
            export = InputService.get_bool(
                df, i, column=vc.export, value_true='YES')
        except:
            raise UnprocessableEntity(vc.export)

        try:
            customer_name = InputService.get_str_or_None(
                df, i, column=vc.customer_name)
        except:
            raise UnprocessableEntity(vc.customer_name)
        try:
            customer_vat_number = InputService.get_str_or_None(
                df, i, column=vc.customer_vat_number)
        except:
            raise UnprocessableEntity(vc.customer_vat_number)
        try:
            customer_vat_number_country_code = InputService.get_str_or_None(
                df, i, column=vc.customer_vat_number_country_code)
        except:
            raise UnprocessableEntity(vc.customer_vat_number_country_code)

        try:
            supplier_vat_number = InputService.get_str_or_None(
                df, i, column=vc.supplier_vat_number)
        except:
            raise UnprocessableEntity(vc.supplier_vat_number)
        try:
            supplier_name = InputService.get_str_or_None(
                df, i, column=vc.supplier_name)
        except:
            raise UnprocessableEntity(vc.supplier_name)

        item_brand_name = vc.item_brand_name

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



####BACKUP

#  @staticmethod
#     def get_df_vars_AMZ2020(df: pd.DataFrame, i: int, current: int, object_type: str) -> List:

#         try:
#             account_given_id = InputService.get_str(
#                 df, i, column='UNIQUE_ACCOUNT_IDENTIFIER')
#         except:
#             raise UnprocessableEntity('UNIQUE_ACCOUNT_IDENTIFIER')

#         try:
#             channel_code = InputService.get_str(df, i, column='SALES_CHANNEL')
#         except:
#             raise UnprocessableEntity('SALES_CHANNEL')

#         try:
#             given_id = InputService.get_str(
#                 df, i, column='TRANSACTION_EVENT_ID')
#         except:
#             raise UnprocessableEntity('TRANSACTION_EVENT_ID')

#         try:
#             activity_id = InputService.get_str(
#                 df, i, column='ACTIVITY_TRANSACTION_ID')
#         except:
#             raise UnprocessableEntity('ACTIVITY_TRANSACTION_ID')

#         try:
#             item_sku = InputService.get_str(df, i, column='SELLER_SKU')
#         except:
#             raise UnprocessableEntity('SELLER_SKU')

#         try:
#             item_name = InputService.get_str_or_None(
#                 df, i, column='ITEM_DESCRIPTION')
#         except:
#             raise UnprocessableEntity('ITEM_DESCRIPTION')

#         try:
#             item_asin = InputService.get_str_or_None(df, i, column='ASIN')
#         except:
#             raise UnprocessableEntity('ASIN')

#         try:
#             shipment_date = InputService.get_date_or_None(
#                 df, i, column='TRANSACTION_DEPART_DATE')
#         except:
#             raise UnprocessableEntity('TRANSACTION_DEPART_DATE')

#         try:
#             arrival_date = InputService.get_date_or_None(
#                 df, i, column='TRANSACTION_ARRIVAL_DATE')
#         except:
#             raise UnprocessableEntity('TRANSACTION_ARRIVAL_DATE')

#         try:
#             complete_date = InputService.get_date_or_None(
#                 df, i, column='TRANSACTION_COMPLETE_DATE')
#         except:
#             raise UnprocessableEntity('TRANSACTION_COMPLETE_DATE')

#         try:
#             public_activity_period = InputService.get_str(
#                 df, i, column='ACTIVITY_PERIOD')
#         except:
#             raise UnprocessableEntity('ACTIVITY_PERIOD')
#         try:
#             marketplace = InputService.get_str_or_None(
#                 df, i, column='MARKETPLACE')
#         except:
#             raise UnprocessableEntity('MARKETPLACE')
#         try:
#             transaction_type_public_code = InputService.get_str_or_None(
#                 df, i, column='TRANSACTION_TYPE')
#         except:
#             raise UnprocessableEntity('TRANSACTION_TYPE')

#         try:
#             tax_calculation_date = InputService.get_date_or_None(
#                 df, i, column='TAX_CALCULATION_DATE')
#         except:
#             raise UnprocessableEntity('TAX_CALCULATION_DATE')

#         try:
#             item_manufacture_country = InputService.get_str_or_None(
#                 df, i, column='ITEM_MANUFACTURE_COUNTRY')
#         except:
#             raise UnprocessableEntity('ITEM_MANUFACTURE_COUNTRY')
#         try:
#             item_quantity = int(df.iloc[i]['QTY'])
#         except:
#             raise UnprocessableEntity('QTY')

#         try:
#             item_weight_kg = InputService.get_float_or_None(
#                 df, i, column='ITEM_WEIGHT')
#         except:
#             raise UnprocessableEntity('ITEM_WEIGHT')
#         try:
#             item_weight_kg_total = InputService.get_float_or_None(
#                 df, i, column='TOTAL_ACTIVITY_WEIGHT')
#         except:
#             raise UnprocessableEntity('TOTAL_ACTIVITY_WEIGHT')

#         try:
#             unit_cost_price_net = InputService.get_float_or_None(
#                 df, i, column='COST_PRICE_OF_ITEMS')
#         except:
#             raise UnprocessableEntity('COST_PRICE_OF_ITEMS')

#         try:
#             item_price_discount_net = InputService.get_float_or_None(
#                 df, i, column='PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL')
#         except:
#             raise UnprocessableEntity('PROMO_PRICE_OF_ITEMS_AMT_VAT_EXCL')
#         try:
#             item_price_discount_vat = InputService.get_float_or_None(
#                 df, i, column='PROMO_PRICE_OF_ITEMS_VAT_AMT')
#         except:
#             raise UnprocessableEntity('PROMO_PRICE_OF_ITEMS_VAT_AMT')
#         try:
#             item_price_discount_gross = InputService.get_float_or_None(
#                 df, i, column='PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL')
#         except:
#             raise UnprocessableEntity('PROMO_PRICE_OF_ITEMS_AMT_VAT_INCL')

#         try:
#             item_price_net = InputService.get_float_or_None(
#                 df, i, column='PRICE_OF_ITEMS_AMT_VAT_EXCL')
#         except:
#             raise UnprocessableEntity('PRICE_OF_ITEMS_AMT_VAT_EXCL')
#         try:
#             item_price_vat = InputService.get_float_or_None(
#                 df, i, column='PRICE_OF_ITEMS_VAT_AMT')
#         except:
#             raise UnprocessableEntity('PRICE_OF_ITEMS_VAT_AMT')
#         try:
#             item_price_gross = InputService.get_float_or_None(
#                 df, i, column='PRICE_OF_ITEMS_AMT_VAT_INCL')
#         except:
#             raise UnprocessableEntity('PRICE_OF_ITEMS_AMT_VAT_INCL')

#         try:
#             item_price_total_net = InputService.get_float_or_None(
#                 df, i, column='TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL')
#         except:
#             raise UnprocessableEntity('TOTAL_PRICE_OF_ITEMS_AMT_VAT_EXCL')
#         try:
#             item_price_total_vat = InputService.get_float_or_None(
#                 df, i, column='TOTAL_PRICE_OF_ITEMS_VAT_AMT')
#         except:
#             raise UnprocessableEntity('TOTAL_PRICE_OF_ITEMS_VAT_AMT')
#         try:
#             item_price_total_gross = InputService.get_float_or_None(
#                 df, i, column='TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL')
#         except:
#             raise UnprocessableEntity('TOTAL_PRICE_OF_ITEMS_AMT_VAT_INCL')

#         try:
#             item_price_vat_rate = InputService.get_float_or_None(
#                 df, i, column='PRICE_OF_ITEMS_VAT_RATE_PERCENT')
#         except:
#             raise UnprocessableEntity('PRICE_OF_ITEMS_VAT_RATE_PERCENT')

#         try:
#             shipment_price_discount_net = InputService.get_float_or_None(
#                 df, i, column='PROMO_SHIP_CHARGE_AMT_VAT_EXCL')
#         except:
#             raise UnprocessableEntity('PROMO_SHIP_CHARGE_AMT_VAT_EXCL')
#         try:
#             shipment_price_discount_vat = InputService.get_float_or_None(
#                 df, i, column='PROMO_SHIP_CHARGE_VAT_AMT')
#         except:
#             raise UnprocessableEntity('PROMO_SHIP_CHARGE_VAT_AMT')
#         try:
#             shipment_price_discount_gross = InputService.get_float_or_None(
#                 df, i, column='PROMO_SHIP_CHARGE_AMT_VAT_INCL')
#         except:
#             raise UnprocessableEntity('PROMO_SHIP_CHARGE_AMT_VAT_INCL')

#         try:
#             shipment_price_net = InputService.get_float_or_None(
#                 df, i, column='SHIP_CHARGE_AMT_VAT_EXCL')
#         except:
#             raise UnprocessableEntity('SHIP_CHARGE_AMT_VAT_EXCL')
#         try:
#             shipment_price_vat = InputService.get_float_or_None(
#                 df, i, column='SHIP_CHARGE_VAT_AMT')
#         except:
#             raise UnprocessableEntity('SHIP_CHARGE_VAT_AMT')
#         try:
#             shipment_price_gross = InputService.get_float_or_None(
#                 df, i, column='SHIP_CHARGE_AMT_VAT_INCL')
#         except:
#             raise UnprocessableEntity('SHIP_CHARGE_AMT_VAT_INCL')

#         try:
#             shipment_price_total_net = InputService.get_float_or_None(
#                 df, i, column='TOTAL_SHIP_CHARGE_AMT_VAT_EXCL')
#         except:
#             raise UnprocessableEntity('TOTAL_SHIP_CHARGE_AMT_VAT_EXCL')
#         try:
#             shipment_price_total_vat = InputService.get_float_or_None(
#                 df, i, column='TOTAL_SHIP_CHARGE_VAT_AMT')
#         except:
#             raise UnprocessableEntity('TOTAL_SHIP_CHARGE_VAT_AMT')
#         try:
#             shipment_price_total_gross = InputService.get_float_or_None(
#                 df, i, column='TOTAL_SHIP_CHARGE_AMT_VAT_INCL')
#         except:
#             raise UnprocessableEntity('TOTAL_SHIP_CHARGE_AMT_VAT_INCL')

#         try:
#             shipment_price_vat_rate = InputService.get_float_or_None(
#                 df, i, column='SHIP_CHARGE_VAT_RATE_PERCENT')
#         except:
#             raise UnprocessableEntity('SHIP_CHARGE_VAT_RATE_PERCENT')

#         try:
#             sale_total_value_net = InputService.get_float_or_None(
#                 df, i, column='TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL')
#         except:
#             raise UnprocessableEntity('TOTAL_ACTIVITY_VALUE_AMT_VAT_EXCL')
#         try:
#             sale_total_value_vat = InputService.get_float_or_None(
#                 df, i, column='TOTAL_ACTIVITY_VALUE_VAT_AMT')
#         except:
#             raise UnprocessableEntity('TOTAL_ACTIVITY_VALUE_VAT_AMT')
#         try:
#             sale_total_value_gross = InputService.get_float_or_None(
#                 df, i, column='TOTAL_ACTIVITY_VALUE_AMT_VAT_INCL')
#         except:
#             raise UnprocessableEntity('TOTAL_ACTIVITY_VALUE_AMT_VAT_INCL')

#         try:
#             gift_wrap_price_discount_net = InputService.get_float_or_None(
#                 df, i, column='PROMO_GIFT_WRAP_AMT_VAT_EXCL')
#         except:
#             raise UnprocessableEntity('PROMO_GIFT_WRAP_AMT_VAT_EXCL')
#         try:
#             gift_wrap_price_discount_vat = InputService.get_float_or_None(
#                 df, i, column='PROMO_GIFT_WRAP_VAT_AMT')
#         except:
#             raise UnprocessableEntity('PROMO_GIFT_WRAP_VAT_AMT')
#         try:
#             gift_wrap_price_discount_gross = InputService.get_float_or_None(
#                 df, i, column='PROMO_GIFT_WRAP_AMT_VAT_INCL')
#         except:
#             raise UnprocessableEntity('PROMO_GIFT_WRAP_AMT_VAT_INCL')

#         try:
#             gift_wrap_price_net = InputService.get_float_or_None(
#                 df, i, column='GIFT_WRAP_AMT_VAT_EXCL')
#         except:
#             raise UnprocessableEntity('GIFT_WRAP_AMT_VAT_EXCL')
#         try:
#             gift_wrap_price_vat = InputService.get_float_or_None(
#                 df, i, column='GIFT_WRAP_VAT_AMT')
#         except:
#             raise UnprocessableEntity('GIFT_WRAP_VAT_AMT')
#         try:
#             gift_wrap_price_gross = InputService.get_float_or_None(
#                 df, i, column='GIFT_WRAP_AMT_VAT_INCL')
#         except:
#             raise UnprocessableEntity('GIFT_WRAP_AMT_VAT_INCL')

#         try:
#             gift_wrap_price_total_net = InputService.get_float_or_None(
#                 df, i, column='TOTAL_GIFT_WRAP_AMT_VAT_EXCL')
#         except:
#             raise UnprocessableEntity('TOTAL_GIFT_WRAP_AMT_VAT_EXCL')
#         try:
#             gift_wrap_price_total_vat = InputService.get_float_or_None(
#                 df, i, column='TOTAL_GIFT_WRAP_VAT_AMT')
#         except:
#             raise UnprocessableEntity('TOTAL_GIFT_WRAP_VAT_AMT')
#         try:
#             gift_wrap_price_total_gross = InputService.get_float_or_None(
#                 df, i, column='TOTAL_GIFT_WRAP_AMT_VAT_INCL')
#         except:
#             raise UnprocessableEntity('TOTAL_GIFT_WRAP_AMT_VAT_INCL')

#         try:
#             gift_wrap_price_tax_rate = InputService.get_float_or_None(
#                 df, i, column='GIFT_WRAP_VAT_RATE_PERCENT')
#         except:
#             raise UnprocessableEntity('GIFT_WRAP_VAT_RATE_PERCENT')

#         try:
#             currency_code = InputService.get_str_or_None(df, i, column=var_config[file_type].currency_code)
#         except:
#             raise UnprocessableEntity(var_config[file_type].currency_code)

#         try:
#             item_given_tax_code_code = InputService.get_str_or_None(
#                 df, i, column='PRODUCT_TAX_CODE')
#         except:
#             raise UnprocessableEntity('PRODUCT_TAX_CODE')

#         try:
#             departure_country_code = InputService.get_str_or_None(
#                 df, i, column='DEPARTURE_COUNTRY')
#         except:
#             raise UnprocessableEntity('DEPARTURE_COUNTRY')
#         try:
#             departure_postal_code = InputService.get_single_str_compact(
#                 df, i, column='DEPARTURE_POST_CODE')
#         except:
#             raise UnprocessableEntity('DEPARTURE_POST_CODE')
#         try:
#             departure_city = InputService.get_str_or_None(
#                 df, i, column='DEPATURE_CITY')
#         except:
#             raise UnprocessableEntity('DEPATURE_CITY')

#         try:
#             arrival_country_code = InputService.get_str_or_None(
#                 df, i, column='ARRIVAL_COUNTRY')
#         except:
#             raise UnprocessableEntity('ARRIVAL_COUNTRY')
#         try:
#             arrival_postal_code = InputService.get_single_str_compact(
#                 df, i, column='ARRIVAL_POST_CODE')
#         except:
#             raise UnprocessableEntity('ARRIVAL_POST_CODE')
#         try:
#             arrival_city = InputService.get_str_or_None(
#                 df, i, column='ARRIVAL_CITY')
#         except:
#             raise UnprocessableEntity('ARRIVAL_CITY')
#         try:
#             arrival_address = InputService.get_str_or_None(
#                 df, i, column='ARRIVAL_ADDRESS')
#         except:
#             raise UnprocessableEntity('ARRIVAL_ADDRESS')

#         try:
#             sale_departure_country_code = InputService.get_str_or_None(
#                 df, i, column='SALE_DEPART_COUNTRY')
#         except:
#             raise UnprocessableEntity('SALE_DEPART_COUNTRY')
#         try:
#             sale_arrival_country_code = InputService.get_str_or_None(
#                 df, i, column='SALE_ARRIVAL_COUNTRY')
#         except:
#             raise UnprocessableEntity('SALE_ARRIVAL_COUNTRY')

#         try:
#             shipment_mode = InputService.get_str_or_None(
#                 df, i, column='TRANSPORTATION_MODE')
#         except:
#             raise UnprocessableEntity('TRANSPORTATION_MODE')
#         try:
#             shipment_conditions = InputService.get_str_or_None(
#                 df, i, column='DELIVERY_CONDITIONS')
#         except:
#             raise UnprocessableEntity('DELIVERY_CONDITIONS')

#         try:
#             departure_seller_vat_country_code = InputService.get_str_or_None(
#                 df, i, column='SELLER_DEPART_VAT_NUMBER_COUNTRY')
#         except:
#             raise UnprocessableEntity('SELLER_DEPART_VAT_NUMBER_COUNTRY')
#         try:
#             departure_seller_vat_number = InputService.get_str_or_None(
#                 df, i, column='SELLER_DEPART_COUNTRY_VAT_NUMBER')
#         except:
#             raise UnprocessableEntity('SELLER_DEPART_COUNTRY_VAT_NUMBER')

#         try:
#             arrival_seller_vat_country_code = InputService.get_str_or_None(
#                 df, i, column='SELLER_ARRIVAL_VAT_NUMBER_COUNTRY')
#         except:
#             raise UnprocessableEntity('SELLER_ARRIVAL_VAT_NUMBER_COUNTRY')
#         try:
#             arrival_seller_vat_number = InputService.get_str_or_None(
#                 df, i, column='SELLER_ARRIVAL_COUNTRY_VAT_NUMBER')
#         except:
#             raise UnprocessableEntity('SELLER_ARRIVAL_COUNTRY_VAT_NUMBER')

#         try:
#             seller_vat_country_code = InputService.get_str_or_None(
#                 df, i, column='TRANSACTION_SELLER_VAT_NUMBER_COUNTRY')
#         except:
#             raise UnprocessableEntity('TRANSACTION_SELLER_VAT_NUMBER_COUNTRY')
#         try:
#             seller_vat_number = InputService.get_str_or_None(
#                 df, i, column='TRANSACTION_SELLER_VAT_NUMBER')
#         except:
#             raise UnprocessableEntity('TRANSACTION_SELLER_VAT_NUMBER')

#         try:
#             tax_calculation_imputation_country = InputService.get_str_or_None(
#                 df, i, column='VAT_CALCULATION_IMPUTATION_COUNTRY')
#         except:
#             raise UnprocessableEntity('VAT_CALCULATION_IMPUTATION_COUNTRY')
#         try:
#             tax_jurisdiction = InputService.get_str_or_None(
#                 df, i, column='TAXABLE_JURISDICTION')
#         except:
#             raise UnprocessableEntity('TAXABLE_JURISDICTION')
#         try:
#             tax_jurisdiction_level = InputService.get_str_or_None(
#                 df, i, column='TAXABLE_JURISDICTION_LEVEL')
#         except:
#             raise UnprocessableEntity('TAXABLE_JURISDICTION_LEVEL')

#         try:
#             invoice_number = InputService.get_str_or_None(
#                 df, i, column='VAT_INV_NUMBER')
#         except:
#             raise UnprocessableEntity('VAT_INV_NUMBER')
#         try:
#             invoice_amount_vat = InputService.get_float_or_None(
#                 df, i, column='VAT_INV_CONVERTED_AMT')
#         except:
#             raise UnprocessableEntity('VAT_INV_CONVERTED_AMT')
#         try:
#             invoice_currency_code = InputService.get_str_or_None(
#                 df, i, column='VAT_INV_CURRENCY_CODE')
#         except:
#             raise UnprocessableEntity('VAT_INV_CURRENCY_CODE')
#         try:
#             invoice_exchange_rate = InputService.get_float_or_None(
#                 df, i, column='VAT_INV_EXCHANGE_RATE')
#         except:
#             raise UnprocessableEntity('VAT_INV_EXCHANGE_RATE')
#         try:
#             invoice_exchange_rate_date = InputService.get_date_or_None(
#                 df, i, column='VAT_INV_EXCHANGE_RATE_DATE')
#         except:
#             raise UnprocessableEntity('VAT_INV_EXCHANGE_RATE_DATE')
#         try:
#             invoice_url = InputService.get_str_or_None(
#                 df, i, column='INVOICE_URL')
#         except:
#             raise UnprocessableEntity('INVOICE_URL')

#         try:
#             export = InputService.get_bool(
#                 df, i, column='EXPORT_OUTSIDE_EU', value_true='YES')
#         except:
#             raise UnprocessableEntity('EXPORT_OUTSIDE_EU')

#         try:
#             customer_name = InputService.get_str_or_None(
#                 df, i, column='BUYER_NAME')
#         except:
#             raise UnprocessableEntity('BUYER_NAME')
#         try:
#             customer_vat_number = InputService.get_str_or_None(
#                 df, i, column='BUYER_VAT_NUMBER')
#         except:
#             raise UnprocessableEntity('BUYER_VAT_NUMBER')
#         try:
#             customer_vat_number_country_code = InputService.get_str_or_None(
#                 df, i, column='BUYER_VAT_NUMBER_COUNTRY')
#         except:
#             raise UnprocessableEntity('BUYER_VAT_NUMBER_COUNTRY')

#         try:
#             supplier_vat_number = InputService.get_str_or_None(
#                 df, i, column='SUPPLIER_VAT_NUMBER')
#         except:
#             raise UnprocessableEntity('SUPPLIER_VAT_NUMBER')
#         try:
#             supplier_name = InputService.get_str_or_None(
#                 df, i, column='SUPPLIER_NAME')
#         except:
#             raise UnprocessableEntity('SUPPLIER_NAME')

#         #unprovided vars
#         item_brand_name = None

#         return (
#             account_given_id,
#             channel_code,
#             given_id,
#             activity_id,
#             item_sku,
#             item_name,
#             item_brand_name,
#             item_asin,
#             shipment_date,
#             arrival_date,
#             complete_date,
#             public_activity_period,
#             marketplace,
#             transaction_type_public_code,
#             tax_calculation_date,
#             item_manufacture_country,
#             item_quantity,
#             item_weight_kg,
#             item_weight_kg_total,
#             unit_cost_price_net,
#             item_price_discount_net,
#             item_price_discount_vat,
#             item_price_discount_gross,
#             item_price_net,
#             item_price_vat,
#             item_price_gross,
#             item_price_total_net,
#             item_price_total_vat,
#             item_price_total_gross,
#             item_price_vat_rate,
#             shipment_price_discount_net,
#             shipment_price_discount_vat,
#             shipment_price_discount_gross,
#             shipment_price_net,
#             shipment_price_vat,
#             shipment_price_gross,
#             shipment_price_total_net,
#             shipment_price_total_vat,
#             shipment_price_total_gross,
#             shipment_price_vat_rate,
#             sale_total_value_net,
#             sale_total_value_vat,
#             sale_total_value_gross,
#             gift_wrap_price_discount_net,
#             gift_wrap_price_discount_vat,
#             gift_wrap_price_discount_gross,
#             gift_wrap_price_net,
#             gift_wrap_price_vat,
#             gift_wrap_price_gross,
#             gift_wrap_price_total_net,
#             gift_wrap_price_total_vat,
#             gift_wrap_price_total_gross,
#             gift_wrap_price_tax_rate,
#             currency_code,
#             item_given_tax_code_code,
#             departure_country_code,
#             departure_postal_code,
#             departure_city,
#             arrival_country_code,
#             arrival_postal_code,
#             arrival_city,
#             arrival_address,
#             sale_departure_country_code,
#             sale_arrival_country_code,
#             shipment_mode,
#             shipment_conditions,
#             departure_seller_vat_country_code,
#             departure_seller_vat_number,
#             arrival_seller_vat_country_code,
#             arrival_seller_vat_number,
#             seller_vat_country_code,
#             seller_vat_number,
#             tax_calculation_imputation_country,
#             tax_jurisdiction,
#             tax_jurisdiction_level,
#             invoice_number,
#             invoice_amount_vat,
#             invoice_currency_code,
#             invoice_exchange_rate,
#             invoice_exchange_rate_date,
#             invoice_url,
#             export,
#             customer_name,
#             customer_vat_number,
#             customer_vat_number_country_code,
#             supplier_vat_number,
#             supplier_name
#         )
