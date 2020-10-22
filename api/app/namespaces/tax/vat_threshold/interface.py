from mypy_extensions import TypedDict
from datetime import date
from typing import List


class VatThresholdInterface(TypedDict, total=False):
    valid_from: date
    valid_to: date
    vat_threshold_id: int

    # mirrored attributes (no relationships!)
    created_by: int
    country_code: str
    value: int
    currency_code: str
