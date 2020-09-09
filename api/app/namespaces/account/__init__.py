from .model import Account
from .schema import account_dto, account_sub_dto, account_admin_dto#, AccountSubSchema

BASE_ROUTE = "account"


def attach_account(api, app):
    from .controller import ns as account_ns
    api.add_namespace(account_ns, path=f"/{BASE_ROUTE}")
