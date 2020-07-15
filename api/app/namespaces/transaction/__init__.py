from .model import Transaction, TransactionType
from .schema import transaction_dto, transaction_sub_dto, transaction_admin_dto, transaction_type_dto


BASE_ROUTE = "transaction"


def attach_transaction(api, app):
    from .controller import ns as transaction_ns
    api.add_namespace(transaction_ns, path=f"/{BASE_ROUTE}")
