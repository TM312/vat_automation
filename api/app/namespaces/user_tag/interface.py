from mypy_extensions import TypedDict

class UserTagInterface(TypedDict, total=False):
    name: str
