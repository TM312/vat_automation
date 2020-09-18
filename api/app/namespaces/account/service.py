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
        return Account.query.all()

    @staticmethod
    def get_all_by_seller_firm_id(seller_firm_id: int) -> List[Account]:
        return Item.query.filter_by(seller_firm_id=seller_firm_id).all()

    @staticmethod
    def get_by_id(account_id: int) -> Account:
        return Account.query.filter_by(id = account_id).first()

    @staticmethod
    def get_by_public_id(account_public_id: str) -> Account:
        return Account.query.filter_by(public_id = account_public_id).first()

    @staticmethod
    def get_by_given_id_channel_code(account_given_id: str, channel_code: str) -> Account:
        return Account.query.filter(Account.given_id==account_given_id, Account.channel_code==channel_code).first()

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
            account = AccountService.get_by_given_id_channel_code(account_data['given_id'], account_data['channel_code'])
            if account:
                return account
            else:
                try:
                    new_account = AccountService.create(account_data)
                    return new_account

                except:
                    db.session.rollback()
                    raise



    @staticmethod
    def handle_account_data_upload(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: Dict) -> Dict:
        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_object = AccountService.create_accounts(df, file_path_in, user_id, seller_firm_id)
        tag = TagService.get_by_code('ACCOUNT')
        NotificationService.handle_seller_firm_notification_data_upload(seller_firm_id, user_id, tag, seller_firm_notification_data)
        InputService.move_file_to_out(file_path_in, basepath, file_type)

        return response_object


    @staticmethod
    def get_df_vars(df: pd.DataFrame, i: int, current: int, object_type: str) -> List:
        try:
            given_id = InputService.get_str(df, i, column='account_id')
        except:
            SocketService.emit_status_error_column_read(current, object_type, column_name='account_id')
            return False

        if not given_id or given_id == '':
            SocketService.emit_status_error_no_value(current, object_type, column_name='account_id')
            return False

        try:
            channel_code = InputService.get_str(df, i, column='channel_code')
        except:
            SocketService.emit_status_error_column_read(current, object_type, column_name='channel_code')
            return False

        if not channel_code or channel_code == '':
            SocketService.emit_status_error_no_value(current, object_type, column_name='channel_code')
            return False

        return given_id, channel_code





    @staticmethod
    def create_accounts(df: pd.DataFrame, file_path_in: str, user_id: int, seller_firm_id: int) -> List[Dict]:

        redundancy_counter = 0
        error_counter = 0
        total = total_number_accounts = len(df.index)
        original_filename = os.path.basename(file_path_in)[:128]
        object_type = object_type_human_read = 'account'
        duplicate_list = []
        duplicate_counter = 0


        if not seller_firm_id:
            # send error status via socket
            SocketService.emit_status_error_no_seller_firm(object_type)
            return False

         # send status update via socket
        SocketService.emit_status_success(0, total, original_filename, object_type)

        for i in range(total_number_accounts):
            current = i + 1

            given_id, channel_code = AccountService.get_df_vars(df, i, current, object_type)
            if not isinstance(given_id, str) and isinstance(channel_code, str):
                return False


            account = AccountService.get_by_given_id_channel_code(given_id, channel_code)
            if account:
                print('found account for given_id: {} | channel_code: {} --> {}'.format(given_id, channel_code, account), flush=True)
                if not duplicate_counter > 2:
                    message = 'The account "{}-{}" has already been registered and skipped consequently.'.format(channel_code, given_id)
                    SocketService.emit_status_info(object_type, message)
                duplicate_list.append('{}: {}'.format(channel_code, given_id))
                total -= 1
                duplicate_counter +=1
                continue


            else:
                account_data = {
                    'created_by': user_id,
                    'original_filename': original_filename,
                    'seller_firm_id' : seller_firm_id,
                    'given_id' : given_id,
                    'channel_code' : channel_code
                }


                try:
                    new_account = AccountService.create(account_data)

                except:
                    db.session.rollback()
                    error_counter += 1

                    # send error status via socket
                    message = 'Error at {} "{}" for channel "{}" (file: {}). Please recheck.'.format(object_type_human_read, given_id, channel_code, original_filename)
                    SocketService.emit_status_error(object_type, message)
                    return False


                # send status update via socket
                SocketService.emit_status_success(current, total, original_filename, object_type)

        # following the succesful processing, the vuex store is being reset
        # first cleared
        SocketService.emit_clear_objects(object_type)
        # then refilled
        AccountService.push_all_by_seller_firm_id(seller_firm_id, object_type)

        # send final status via socket
        SocketService.emit_status_final(total, original_filename, object_type, object_type_human_read, duplicate_list=duplicate_list)

        return True


    @staticmethod
    def push_all_by_seller_firm_id(seller_firm_id: int, object_type: str) -> None:
        socket_list = []
        accounts = AccountService.get_all_by_seller_firm_id(seller_firm_id)

        for account in accounts:
            # push accounts to vuex via socket
            account_json = AccountSubSchema.get_account_sub(account)

            if len(items) < 10:
                SocketService.emit_new_object(account_json, object_type)
            else:
                socket_list.append(account_json)


            if len(socket_list) > 0:
                SocketService.emit_new_objects(socket_list, object_type)



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
