from mypy_extensions import TypedDict
from datetime import date
from typing import List


class TaxCodeInterface(TypedDict, total=False):
    code: str
    name: str
    description: str
