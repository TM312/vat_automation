from flask import g, current_app
from app.extensions import db
from typing import List, BinaryIO
import pandas as pd

from .model import Account
from .interface import AccountInterface
from ..utils.service import InputService
from ..utils.interface import ResponseObjectInterface
from ..business.seller_firm.service import SellerFirmService



class AccountService:

    @staticmethod
    def get_by_public_id_channel_code(account_public_id: str, channel_code: str) -> Account:
        account = Account.query.filter_by(public_id=account_public_id,  channel_code=channel_code).first()
        if account:
            return account
        else:
            raise NotFound('An account for the channel {} and the id {} does not exist in our db. Please add the account before proceeding.'.format(channel_code, account_public_id))



    @staticmethod
    #kwargs can contain: seller_firm_public_id
    def process_account_files_upload(account_information_files: List[BinaryIO], **kwargs) -> ResponseObjectInterface:
        BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config['BASE_PATH_STATIC_DATA_SELLER_FIRM']

        file_type = 'account_list'
        df_encoding = 'utf-8'
        delimiter = None
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM
        user_id = g.user.id

        for file in account_information_files:
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            AccountService.process_account_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, **kwargs)

        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(account_information_files)))
        }

        return response_object



    # celery task !!
    @staticmethod
    def process_account_information_file(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, **kwargs) -> List[ResponseObjectInterface]:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)

        response_objects = AccountService.create_accounts(df, file_path_in, user_id, **kwargs)

        InputService.move_file_to_out(file_path_in, file_type)


        return response_objects




    @staticmethod
    def create_accounts(df: pd.DataFrame, file_path_in: str, user_id: int, **kwargs) -> List[ResponseObjectInterface]:

        redundancy_counter = 0
        error_counter = 0
        total_number_accounts = len(df.index)
        input_type = 'account' # only used for response objects

        for i in range(total_number_accounts):

            seller_firm_id = SellerFirmService.get_seller_firm_id(df=df, i=i, **kwargs)
            public_id = InputService.get_str(df, i, column='account_id')
            channel_code = InputService.get_str(df, i, column='channel_code')


            if seller_firm_id:
                redundancy_counter += AccountService.handle_redundancy(public_id, channel_code)
                account_data = {
                    'created_by': user_id,
                    'seller_firm_id' : seller_firm_id,
                    'public_id' : public_id,
                    'channel_code' : channel_code
                }

                try:
                    new_account = AccountService.create_account(account_data)

                except:
                    db.session.rollback()

                    error_counter += 1

            else:
                error_counter += 1


        response_objects = InputService.create_input_response_objects(file_path, input_type, total_number_accounts, error_counter, redundancy_counter=redundancy_counter)

        return response_objects


    @staticmethod
    def create_account(account_data: AccountInterface) -> Account:

        new_account = Account(
            created_by = account_data.get('created_by'),
            seller_firm_id = account_data.get('seller_firm_id'),
            public_id = account_data.get('public_id'),
            channel_code = account_data.get('channel_code')
        )

        #add seller firm to db
        db.session.add(new_account)
        db.session.commit()

        return new_account



# List all files in a directory using scandir(): Returns an iterator of all the objects in a directory including file attribute information


    @staticmethod
    def handle_redundancy(public_id: str, channel_code: str) -> int:
        account: Account = Account.query.filter(Account.public_id == public_id,  Account.channel_code == channel_code).first()

        # if an account with the same public_id and channel_code already exists, it is being deleted.
        if account:
            db.session.delete(account)
            redundancy_counter = 1

        else:
            redundancy_counter = 0

        return redundancy_counter
