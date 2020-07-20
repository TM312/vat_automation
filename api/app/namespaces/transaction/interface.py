from mypy_extensions import TypedDict
from typing import Union
from decimal import Decimal
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
    customer_firm_id: int
    customer_firm_vatin_id: int
    tax_jurisdiction_code: str

    type_code: str

    tax_treatment_code: str

    tax_date: date
    tax_calculation_date: date
    item_tax_code_code: str
    item_tax_rate_type_code: str
    shipment_tax_rate_type_code = str
    gift_wrap_tax_rate_type_code = str
    item_price_net: Union[float, int, complex, Decimal]
    item_price_discount_net: Union[float, int, complex, Decimal]
    item_price_total_net: Union[float, int, complex, Decimal]
    shipment_price_net: Union[float, int, complex, Decimal]
    shipment_price_discount_net: Union[float, int, complex, Decimal]
    shipment_price_total_net: Union[float, int, complex, Decimal]
    gift_wrap_price_net: Union[float, int, complex, Decimal]
    gift_wrap_price_discount_net: Union[float, int, complex, Decimal]
    gift_wrap_price_total_net: Union[float, int, complex, Decimal]
    item_price_vat_rate: Union[float, int, complex, Decimal]
    item_price_vat: Union[float, int, complex, Decimal]
    item_price_discount_vat: Union[float, int, complex, Decimal]
    item_price_total_vat: Union[float, int, complex, Decimal]
    shipment_price_vat_rate: Union[float, int, complex, Decimal]
    shipment_price_vat: Union[float, int, complex, Decimal]
    shipment_price_discount_vat: Union[float, int, complex, Decimal]
    shipment_price_total_vat: Union[float, int, complex, Decimal]
    gift_wrap_price_vat_rate: Union[float, int, complex, Decimal]
    gift_wrap_price_vat: Union[float, int, complex, Decimal]
    gift_wrap_price_discount_vat: Union[float, int, complex, Decimal]
    gift_wrap_price_total_vat: Union[float, int, complex, Decimal]
    total_value_net: Union[float, int, complex, Decimal]
    total_value_vat: Union[float, int, complex, Decimal]
    total_value_gross: Union[float, int, complex, Decimal]
    transaction_currency_code: str
    invoice_currency_code: str
    invoice_exchange_rate_date: date
    invoice_exchange_rate: Union[float, int, complex, Decimal]
    invoice_amount_net: Union[float, int, complex, Decimal]
    invoice_amount_vat: Union[float, int, complex, Decimal]
    invoice_amount_gross: Union[float, int, complex, Decimal]
    vat_rate_reverse_charge: Union[float, int, complex, Decimal]
    invoice_amount_vat_reverse_charge: Union[float, int, complex, Decimal]
    arrival_seller_vatin_id: int
    departure_seller_vatin_id: int
    seller_vatin_id: int
