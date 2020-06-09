from mypy_extensions import TypedDict
from datetime import date, datetime
from typing import List
from . import DistanceSale


class AmazonInterface(PlatformInterface):
    distance_sales: List[DistanceSale]


class DistanceSaleInterface(TypedDict, total=False):
    created_by: int
    created_on: datetime
    original_filename: str
    valid_from: date
    valid_to: date
    platform_code: str
    seller_firm_id: int
    arrival_country_code: str
    status: bool
