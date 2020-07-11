from mypy_extensions import TypedDict

from datetime import date, datetime

class VATINInterface(TypedDict, total=False):
    created_on: datetime
    valid_from: date
    valid_to: date
    last_validated: date
    initial_tax_date: date
    country_code: str
    number: str
    valid: bool
    business_id: int
