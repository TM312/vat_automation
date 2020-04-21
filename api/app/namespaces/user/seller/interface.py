from mypy_extensions import TypedDict

class SellerInterface(TypedDict, total=False):
    email: str
    password: str
