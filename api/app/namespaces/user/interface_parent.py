from mypy_extensions import TypedDict
from datetime import datetime

class UserInterface(TypedDict, total=False):
    public_id: str

    registered_on: datetime
    modified_at: datetime
    confirmed: bool
    confirmed_on: datetime
    last_seen: datetime

    username: str
    email: str

    employer_id: int
    role: str
    password_hash: str
    avatar_hash: str
    location: str

    u_type: str
