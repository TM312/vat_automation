from .model import Account

class AccountService:

    @staticmethod
    def get_by_public_id_channel_code(account_public_id: str, channel_code: str) -> Account:
        account = Account.query.filter_by(
            public_id=account_public_id,  channel_code=channel_code).first()
        if account:
            return account
        else:
            raise NotFound('An account for the channel {} and the id {} does not exist in our db. Please add the account before proceeding.'.format(channel_code, account_public_id))
