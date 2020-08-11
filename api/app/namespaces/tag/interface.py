from mypy_extensions import TypedDict

class TagInterface(TypedDict, total=False):
    code: str
