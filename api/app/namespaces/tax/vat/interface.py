from mypy_extensions import TypedDict
from datetime import date
from typing import List


class VatInterface(TypedDict, total=False):
    valid_from: date
    valid_to: date
    country_code: str
    tax_code_code: str
    tax_rate_type_code: str
    rate: float
