from mypy_extensions import TypedDict
from typing import Union
from datetime import date

class TransactionTypeInterface(TypedDict, total=False):
    code: str
    description: str

class TransactionInterface(TypedDict, total=False):

    transaction_input_id: int
    account_id: int
    item_id: int

    amazon_vat_calculation_service: bool
    customer_relationship_checked: bool
    customer_relationship: str
    customer_vatin_id: int
    tax_jurisdiction_code: str

    type_code: str

    tax_treatment_code: str

    tax_date: date
    tax_calculation_date: date
    item_tax_code_code: str
    item_tax_rate_type_code: str
    shipment_tax_rate_type_code: str
    gift_wrap_tax_rate_type_code: str
    item_price_net: float
    item_price_discount_net: float
    item_price_total_net: float
    shipment_price_net: float
    shipment_price_discount_net: float
    shipment_price_total_net: float
    gift_wrap_price_net: float
    gift_wrap_price_discount_net: float
    gift_wrap_price_total_net: float
    item_price_vat_rate: float
    item_price_vat: float
    item_price_discount_vat: float
    item_price_total_vat: float
    shipment_price_vat_rate: float
    shipment_price_vat: float
    shipment_price_discount_vat: float
    shipment_price_total_vat: float
    gift_wrap_price_vat_rate: float
    gift_wrap_price_vat: float
    gift_wrap_price_discount_vat: float
    gift_wrap_price_total_vat: float
    total_value_net: float
    total_value_vat: float
    total_value_gross: float
    transaction_currency_code: str
    invoice_currency_code: str
    invoice_exchange_rate_date: date
    invoice_exchange_rate: float
    invoice_amount_net: float
    invoice_amount_vat: float
    invoice_amount_gross: float
    reverse_charge_vat_rate: float
    invoice_amount_reverse_charge_vat: float
    arrival_seller_vatin_id: int
    departure_seller_vatin_id: int
    seller_vatin_id: int
