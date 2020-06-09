from mypy_extensions import TypedDict
from datetime import date
from typing import List

class CurrencyInterface(TypedDict, total=False):
    code: str
    name: str
    countries: List['app.namespaces.country.Country']
