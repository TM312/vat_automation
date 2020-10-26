from mypy_extensions import TypedDict


class TransactionTypePublicInterface(TypedDict, total=False):
    code: str
    name: str
    description: str
    platform_code: str
    transaction_type_code: str
