from mypy_extensions import TypedDict


class ResponseObjectInterface(TypedDict, total=False):
    status: str
    message: str
    token: str
