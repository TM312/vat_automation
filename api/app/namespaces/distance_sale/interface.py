from mypy_extensions import TypedDict
from datetime import date, datetime

class DistanceSaleInterface(TypedDict, total=False):
    created_by: str
    created_on: datetime
    original_filename: str
    valid_from: date
    valid_to: date
    platform_code: str
    seller_firm_id: int
    arrival_country_code: str
    status: bool
