from .model import TransactionTypePublic
from .schema import transaction_type_public_dto


BASE_ROUTE = "transaction_type_public"

def attach_transaction_type_public(api, app):
    from .controller import ns as transaction_type_public_ns
    api.add_namespace(transaction_type_public_ns, path=f"/{BASE_ROUTE}")
