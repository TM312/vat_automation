from mypy_extensions import TypedDict
from datetime import date, datetime
from uuid import UUID

class BusinessInterface(TypedDict, total=False):
    id: int
    public_id: UUID
    created_by: str
    created_on: datetime
    modified_at: datetime
    times_modified: int
    name: str
    address: str
    b_type: str
