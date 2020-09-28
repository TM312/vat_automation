from mypy_extensions import TypedDict
from typing import List


class TaxRateTypeInterface(TypedDict, total=False):
    code: str
    name: str
    description: str
