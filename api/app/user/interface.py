from mypy_extensions import TypedDict

class UserInterface(TypedDict, total=False):
    email: str
    password: str
