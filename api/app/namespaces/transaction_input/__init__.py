from .model import TransactionInput
from .schema import transaction_input_dto, transaction_input_sub_dto, transaction_input_admin_dto

BASE_ROUTE = "transaction_input"

def attach_transaction_input(api, app):
    from .controller import ns as transaction_input_ns
    api.add_namespace(transaction_input_ns, path=f"/{BASE_ROUTE}")
