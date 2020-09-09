import os
from typing import (
    List,
    BinaryIO,
    Dict)

import pandas as pd


from flask import g, current_app

from app.extensions import (
    db,
    socket_io)

from app.extensions.socketio.emitters import SocketService

from . import Account
from .schema import AccountSubSchema
from .interface import AccountInterface
from ..utils.service import InputService
from ..tag.service import TagService
from ..utils.service import NotificationService





class AccountService:

    @staticmethod
    def get_all() -> List[Account]:
        accounts = Account.query.all()
        return accounts

    @staticmethod
    def get_by_id(account_id: int) -> Account:
        return Account.query.filter(Account.id == account_id).first()

    @staticmethod
    def get_by_public_id(account_public_id: str) -> Account:
        return Account.query.filter_by(public_id = account_public_id).first()

    @staticmethod
    def get_by_given_id_channel_code(account_given_id: str, channel_code: str) -> Account:
        account = Account.query.filter_by(given_id=account_given_id,  channel_code=channel_code).first()
        if account:
            return account
        else:
            raise NotFound('An account for the channel {} and the id {} does not exist in our db. Please add the account before proceeding.'.format(channel_code, account_given_id))


    @staticmethod
    def update(account_id: int, data_changes: AccountInterface) -> Account:
        account = AccountService.get_by_id(account_id)
        if account:
            account.update(data_changes)
            db.session.commit()
            return account

    @staticmethod
    def update_by_public_id(account_public_id: str, data_changes: AccountInterface) -> Account:
        account = AccountService.get_by_public_id(account_public_id)
        if account:
            account.update(data_changes)
            db.session.commit()
            return account

    @staticmethod
    def delete_by_id(account_id: int):
        account = AccountService.get_by_id(account_id)
        if account:
            db.session.delete(account)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Account (code: {}) has been successfully deleted.'.format(account_id)
            }
            return response_object
        else:
            raise NotFound('This account does not exist.')

    @staticmethod
    def delete_by_public_id(account_public_id: str):
        account = AccountService.get_by_public_id(account_public_id)
        if account:
            db.session.delete(account)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Account (code: {}) has been successfully deleted.'.format(account_public_id)
            }
            return response_object
        else:
            raise NotFound('This account does not exist.')


    @staticmethod
    def process_single_submit(seller_firm_public_id: str, account_data: AccountInterface):

        account_data['created_by'] = g.user.id

        new_account = AccountService.create_by_seller_firm_public_id(seller_firm_public_id, account_data)

        return new_account


    @staticmethod
    def create_by_seller_firm_public_id(seller_firm_public_id: str, account_data: AccountInterface) -> Account:
        from ..business.seller_firm.service import SellerFirmService

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if seller_firm:
            account_data['seller_firm_id'] = seller_firm.id
            AccountService.handle_redundancy(account_data['given_id'], account_data['channel_code'])

            try:
                new_account = AccountService.create(account_data)
                return new_account

            except:
                db.session.rollback()
                raise



    # @staticmethod
    # def process_account_files_upload(account_information_files: List[BinaryIO], seller_firm_public_id: str) -> Dict:
    #     from ..business.seller_firm.service import SellerFirmService

    #     BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config.BASE_PATH_STATIC_DATA_SELLER_FIRM

    #     file_type = 'account_list'
    #     df_encoding = 'utf-8'
    #     delimiter = ';'
    #     basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM
    #     user_id = g.user.id
    #     seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)

    #     for file in account_information_files:
    #         file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
    #         AccountService.process_account_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm.id)

    #     response_object = {
    #         'status': 'success',
    #         'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(account_information_files)))
    #     }

    #     return response_object


    @staticmethod
    def handle_account_data_upload(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: Dict) -> Dict:
        response_object = AccountService.process_account_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm_id)
        tag = TagService.get_by_code('ACCOUNT')
        NotificationService.handle_seller_firm_notification_data_upload(seller_firm_id, user_id, tag, seller_firm_notification_data)

        return response_object



    @staticmethod
    def process_account_information_file(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int) -> List[Dict]:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)

        response_objects = AccountService.create_accounts(df, file_path_in, user_id, seller_firm_id)

        InputService.move_file_to_out(file_path_in, basepath, file_type)


        return response_objects




    @staticmethod
    def create_accounts(df: pd.DataFrame, file_path_in: str, user_id: int, seller_firm_id: int) -> List[Dict]:

        redundancy_counter = 0
        error_counter = 0
        total_number_accounts = len(df.index)
        input_type = 'account' # only used for response objects
        original_filename = os.path.basename(file_path_in)[:128]

        for i in range(total_number_accounts):

            try:
                given_id = InputService.get_str(df, i, column='account_id')
            except:
                # send error status via socket
                title = 'Can not read column "account_id" in row {}.'.format(i+1)
                SocketService.emit_status_error(i+1, total_number_accounts, original_filename, 'account', title)
                return False

            if not given_id or given_id == '':
                # send error status via socket
                title = 'No account id provided in row {}.'.format(i+1)
                SocketService.emit_status_error(i+1, total_number_accounts, original_filename, 'account', title)
                return False

            try:
                channel_code = InputService.get_str(df, i, column='channel_code')
            except:
                # send error status via socket
                title = 'Can not read column "channel_code" in row {}.'.format(i+1)
                SocketService.emit_status_error(i+1, total_number_accounts, original_filename, 'account', title)
                return False

            if not channel_code or channel_code == '':
                # send error status via socket
                title = 'No channel provided in row {}.'.format(i+1)
                SocketService.emit_status_error(i+1, total_number_accounts, original_filename, 'account', title)
                return False


            redundancy_counter += AccountService.handle_redundancy(given_id, channel_code)
            account_data = {
                'created_by': user_id,
                'original_filename': original_filename,
                'seller_firm_id' : seller_firm_id,
                'given_id' : given_id,
                'channel_code' : channel_code
            }

            try:
                new_account = AccountService.create(account_data)

                # send status update via socket
                title = 'New accounts are being registered...'
                SocketService.emit_status_success(i+1, total_number_accounts, original_filename, 'account', title)

                # push new distance sale to vuex via socket
                account_json = AccountSubSchema.get_account_sub(new_account)
                SocketService.emit_new_account(meta=account_json)

            except:
                db.session.rollback()
                error_counter += 1

                # send error status via socket
                title = 'Error at account "{}" for channel "{}". Please recheck.'.format(given_id, channel_code)
                SocketService.emit_status_error(i+1, total_number_accounts, original_filename, 'account', title)
                return False

        # send final status via socket
        if redundancy_counter > 0:
            title = '{} accounts have been successfully registered. {} accounts already existed before and have been updated.'.format(total_number_accounts, redundancy_counter)
        else:
            title = '{} accounts have been successfully registered.'.format(total_number_accounts)
        SocketService.emit_status_final(i+1, total_number_accounts, original_filename, 'account', title)

        return True



    @staticmethod
    def create(account_data: AccountInterface) -> Account:

        new_account = Account(
            created_by = account_data.get('created_by'),
            original_filename=account_data.get('original_filename'),
            seller_firm_id = account_data.get('seller_firm_id'),
            given_id = account_data.get('given_id'),
            channel_code = account_data.get('channel_code')
        )

        #add seller firm to db
        db.session.add(new_account)
        db.session.commit()

        return new_account



# List all files in a directory using scandir(): Returns an iterator of all the objects in a directory including file attribute information


    @staticmethod
    def handle_redundancy(given_id: str, channel_code: str) -> int:
        redundancy_counter = 0

        account = Account.query.filter(Account.given_id == given_id,  Account.channel_code == channel_code).first()

        # if an account with the same given_id and channel_code already exists, it is being deleted. !!!! need to take care of
        if account:
            db.session.delete(account)
            redundancy_counter += 1

        return redundancy_counter
