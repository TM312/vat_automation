from os import path, listdir
from datetime import date
from app.namespaces.business.seller_firm.service import SellerFirmService
from app.namespaces.user.seller.service import SellerService

from app.namespaces.account.service import AccountService
from app.namespaces.distance_sale.service import DistanceSaleService
from app.namespaces.item.service import ItemService
from app.namespaces.tax.vatin.service import VATINService
from app.namespaces.transaction_input.service import TransactionInputService

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
        df_encoding = 'utf-8',
        delimiter = ',',
        basepath = '/home/data/business_data',

        file_path_in_accounts = path.join(dir_path,'accounts.csv')
        file_path_in_distance_sales = path.join(dir_path, 'distance_sales.csv')
        file_path_in_items = path.join(dir_path, 'items.csv')

        print(listdir(file_path_in_accounts), flush=True)  # returns list


        # AccountService.handle_account_data_upload(
        #     file_path_in=file_path_in_accounts,
        #     file_type = 'account_list',
        #     df_encoding=df_encoding,
        #     delimiter=delimiter,
        #     basepath=basepath,
        #     user_id=seller.id,
        #     seller_firm_id=seller_firm.id,
        #     seller_firm_notification_data=seller_firm_notification_data
        # )


        # DistanceSaleService.handle_distance_sale_data_upload(
        #     file_path_in=file_path_in_distance_sales,
        #     file_type='distance_sale_list',
        #     df_encoding=df_encoding,
        #     delimiter=delimiter,
        #     basepath=basepath,
        #     user_id=seller.id,
        #     seller_firm_id=seller_firm.id,
        #     seller_firm_notification_data=seller_firm_notification_data
        # )

        # ItemService.handle_item_data_upload(
        #     file_path_in=file_path_in_items,
        #     file_type='item_list',
        #     df_encoding=df_encoding,
        #     delimiter=delimiter,
        #     basepath=basepath,
        #     user_id=seller.id,
        #     seller_firm_id=seller_firm.id,
        #     seller_firm_notification_data=seller_firm_notification_data
        # )

        # VATINSeedService.seed_bond_vatins(seller_firm.id)


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
        df_encoding = 'utf-8',
        delimiter = ',',
        basepath = '/home/data/business_data',

        file_path_in_transaction_inputs = path.join(dir_path, 'transactions', 'Sales Tax Transaction Report_MBOND-2020-01')

        TransactionInputService.handle_transaction_input_data_upload(
            file_path_in=file_path_in_transaction_inputs,
            file_type='transactions_amazon',
            df_encoding=df_encoding,
            delimiter=delimiter,
            basepath=basepath,
            user_id=seller.id,
            seller_firm_id=seller_firm.id,
            seller_firm_notification_data=seller_firm_notification_data
        )



class VATINSeedService:

    @staticmethod
    def seed_bond_vatins(seller_firm_id):
        valid_from = datetime.strptime('01-06-2018', '%d-%m-%Y').date()
        vatin_data_list[
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
