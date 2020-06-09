from mypy_extensions import TypedDict
from datetime import datetime
from uuid import UUID

class UserInterface(TypedDict, total=False):
    name: str
    email: str
    employer_id: int
    role: str
    password: str
    location: str
