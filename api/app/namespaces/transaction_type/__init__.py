from .model import TransactionType
from .schema import transaction_type_dto


BASE_ROUTE = "transaction_type"

def attach_transaction_type(api, app):
    from .controller import ns as transaction_type_ns
    api.add_namespace(transaction_type_ns, path=f"/{BASE_ROUTE}")
