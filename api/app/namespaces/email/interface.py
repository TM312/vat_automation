from mypy_extensions import TypedDict


class EmailInterface(TypedDict, total=False):
    token: str
