from mypy_extensions import TypedDict

class ItemTagInterface(TypedDict, total=False):
    name: str
