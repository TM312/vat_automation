from mypy_extensions import TypedDict
from typing import List


class BundleInterface(TypedDict, total=False):
    id: int
    transaction_inputs: List['app.namespaces.transaction_input.TransactionInput']
