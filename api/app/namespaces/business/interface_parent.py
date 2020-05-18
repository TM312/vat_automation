from mypy_extensions import TypedDict
from datetime import date, datetime

class BusinessInterface(TypedDict, total=False):
    public_id: str
    created_by: str
    created_on: datetime
    modified_at: datetime
    name: str
    address: str
    b_type: str
