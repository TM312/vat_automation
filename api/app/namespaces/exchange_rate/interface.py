from mypy_extensions import TypedDict
from datetime import date, datetime


class ExchangeRateInterface(TypedDict, total=False):
    source: str
    created_on: datetime
    date: date
    base: str
    target: str
    rate: float
