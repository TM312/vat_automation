from mypy_extensions import TypedDict
from datetime import date, datetime

class ItemInterface(TypedDict, total=False):

    created_by: int
    created_on: datetime
    original_filename: str
    sku: str
    seller_firm_id: int
    valid_from: date
    valid_to: date
    brand_name: str
    name: str
    ean: str
    asin: str
    fnsku: str
    weight_kg: float
    tax_code_code: str
    unit_cost_price_currency_code: str
    unit_cost_price_net: float
