from mypy_extensions import TypedDict
from typing import List
from datetime import datetime

class AccountInterface(TypedDict, total=False):
    given_id: str
    created_by: int
    created_on: datetime
    modified_at: datetime
    channel_code: str
    seller_firm_id: int
