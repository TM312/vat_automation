from mypy_extensions import TypedDict

class TaxAuditorInterface(TypedDict, total=False):
    email: str
    password: str
