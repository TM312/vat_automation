# This is a test for transaction #1

## Input Types:

String (str): 'This is a string'
Integer (int): 1, 2, 3, etc.
Float (float): 1.2, 1.452343, etc.
Boolean (bool): False, True
date (date): Schreib einfach als: 'YY-mm-dd'

Prices are being multiplied by 100 to be stored as integers.
Rates are being multuplied by 10'000 to be stored as integers.

Bzgl. "customer_relationship_checked": "True" genau dann, wenn es eine Vat Nummer der Customer Firm gibt. Sonst immer "False"
Bzgl. "customer_relationship": Entweder 'B2B' oder 'B2C'
Bzgl. "type code": Bezieht sich auf die Transaction Types. Deren Codes lauten entsprechend:
    'SALE',
    'REFUND',
    'ACQUISITION',
    'MOVEMENT',
    'INBOUND',

Country Codes sind 2-stellige ISO Codes, also zB DE für Deutschland

Tax Treatment Codes sind:
'LOCAL_SALE', 'LOCAL_SALE_REVERSE_CHARGE', 'DISTANCE_SALE', 'INTRA_COMMUNITY_SALE', 'EXPORT', 'LOCAL_ACQUISITION', 'INTRA_COMMUNITY_ACQUISITION', 'IMPORT'

Bzgl. Tax Rate Type Codes (zB. "item_tax_rate_type_code"): 'R', 'R2', 'Z', 'S'

## Test Output

type_code: str ==
amazon_vat_calculation_service: bool ==

customer_relationship_checked: bool ==
customer_relationship: str ==

tax_jurisdiction_code: str ==
arrival_country_code: str ==
departure_country_code: str ==
tax_treatment_code: str ==

tax_date: date ==
tax_calculation_date: date ==
item_tax_code_code: str ==
item_tax_rate_type_code: str ==
shipment_tax_rate_type_code: str ==
gift_wrap_tax_rate_type_code: str ==
_item_price_net: int ==                         #multiply by factor 100
_item_price_discount_net: int ==                        #multiply by factor 100
_item_price_total_net: int ==                       #multiply by factor 100
_shipment_price_net: int ==                         #multiply by factor 100
_shipment_price_discount_net: int ==                        #multiply by factor 100
_shipment_price_total_net: int ==                       #multiply by factor 100
_gift_wrap_price_net: int ==                        #multiply by factor 100
_gift_wrap_price_discount_net: int ==                       #multiply by factor 100
_gift_wrap_price_total_net: int ==                      #multiply by factor 100
_item_price_vat_rate: int ==                        #multiply by factor 100
_item_price_vat: int ==                         #multiply by factor 100
_item_price_discount_vat: int ==                        #multiply by factor 100
_item_price_total_vat: int ==                       #multiply by factor 100
_shipment_price_vat_rate: int ==                        #multiply by factor 100
_shipment_price_vat: int ==                         #multiply by factor 100
_shipment_price_discount_vat: int ==                        #multiply by factor 100
_shipment_price_total_vat: int ==                       #multiply by factor 100
_gift_wrap_price_vat_rate: int ==                       #multiply by factor 100
_gift_wrap_price_vat: int ==                        #multiply by factor 100
_gift_wrap_price_discount_vat: int ==                       #multiply by factor 100
_gift_wrap_price_total_vat: int ==                      #multiply by factor 100
_total_value_net: int ==                        #multiply by factor 100
_total_value_vat: int ==                        #multiply by factor 100
_total_value_gross: int ==                      #multiply by factor 100
transaction_currency_code: str ==
invoice_currency_code: str ==
invoice_exchange_rate_date: date ==
_invoice_exchange_rate: int ==                      #multiply by factor 100
_invoice_amount_net: int ==                         #multiply by factor 100
_invoice_amount_vat: int ==                         #multiply by factor 100
_invoice_amount_gross: int ==                       #multiply by factor 100
_vat_rate_reverse_charge: int ==                    #multiply by factor 10'000
_invoice_amount_vat_reverse_charge: int ==                      #multiply by factor 100



# To do Thomas:
seller_firm_id ==
item_id ==
notifications
transaction_input_id ==
