import pandas as pd
from datetime import date
from flask import g
from typing import List, BinaryIO, Dict

from werkzeug.exceptions import UnprocessableEntity, InternalServerError, Unauthorized

from .interface import TaxRecordDictInterface

from ..utils.service import HelperService
from ..utils.interface import ResponseObjectInterface
from ..transaction.model import Transaction
from ..transaction.service import TransactionService
from ..transaction_input.model import TransactionInput
#from ..transaction_input.service import TransactionInputService

from ..business.seller_firm.model import SellerFirm
from ..user.service_parent import UserService

class TaxRecordService:

    @staticmethod
    def get_record_as_csv(start_date_str: str, end_date_str: str, seller_firm_public_id: str) -> ResponseObjectInterface:

        seller_firm = SellerFirm.query.filter_by(public_id = seller_firm_public_id)
        if g.user.employer_id == seller_firm.accounting_firm_id:

            !!! call as async celery task
            tax_record_file = TaxRecordService.get_by_validity_public_id(start_date_str, end_date_str, seller_firm_public_id)


            response_object = {
                'status': 'success',
                'message': 'Your request is being processed. You will shortly receive a tax record output for the period {}-{}.'.format(start_date_str, end_date_str)
            }
            return response_object

        else:
            raise Unauthorized('You are not authorized to retrieve tax records for this seller firm. Please make sure to establish a client relationship between your employer and the seller firm first.')



    @staticmethod
    def get_df_list(tax_record_dict: TaxRecordDictInterface) -> List[List[pd.DataFrame], List[str]]:
        tab_names = ['SUMMARY', 'LOCAL_SALES', 'LOCAL_SALES_REVERSE_CHARGE', 'DISTANCE_SALES', 'NON_TAXABLE_DISTANCE_SALES', 'INTRA_COMMUNITY_SALES', 'EXPORTS', 'DOMESTIC_ACQUISITIONS', 'INTRA_COMMUNITY_ACQUISITIONS']

        df_local_sales = pd.Dataframe(tax_record_dict.get('LOCAL_SALES')
        df_local_sales_reverse_charge = pd.Dataframe(tax_record_dict.get('LOCAL_SALES_REVERSE_CHARGE')
        df_distance_sales = pd.Dataframe(tax_record_dict.get('DISTANCE_SALES')
        df_non_taxable_distance_sales = pd.Dataframe(tax_record_dict.get('NON_TAXABLE_DISTANCE_SALES')
        df_intra_community_sales = pd.Dataframe(tax_record_dict.get('INTRA_COMMUNITY_SALES')
        df_exports = pd.Dataframe(tax_record_dict.get('EXPORTS')
        df_domestic_acquisitions = pd.Dataframe(tax_record_dict.get('DOMESTIC_ACQUISITIONS')
        df_intra_community_acquisitions = pd.Dataframe(tax_record_dict.get('INTRA_COMMUNITY_ACQUISITIONS')
        df_summary = TaxRecordService.calculate_front_page(df_local_sales, df_local_sales_reverse_charge, df_distance_sales, df_non_taxable_distance_sales, df_intra_community_sales, df_exports, df_domestic_acquisitions, df_intra_community_acquisitions)

        df_list = [df_summary, df_local_sales, df_local_sales_reverse_charge, df_distance_sales, df_non_taxable_distance_sales, df_intra_community_sales, df_exports, df_domestic_acquisitions, df_intra_community_acquisitions]

!!! hier evtl noch andere dfs und ggf. tab_names

!!! evtl. dies für summary :
####

            https: // stackoverflow.com/questions/18423298/easy-way-to-fill-in-an-excel-file-with-python



####



        return tab_names, df_list


    # celery task on this level
    @staticmethod
    def get_by_validity_public_id(start_date_str: str, end_date_str: str, seller_firm_public_id:str) -> BinaryIO:

        transactions = TransactionService.get_by_validity_public_id(start_date_str, end_date_str, seller_firm_public_id)

        tax_record_dict = TaxRecordService.get_tax_record_dict_from_transactions(transactions)

        # list of dataframes and sheet names
        tab_names, df_list = TaxRecordService.get_df_list(tax_record_dict)
        filename=TaxRecordService.create_filename(seller_firm_public_id)

        # run function
        tax_record_file = !!! dfs_tabs(dfs, sheets, filename)

        return tax_record_file



        @staticmethod
    !!! def calculate_front_page(df_local_sales: pd.DataFrame, df_local_sales_reverse_charge: pd.DataFrame, df_distance_sales: pd.DataFrame, df_non_taxable_distance_sales: pd.DataFrame, df_intra_community_sales: pd.DataFrame, df_exports: pd.DataFrame, df_domestic_acquisitions: pd.DataFrame, df_intra_community_acquisitions: pd.DataFrame) -> pd.DataFrame:

            ### something happens here


            return df_summary


        @staticmethod
        def create_filename(seller_firm_public_id: str) -> str:
            today_as_str= str(date.today().strftime('%Y%m%d'))
            seller_firm = Seller.query.filter(public_id = seller_firm_public_id).first()
            if seller_firm.accounting_firm_client_id:
                filename = '{}_{}_EXPORT'.format(today_as_str, seller_firm.accounting_firm_client_id)
            else:
                filename = '{}_{}_EXPORT'.format(today_as_str, seller_firm_public_id)

            return filename



!!! below is the function to write dfs into excel file with different tabs
            # function
        def dfs_tabs(df_list, tab_names, filename):
            writer=pd.ExcelWriter(filename, engine='xlsxwriter')
            for dataframe, sheet in zip(df_list, tab_names):
                dataframe.to_excel(writer, sheet_name=sheet, startrow=0, startcol=0)
                writer.save()






    @staticmethod
    def append_to_tax_record_dict(tax_record_dict: Dict, t_treatment_code: str, t_type_dict: Dict):
        if t_treatment_code == 'LOCAL_SALE':
            t_treatment_list: List[Dict] = tax_record_dict.get('LOCAL_SALES')

        elif t_treatment_code == 'LOCAL_SALE_REVERSE_CHARGE':
            t_treatment_list: List[Dict] = tax_record_dict.get('LOCAL_SALE_REVERSE_CHARGES')

        elif t_treatment_code == 'DISTANCE_SALE':
            t_treatment_list: List[Dict] = tax_record_dict.get('DISTANCE_SALES')

        elif t_treatment_code == 'NON_TAXABLE_DISTANCE_SALE':
            t_treatment_list: List[Dict] = tax_record_dict.get('NON_TAXABLE_DISTANCE_SALES')

        elif t_treatment_code == 'INTRA_COMMUNITY_SALE':
            t_treatment_list: List[Dict] = tax_record_dict.get('INTRA_COMMUNITY_SALES')

        elif t_treatment_code == 'EXPORT':
            t_treatment_list: List[Dict] = tax_record_dict.get('EXPORTS')

        elif t_treatment_code == 'DOMESTIC_ACQUISITION':
            t_treatment_list: List[Dict] = tax_record_dict.get('DOMESTIC_ACQUISITIONS')

        elif t_treatment_code == 'INTRA_COMMUNITY_ACQUISITION':
            t_treatment_list: List[Dict] = tax_record_dict.get('INTRA_COMMUNITY_ACQUISITIONS')


        else:
            raise InternalServerError

        t_treatment_list.append(t_type_dict)



    @staticmethod
    def create_t_type_dict(t_treatment_code: str, tax_record_base_dict: Dict, transaction_input_dict: Dict, t_dict: Dict) -> Dict:
        if t_treatment_code == 'LOCAL_SALE':
            t_type_dict =

            --> !! hier werden die tax type spezifischen dicts definiert auf Basis Gespräch Davide Nico

        elif t_treatment_code == 'LOCAL_SALE_REVERSE_CHARGE':
            t_type_dict =


        elif t_treatment_code == 'DISTANCE_SALE':
            t_type_dict =

        elif t_treatment_code == 'NON_TAXABLE_DISTANCE_SALE':
            t_type_dict =

        elif t_treatment_code == 'INTRA_COMMUNITY_SALE':
            t_type_dict =

        elif t_treatment_code == 'EXPORT':
            t_type_dict =

        elif t_treatment_code == 'DOMESTIC_ACQUISITION':
            t_type_dict =

        elif t_treatment_code == 'INTRA_COMMUNITY_ACQUISITION':
            t_type_dict =


        else:
            raise UnprocessableEntity('Transaction type unknown.')

        return t_type_dict




    @staticmethod
    def get_tax_record_dict_from_transactions(transactions: Transaction) -> TaxRecordDictInterface:
        local_sales = local_sales_reverse_charge = distance_sales = non_taxable_distance_sales = intra_community_sales = exports = domestic_acquisitions = intra_community_acquisitions = []
        t_treatment_list=[]

        tax_record_dict = {
            'LOCAL_SALES': local_sales,
            'LOCAL_SALE_REVERSE_CHARGES': local_sales_reverse_charge,
            'DISTANCE_SALES': distance_sales,
            'NON_TAXABLE_DISTANCE_SALES': non_taxable_distance_sales,
            'INTRA_COMMUNITY_SALES': intra_community_sales,
            'EXPORTS': exports,
            'DOMESTIC_ACQUISITIONS': domestic_acquisitions,
            'INTRA_COMMUNITY_ACQUISITIONS': intra_community_acquisitions
        }


        for t in transactions:
            seller_firm = SellerFirm.query.filter(id = t.account.seller_firm_id).first()
            t_treatment_code = t.tax_treatment
            transaction_input = TransactionInput.query.filter_by(transaction_id = t.id).first()

            # # using the sqlalchemy internal __dict__ method --> https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
            # transaction_input_dict = transaction_input.__dict__
            # t_dict = t.__dict__

            tax_record_base_dict = {

                'SELLER_FIRM_ID': seller_firm.id,
                'SELLER_FIRM_NAME': seller_firm.name,
                'SELLER_FIRM_ADDRESS': seller_firm.address,
                'SELLER_FIRM_ESTABLISHMENT_COUNTRY': seller_firm.establishment_country_code,

                'CREATED_BY': UserService.get_by_id(id=transaction_input.created_by).username,
                'ORIGINAL_FILENAME': transaction_input.original_filename,

                'ACCOUNT_PUBLIC_ID': transaction_input.account_public_id,
                'CHANNEL_CODE': transaction_input.channel_code,
                'MARKETPLACE': transaction_input.marketplace,
                'TRANSACTION_TYPE': t.transaction_type,

                'PUBLIC_ID': transaction_input.public_id,
                'ACTIVITY_ID': transaction_input.activity_id,

                'AMAZON_VAT_CALCULATION_SERVICE': t.amazon_vat_calculation_service,
                'CUSTOMER_RELATIONSHIP_CODE': t.customer_relationship_code,
                'CUSTOMER_RELATIONSHIP_CODE_CHECKED': t.customer_relationship_code_checked,
                'TAX_TREATMENT_CODE': t.tax_treatment_code,

                'TAX_CALCULATION_DATE': transaction_input.check_tax_calculation_date,
                'SHIPMENT_DATE': transaction_input.shipment_date,
                'TAX_DATE': t.tax_date,

                'ITEM_SKU': transaction_input.item_sku,
                'ITEM_NAME': transaction_input.item_name,
                'ITEM_QUANTITY': transaction_input.item_quantity,

                'ITEM_PRICE_NET': t.item_price_net,
                'ITEM_PRICE_DISCOUNT_NET': t.item_price_discount_net,
                'ITEM_PRICE_TOTAL_NET': t.item_price_total_net,

                'SHIPMENT_PRICE_NET': t.shipment_price_net,
                'SHIPMENT_PRICE_DISCOUNT_NET': t.shipment_price_discount_net,
                'SHIPMENT_PRICE_TOTAL_NET': t.shipment_price_total_net,

                'GIFT_WRAP_PRICE_NET': t.gift_wrap_price_net,
                'GIFT_WRAP_PRICE_DISCOUNT_NET': t.gift_wrap_price_discount_net,
                'GIFT_WRAP_PRICE_TOTAL_NET': t.gift_wrap_price_total_net,

                'ITEM_PRICE_VAT_RATE': t.item_price_vat_rate,
                'ITEM_PRICE_VAT': t.item_price_vat,
                'ITEM_PRICE_DISCOUNT_VAT': t.item_price_discount_vat,
                'ITEM_PRICE_TOTAL_VAT': t.item_price_total_vat,

                'SHIPMENT_PRICE_VAT_RATE': t.gift_wrap_vat_rate,
                'SHIPMENT_PRICE_VAT': t.shipment_price_vat,
                'SHIPMENT_PRICE_DISCOUNT_VAT': t.shipment_price_discount_vat,
                'SHIPMENT_PRICE_TOTAL_VAT': t.shipment_price_total_vat,

                'GIFT_WRAP_PRICE_VAT_RATE': t.shipment_price_vat_rate,
                'GIFT_WRAP_PRICE_VAT': t.gift_wrap_price_vat,
                'GIFT_WRAP_PRICE_DISCOUNT_VAT': t.gift_wrap_price_discount_vat,
                'GIFT_WRAP_PRICE_TOTAL_VAT': t.gift_wrap_price_total_vat,

                'TOTAL_VALUE_NET': t.total_value_net,
                'TOTAL_VALUE_VAT': t.total_value_vat,
                'TOTAL_VALUE_GROSS': t.total_value_gross,

                'ITEM_PRICE_GROSS': transaction_input.item_price_gross,
                'ITEM_PRICE_DISCOUNT_GROSS': transaction_input.item_price_discount_gross,
                'ITEM_PRICE_TOTAL_GROSS': transaction_input.item_price_total_gross,

                'SHIPMENT_PRICE_GROSS': transaction_input.shipment_price_gross,
                'SHIPMENT_PRICE_DISCOUNT_GROSS': transaction_input.shipment_price_discount_gross,
                'SHIPMENT_PRICE_TOTAL_GROSS': transaction_input.shipment_price_total_gross,

                'GIFT_WRAP_PRICE_GROSS': transaction_input.gift_wrap_price_gross,
                'GIFT_WRAP_PRICE_DISCOUNT_GROSS': transaction_input.gift_wrap_price_discount_net,
                'GIFT_WRAP_PRICE_TOTAL_GROSS': transaction_input.gift_wrap_price_total_gross,

                'INVOICE_CURRENCY': t.invoice_currency_code

                'ITEM_TAX_CODE':
                'ITEM_TAX_RATE_TYPE':

                'DEPARTURE_CITY':
                'DEPARTURE_COUNTRY':
                'DEPARTURE_POSTAL_CODE':

                'ARRIVAL_CITY':
                'ARRIVAL_COUNTRY':
                'ARRIVAL_POSTAL_CODE':

                'DEPARTURE_SELLER_VAT_NUMBER_COUNTRY':
                'DEPARTURE_SELLER_VAT_NUMBER':
                'DEPARTURE_SELLER_VAT_VALID':
                'DEPARTURE_SELLER_VAT_CHECKED_DATE':

                'ARRIVAL_SELLER_VAT_NUMBER_COUNTRY':
                'ARRIVAL_SELLER_VAT_NUMBER':
                'ARRIVAL_SELLER_VAT_VALID':
                'ARRIVAL_SELLER_VAT_CHECKED_DATE':

                'SELLER_VAT_NUMBER_COUNTRY':
                'SELLER_VAT_NUMBER':
                'SELLER_VAT_VALID':
                'SELLER_VAT_CHECKED_DATE':

                'CUSTOMER_VAT_NUMBER_COUNTRY':
                'CUSTOMER_VAT_NUMBER':
                'CUSTOMER_VAT_VALID':
                'CUSTOMER_VAT_CHECKED_DATE':

                'TAX_JURISDICTION':

                'INVOICE_AMOUNT_NET':
                'INVOICE_AMOUNT_VAT':
                'INVOICE_AMOUNT_GROSS':

                'INVOICE_NUMBER':
                'INVOICE_CURRENCY':
                'INVOICE_EXCHANGE_RATE':
                'INVOICE_EXCHANGE_RATE_DATE':
                'INVOICE_URL':

                'CUSTOMER_NAME':

                'ARRIVAL_ADDRESS':
                'SUPPLIER_NAME':
                'SUPPLIER_VAT_NUMBER':




                    invoice amounts auf 2 Nachkommastellen gerundet
                    Rates auf 5
            }

            t_type_dict = TaxRecordService.create_t_type_dict(t_treatment_code: str, tax_record_base_dict: Dict, transaction_input_dict: Dict, t_dict: Dict)
            TaxRecordService.append_to_tax_record_dict(tax_record_dict: Dict, t_treatment_code: str, t_type_dict: Dict)

        return tax_record_dict
