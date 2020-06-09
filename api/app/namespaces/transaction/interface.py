from mypy_extensions import TypedDict


class TransactionTypeInterface(TypedDict, total=False):
    code: str
    description: str

class TransactionInterface(TypedDict, total=False):
