import pandas as pd
from datetime import date
from flask import g

from werkzeug.exceptions import UnprocessableEntity, InternalServerError

from ..utils.service import HelperService
from ..transaction.model import Transaction
from ..transaction.service import TransactionService
from ..transaction_input.model import TransactionInput
#from ..transaction_input.service import TransactionInputService

from ..business.seller_firm.model import SellerFirm

class TaxRecordService:

    @staticmethod
    def get_record_as_csv(start_date_str: str, end_date_str: str, seller_firm_public_id: str, tax_treatment_type: str):

        tax_record_dict = TaxRecordService.get_by_validity_public_id(start_date_str, end_date_str, seller_firm_public_id, tax_treatment_type)

        df_local_sales = pd.Dataframe(tax_record_dict.get('LOCAL_SALES')
        df_local_sales_reverse_charge = pd.Dataframe(tax_record_dict.get('LOCAL_SALES_REVERSE_CHARGE')
        df_distance_sales = pd.Dataframe(tax_record_dict.get('DISTANCE_SALES')
        df_non_taxable_distance_sales = pd.Dataframe(tax_record_dict.get('NON_TAXABLE_DISTANCE_SALES')
        df_intra_community_sales = pd.Dataframe(tax_record_dict.get('INTRA_COMMUNITY_SALES')
        df_exports = pd.Dataframe(tax_record_dict.get('EXPORTS')
        df_domestic_acquisitions = pd.Dataframe(tax_record_dict.get('DOMESTIC_ACQUISITIONS')
        df_intra_community_acquisitions = pd.Dataframe(tax_record_dict.get('INTRA_COMMUNITY_ACQUISITIONS')


        df_summary = TaxRecordService.calculate_front_page(df_local_sales, df_local_sales_reverse_charge, df_distance_sales, df_non_taxable_distance_sales, df_intra_community_sales, df_exports, df_domestic_acquisitions, df_intra_community_acquisitions)

        # list of dataframes and sheet names
        df_list = [df_summary, df_local_sales, df_local_sales_reverse_charge, df_distance_sales, df_non_taxable_distance_sales, df_intra_community_sales, df_exports, df_domestic_acquisitions, df_intra_community_acquisitions]
        tab_names = ['SUMMARY', 'LOCAL_SALES', 'LOCAL_SALES_REVERSE_CHARGE', 'DISTANCE_SALES', 'NON_TAXABLE_DISTANCE_SALES', 'INTRA_COMMUNITY_SALES', 'EXPORTS', 'DOMESTIC_ACQUISITIONS', 'INTRA_COMMUNITY_ACQUISITIONS']


        filename=TaxRecordService.create_filename()
        # run function
        dfs_tabs(dfs, sheets, filename)

        !!! return df.to_csv(index=False)

        @staticmethod
    !!! def calculate_front_page(df_local_sales, df_local_sales_reverse_charge, df_distance_sales, df_non_taxable_distance_sales, df_intra_community_sales, df_exports, df_domestic_acquisitions, df_intra_community_acquisitions)

            ### something happens here


            return df_summary


        @staticmethod
        !!!
        def create_filename():
            today_as_str= str(date.today().strftime('%Y%m%d'))

            filename = '{}_{}_EXPORT_{}'.format(today_as_str, seller_firm_public_id, g.user.fullname)

            return filename



!!! below is the function to write dfs into excel file with different tabs
            # function
        def dfs_tabs(df_list, tab_names, filename):
            writer=pd.ExcelWriter(filename, engine='xlsxwriter')
            for dataframe, sheet in zip(df_list, tab_names):
                dataframe.to_excel(writer, sheet_name=sheet, startrow=0, startcol=0)
                writer.save()





    # celery task on this level?
    @staticmethod
    def get_by_validity_public_id(start_date_str: str, end_date_str: str, seller_firm_public_id:str, type_filter: str):

        transactions = TransactionService.get_by_validity_public_id_type(start_date_str, end_date_str, seller_firm_public_id, type_filter)

        tax_record_dict = TaxRecordService.get_tax_record_dict_from_transactions(transactions)

        return tax_record_dict






    @staticmethod
    def append_to_tax_record_dict(tax_record_dict: dict, t_treatment_code: str, t_type_dict: dict) -> dict:
        if t_treatment_code == 'LOCAL_SALE':
            t_treatment_list: list = tax_record_dict.get('LOCAL_SALES')

        elif t_treatment_code == 'LOCAL_SALE_REVERSE_CHARGE':
            t_treatment_list: list = tax_record_dict.get('LOCAL_SALE_REVERSE_CHARGES')

        elif t_treatment_code == 'DISTANCE_SALE':
            t_treatment_list: list = tax_record_dict.get('DISTANCE_SALES')

        elif t_treatment_code == 'NON_TAXABLE_DISTANCE_SALE':
            t_treatment_list: list = tax_record_dict.get('NON_TAXABLE_DISTANCE_SALES')

        elif t_treatment_code == 'INTRA_COMMUNITY_SALE':
            t_treatment_list: list = tax_record_dict.get('INTRA_COMMUNITY_SALES')

        elif t_treatment_code == 'EXPORT':
            t_treatment_list: list = tax_record_dict.get('EXPORTS')

        elif t_treatment_code == 'DOMESTIC_ACQUISITION':
            t_treatment_list: list = tax_record_dict.get('DOMESTIC_ACQUISITIONS')

        elif t_treatment_code == 'INTRA_COMMUNITY_ACQUISITION':
            t_treatment_list: list = tax_record_dict.get('INTRA_COMMUNITY_ACQUISITIONS')


        else:
            raise InternalServerError

        t_treatment_list.append(t_type_dict)


    @staticmethod
    def create_t_type_dict(t_treatment_code: str, tax_record_base_dict: dict, transaction_input_dict: dict, t_dict: dict) -> dict:
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
    def get_tax_record_dict_from_transactions(transactions: Transaction):
        local_sales = local_sales_reverse_charge = distance_sales = non_taxable_distance_sales = intra_community_sales = exports = domestic_acquisitions = intra_community_acquisitions = []

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
            t_treatment_code = t.tax_treatment
            transaction_input = TransactionInput.query.filter_by(transaction_id = t.id).first()

            # using the sqlalchemy internal __dict__ method --> https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
            transaction_input_dict = transaction_input.__dict__
            t_dict = t.__dict__

            tax_record_base_dict = {

                    !!! --> hier führt NICO telefonat mit Davide auch
            }

            t_type_dict = TaxRecordService.create_t_type_dict(t_treatment_code: str, tax_record_base_dict: dict, transaction_input_dict: dict, t_dict: dict)
            TaxRecordService.append_to_tax_record_dict(tax_record_dict: dict, t_treatment_code: str, t_type_dict: dict)

        return tax_record_dict
