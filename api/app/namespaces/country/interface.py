from mypy_extensions import TypedDict
from datetime import date
from typing import List
from .model import Country

class CountryInterface(TypedDict, total=False):
    code: str
    vat_country_code: str
    name: str
    valid_from: date
    valid_to: date
    eus: List['app.namespaces.country.EU']
    currency_code: str


class EUInterface(TypedDict, total=False):
    id: int
    valid_from: date
    valid_to: date
    countries: List[Country]
