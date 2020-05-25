from mypy_extensions import TypedDict
from datetime import datetime

class CustomerInterface(TypedDict, total=False):
    name: str
    address: str
    modified_at: datetime
    times_modified: int
