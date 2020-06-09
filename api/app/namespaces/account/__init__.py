from .model import Account
from .schema import account_dto

BASE_ROUTE = "account"


def attach_account(api, app):
    from .controller import ns as account_ns
    api.add_namespace(account_ns, path=f"/{BASE_ROUTE}")
