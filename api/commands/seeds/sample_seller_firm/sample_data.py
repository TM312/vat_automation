from os import path, listdir
from datetime import date, datetime
from app.namespaces.business.seller_firm.service import SellerFirmService
from app.namespaces.user.seller.service import SellerService

from app.namespaces.account.service import AccountService
from app.namespaces.distance_sale.service import DistanceSaleService
from app.namespaces.item.service import ItemService
from app.namespaces.tax.vatin.service import VATINService
from app.namespaces.transaction_input.service import TransactionInputService
from app.namespaces.utils.service import InputService

from .. import BASE_PATH_SEEDS

class SampleFirmInformationSeedService:

    @staticmethod
    def seed_sample_data_static():
        seller_firm = SellerFirmService.get_by_name_establishment_country(seller_firm_name = 'Bond Store Ltd', establishment_country_code = 'GB')
        seller = SellerService.get_by_email('james.b@mi6-mail.com')

        seller_firm_notification_data = {
            'subject': 'Data Upload',
            'status': 'success',
            'seller_firm_id': seller_firm.id,
            'created_by': seller.id
        }

        dir_path = path.join(
            BASE_PATH_SEEDS,
            'sample_seller_firm',
            'Bond_Store_Ltd',
        )
        df_encoding = 'utf-8'
        delimiter = ','
        basepath = BASE_PATH_SEEDS

        file_path_in_accounts = path.join(dir_path,'accounts.csv')
        file_path_in_distance_sales = path.join(dir_path, 'distance_sales.csv')
        file_path_in_items = path.join(dir_path, 'items.csv')



        df_accounts = InputService.read_file_path_into_df(file_path_in_accounts, df_encoding, delimiter)
        response_object = AccountService.create_accounts(df_accounts, file_path_in_accounts, seller.id, seller_firm.id)

        df_distance_sales = InputService.read_file_path_into_df(file_path_in_distance_sales, df_encoding, delimiter)
        response_object = DistanceSaleService.create_distance_sales(df_distance_sales, file_path_in_distance_sales, seller.id, seller_firm.id)

        df_items = InputService.read_file_path_into_df(file_path_in_items, df_encoding, delimiter)
        response_object = ItemService.create_items(df_items, file_path_in_items, seller.id, seller_firm.id)

        VATINSeedService.seed_bond_vatins(seller_firm.id)


    @staticmethod
    def seed_sample_transaction_input_data():
        seller_firm = SellerFirmService.get_by_name_establishment_country(seller_firm_name = 'Bond Store Ltd', establishment_country_code = 'GB')
        seller = SellerService.get_by_email('james.b@mi6-mail.com')

        seller_firm_notification_data = {
            'subject': 'Data Upload',
            'status': 'success',
            'seller_firm_id': seller_firm.id,
            'created_by': seller.id
        }

        dir_path = path.join(
            BASE_PATH_SEEDS,
            'sample_seller_firm',
            'Bond_Store_Ltd',
        )
        df_encoding = 'utf-8'
        delimiter = ','
        basepath = '/home/data/business_data'

        file_path_in_transaction_inputs = path.join(dir_path, 'transactions', 'transactions_bond.csv')

        # TransactionInputService.handle_transaction_input_data_upload(
        #     file_path_in=file_path_in_transaction_inputs,
        #     file_type='transactions_amazon',
        #     df_encoding=df_encoding,
        #     delimiter=delimiter,
        #     basepath=basepath,
        #     user_id=seller.id,
        #     seller_firm_id=seller_firm.id,
        #     seller_firm_notification_data=seller_firm_notification_data
        # )

        df_transaction_inputs = InputService.read_file_path_into_df(file_path_in_transaction_inputs, df_encoding, delimiter)
        TransactionInputService.create_transaction_inputs_and_transactions(df_transaction_inputs, file_path_in_transaction_inputs, seller.id)



class VATINSeedService:

    @staticmethod
    def seed_bond_vatins(seller_firm_id):
        valid_from = datetime.strptime('01-06-2018', '%d-%m-%Y').date()
        vatin_data_list = [
            {
                'valid_from': valid_from,
                'request_date': date.today(),
                'country_code': 'CZ',
                'number': '685824653',
                'valid': True,
                'business_id': seller_firm_id
            },
            {
                'valid_from': valid_from,
                'request_date': date.today(),
                'country_code': 'DE',
                'number': '312256776',
                'valid': True,
                'business_id': seller_firm_id
            },
            {
                'valid_from': valid_from,
                'request_date': date.today(),
                'country_code': 'ES',
                'number': 'A91415221',
                'valid': True,
                'business_id': seller_firm_id
            },
            {
                'valid_from': valid_from,
                'request_date': date.today(),
                'country_code': 'FR',
                'number': '27850592811',
                'valid': True,
                'business_id': seller_firm_id
            },
            {
                'valid_from': valid_from,
                'request_date': date.today(),
                'country_code': 'GB',
                'number': '007836621',
                'valid': True,
                'business_id': seller_firm_id
            },
            {
                'valid_from': valid_from,
                'request_date': date.today(),
                'country_code': 'IT',
                'number': '10232149696',
                'valid': True,
                'business_id': seller_firm_id
            },
            {
                'valid_from': valid_from,
                'request_date': date.today(),
                'country_code': 'PL',
                'number': '4243264221',
                'valid': True,
                'business_id': seller_firm_id
            }
        ]

        for vatin_data in vatin_data_list:
            VATINService.create(vatin_data)
