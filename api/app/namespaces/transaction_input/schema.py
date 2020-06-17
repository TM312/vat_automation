from flask_restx import Model, fields

from ..transaction import transaction_dto
from ..utils import transaction_notification_dto

transaction_input_dto = Model('transaction_input', {
    'id': fields.Integer(readonly=True),
    'original_filename': fields.String,
    'bundle_id': fields.Integer,
    'created_on': fields.DateTime,
    'created_by': fields.Integer,
    'processed': fields.Boolean,
    'processed_on': fields.DateTime,
    'transactions': fields.List(fields.Nested(transaction_dto)),
    'notifications': fields.List(fields.Nested(transaction_notification_dto)),
    'account_given_id': fields.String,
    'public_activity_period': fields.String,
    'channel_code': fields.String,
    'marketplace': fields.String,
    'transaction_type_public_code': fields.String,
    'given_id': fields.String,
    'activity_id': fields.String,
    'shipment_date': fields.Date,
    'arrival_date': fields.Date,
    'complete_date': fields.Date,
    'item_sku': fields.String,
    'item_name': fields.String,
    'item_manufacture_country': fields.String,
    'item_quantity': fields.Integer,
    'item_weight_kg': fields.Float,
    'item_weight_kg_total': fields.Float,
    'item_price_discount_gross': fields.Float,
    'item_price_gross': fields.Float,
    'item_price_total_gross': fields.Float,
    'shipment_price_discount_gross': fields.Float,
    'shipment_price_gross': fields.Float,
    'shipment_price_total_gross': fields.Float,
    'sale_total_value_gross': fields.Float,
    'gift_wrap_price_discount_gross': fields.Float,
    'gift_wrap_price_gross': fields.Float,
    'gift_wrap_price_total_gross': fields.Float,
    'currency_code': fields.String,
    'departure_country_code': fields.String,
    'departure_postal_code': fields.String,
    'departure_city': fields.String,
    'arrival_country_code': fields.String,
    'arrival_postal_code': fields.String,
    'arrival_city': fields.String,
    'arrival_address': fields.String,
    'shipment_mode': fields.String,
    'shipment_conditions': fields.String,
    'invoice_number': fields.String,
    'invoice_url': fields.String,
    'customer_firm_name': fields.String,
    'customer_firm_vat_number': fields.String,
    'customer_firm_vat_number_country_code': fields.String,
    'supplier_vat_number': fields.String,
    'supplier_name': fields.String,
    'check_tax_calculation_date': fields.Date,
    'check_unit_cost_price_net': fields.Float,
    'check_item_price_discount_net': fields.Float,
    'check_item_price_discount_vat': fields.Float,
    'check_item_price_net': fields.Float,
    'check_item_price_vat': fields.Float,
    'check_item_price_total_net': fields.Float,
    'check_item_price_total_vat': fields.Float,
    'check_item_price_vat': fields.Float,
    'check_item_price_vat_rate': fields.Float,
    'check_shipment_price_discount_net': fields.Float,
    'check_shipment_price_discount_vat': fields.Float,
    'check_shipment_price_net': fields.Float,
    'check_shipment_price_vat': fields.Float,
    'check_shipment_price_total_net': fields.Float,
    'check_shipment_price_total_vat': fields.Float,
    'check_shipment_price_vat': fields.Float,
    'check_shipment_price_vat_rate': fields.Float,
    'check_sale_total_value_net': fields.Float,
    'check_sale_total_value_vat': fields.Float,
    'check_gift_wrap_price_discount_net': fields.Float,
    'check_gift_wrap_price_discount_vat': fields.Float,
    'check_gift_wrap_price_net': fields.Float,
    'check_gift_wrap_price_vat': fields.Float,
    'check_gift_wrap_price_total_net': fields.Float,
    'check_gift_wrap_price_total_vat': fields.Float,
    'check_gift_wrap_price_tax_rate': fields.Float,
    'check_item_tax_code_code': fields.String,
    'check_departure_seller_vat_country_code': fields.String,
    'check_departure_seller_vat_number': fields.String,
    'check_arrival_seller_vat_country_code': fields.String,
    'check_arrival_seller_vat_number': fields.String,
    'check_seller_vat_country_code': fields.String,
    'check_seller_vat_number': fields.String,
    'check_tax_calculation_imputation_country': fields.String,
    'check_tax_jurisdiction': fields.String,
    'check_tax_jurisdiction_level': fields.String,
    'check_invoice_amount_vat': fields.Float,
    'check_invoice_currency_code': fields.String,
    'check_invoice_exchange_rate': fields.Float,
    'check_invoice_exchange_rate_date': fields.Date,
    'check_export': fields.Boolean
})
