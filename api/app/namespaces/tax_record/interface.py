from mypy_extensions import TypedDict
from typing import List, Dict
from datetime import date, datetime


class TaxRecordInterface(TypedDict, total=False):
    id: int
    public_id: str
    active: bool
    created_on: datetime
    created_by: int
    start_date: date
    end_date: date
    filename: str
    seller_firm_id: int
    tax_jurisdiction_code: str

class TaxRecordDictInterface(TypedDict, total=True):
    LOCAL_SALES: List[Dict]
    LOCAL_SALE_REVERSE_CHARGES: List[Dict]
    DISTANCE_SALES: List[Dict]
    NON_TAXABLE_DISTANCE_SALES: List[Dict]
    INTRA_COMMUNITY_SALES: List[Dict]
    EXPORTS: List[Dict]
    DOMESTIC_ACQUISITIONS: List[Dict]
    INTRA_COMMUNITY_ACQUISITIONS: List[Dict]


class TaxRecordBaseDictInterface(TypedDict, total=False):

    SELLER_FIRM_ID: str
    SELLER_FIRM_NAME: str
    SELLER_FIRM_ADDRESS: str
    SELLER_FIRM_ESTABLISHMENT_COUNTRY: str

    CREATED_BY: str
    ORIGINAL_FILENAME: str

    ACCOUNT_GIVEM_ID: str
    CHANNEL_CODE: str
    MARKETPLACE: str
    TRANSACTION_TYPE: str

    TRANSACTION_GIVEN_ID: str
    ACTIVITY_ID: str

    AMAZON_VAT_CALCULATION_SERVICE: bool
    CUSTOMER_RELATIONSHIP: str
    CUSTOMER_RELATIONSHIP_CHECKED: bool

    TAX_JURISDICTION_CODE: str

    TAX_TREATMENT_CODE: str

    TAX_DATE: date
    TAX_CALCULATION_DATE: date
    SHIPMENT_DATE: date

    ITEM_SKU: str
    ITEM_NAME: str
    ITEM_QUANTITY: int

    ITEM_TAX_CODE: str
    ITEM_TAX_RATE_TYPE: str

    ITEM_PRICE_NET: float
    ITEM_PRICE_DISCOUNT_NET: float
    ITEM_PRICE_TOTAL_NET: float

    SHIPMENT_PRICE_NET: float
    SHIPMENT_PRICE_DISCOUNT_NET: float
    SHIPMENT_PRICE_TOTAL_NET: float

    GIFT_WRAP_PRICE_NET: float
    GIFT_WRAP_PRICE_DISCOUNT_NET: float
    GIFT_WRAP_PRICE_TOTAL_NET: float

    ITEM_PRICE_VAT_RATE: float
    ITEM_PRICE_VAT: float
    ITEM_PRICE_DISCOUNT_VAT: float
    ITEM_PRICE_TOTAL_VAT: float

    SHIPMENT_PRICE_VAT_RATE: float
    SHIPMENT_PRICE_VAT: float
    SHIPMENT_PRICE_DISCOUNT_VAT: float
    SHIPMENT_PRICE_TOTAL_VAT: float

    GIFT_WRAP_PRICE_VAT_RATE: float
    GIFT_WRAP_PRICE_VAT: float
    GIFT_WRAP_PRICE_DISCOUNT_VAT: float
    GIFT_WRAP_PRICE_TOTAL_VAT: float

    TOTAL_VALUE_NET: float
    TOTAL_VALUE_VAT: float
    TOTAL_VALUE_GROSS: float

    ITEM_PRICE_GROSS: float
    ITEM_PRICE_DISCOUNT_GROSS: float
    ITEM_PRICE_TOTAL_GROSS: float

    SHIPMENT_PRICE_GROSS: float
    SHIPMENT_PRICE_DISCOUNT_GROSS: float
    SHIPMENT_PRICE_TOTAL_GROSS: float

    GIFT_WRAP_PRICE_GROSS: float
    GIFT_WRAP_PRICE_DISCOUNT_GROSS: float
    GIFT_WRAP_PRICE_TOTAL_GROSS: float

    DEPARTURE_CITY: str
    DEPARTURE_COUNTRY: str
    DEPARTURE_POSTAL_CODE: str

    ARRIVAL_CITY: str
    ARRIVAL_COUNTRY: str
    ARRIVAL_POSTAL_CODE: str

    DEPARTURE_SELLER_VAT_NUMBER_COUNTRY: str
    DEPARTURE_SELLER_VAT_NUMBER: str
    DEPARTURE_SELLER_VAT_VALID: bool
    DEPARTURE_SELLER_VAT_CHECKED_DATE: date

    ARRIVAL_SELLER_VAT_NUMBER_COUNTRY: str
    ARRIVAL_SELLER_VAT_NUMBER: str
    ARRIVAL_SELLER_VAT_VALID: bool
    ARRIVAL_SELLER_VAT_CHECKED_DATE: date

    SELLER_VAT_NUMBER_COUNTRY: str
    SELLER_VAT_NUMBER: str
    SELLER_VAT_VALID: bool
    SELLER_VAT_CHECKED_DATE: date

    CUSTOMER_FIRM_VAT_NUMBER_COUNTRY: str
    CUSTOMER_FIRM_VAT_NUMBER: str
    CUSTOMER_FIRM_VAT_VALID: bool
    CUSTOMER_FIRM_VAT_CHECKED_DATE: date

    INVOICE_AMOUNT_NET: float
    INVOICE_AMOUNT_VAT: float
    INVOICE_AMOUNT_GROSS: float

    INVOICE_NUMBER: str
    INVOICE_CURRENCY: str
    INVOICE_EXCHANGE_RATE: str
    INVOICE_EXCHANGE_RATE_DATE: str
    INVOICE_URL: str

    ARRIVAL_ADDRESS: str
    SUPPLIER_NAME: str
    SUPPLIER_VAT_NUMBER: str

class LOCAL_SALES_DictInterface(TaxRecordBaseDictInterface):
    pass


class LOCAL_SALE_REVERSE_CHARGES_DictInterface(TaxRecordBaseDictInterface):
    VAT_RATE_REVERSE_CHARGE: float
    INVOICE_AMOUNT_VAT_REVERSE_CHARGE: float


class DISTANCE_SALES_DictInterface(TaxRecordBaseDictInterface):
    pass


class NON_TAXABLE_DISTANCE_SALES_DictInterface(TaxRecordBaseDictInterface):
    pass


class INTRA_COMMUNITY_SALES_DictInterface(TaxRecordBaseDictInterface):
    pass


class EXPORTS_DictInterface(TaxRecordBaseDictInterface):
    pass


class DOMESTIC_ACQUISITIONS_DictInterface(TaxRecordBaseDictInterface):
    pass


class INTRA_COMMUNITY_ACQUISITIONS_DictInterface(TaxRecordBaseDictInterface):
    pass
