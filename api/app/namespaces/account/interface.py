from mypy_extensions import TypedDict
from datetime import datetime
from uuid import UUID

class AccountInterface(TypedDict, total=False):
    given_id: str
    created_by: int
    created_on: datetime
    modified_at: datetime
    channel_code: str
    seller_firm_id: int
