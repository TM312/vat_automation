from mypy_extensions import TypedDict
from datetime import datetime


class TokenInterface(TypedDict, total: False):
    auth_token: str
    sub: str
    iat: datetime
    sub: str
    blacklisted_on: datetime
