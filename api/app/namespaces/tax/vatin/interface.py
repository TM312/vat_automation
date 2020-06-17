from mypy_extensions import TypedDict

from datetime import date, datetime

class VATINInterface(TypedDict, total=False):
    created_on: datetime
    valid_from: date
    valid_to: date
    initial_tax_date: date
    _country_code: str
    country_code: str
    _number: str
    number: str
    valid: bool
    business_id: int
