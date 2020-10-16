from flask_restx import Model, fields
from app.namespaces.utils import transaction_notification_dto
from app.namespaces.tax.vatin import vatin_sub_dto


transaction_type_dto = Model('transaction_type', {
    'code': fields.String,
    'description': fields.String
})

transaction_sub_dto = Model('transaction_sub', {
    'public_id': fields.String(readonly=True),
    'tax_jurisdiction_code': fields.String,
    'arrival_country_code': fields.String,
    'departure_country_code': fields.String,
    'arrival_country': fields.String(attribute=lambda x: x.arrival_country.name, readonly=True),
    'departure_country': fields.String(attribute=lambda x: x.departure_country.name, readonly=True),
    'type_code': fields.String,
    'tax_treatment_code': fields.String,
    'tax_date': fields.Date,
    'tax_calculation_date': fields.Date,
    'transaction_currency_code': fields.String(readonly=True),
    'transaction_input_public_id': fields.String(attribute=lambda x: x.transaction_input.public_id, readonly=True),
    'transaction_input_given_id': fields.String(attribute=lambda x: x.transaction_input.given_id, readonly=True),
    'transaction_input_activity_id': fields.String(attribute=lambda x: x.transaction_input.activity_id, readonly=True),
})

transaction_dto = transaction_sub_dto.clone('transaction', {
    'notifications': fields.List(fields.Nested(transaction_notification_dto)),
    'created_on': fields.DateTime,
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True),
    # 'account_public_id': fields.String(attribute=lambda x: x.account.public_id, readonly=True),
    # 'item_public_id': fields.String(attribute=lambda x: x.item.public_id, readonly=True),
    'amazon_vat_calculation_service': fields.Boolean,
    'customer_relationship_checked': fields.Boolean,
    'customer_relationship': fields.String,
    'customer_vatin': fields.List(fields.Nested(vatin_sub_dto)),
    'supplier_relationship': fields.String,
    'supplier_vatin': fields.List(fields.Nested(vatin_sub_dto)),
    'item_tax_code_code': fields.String,
    'item_tax_rate_type_code': fields.String,
    'shipment_tax_rate_type_code': fields.String,
    'gift_wrap_tax_rate_type_code': fields.String,
    'item_price_net': fields.Float,
    'item_price_discount_net': fields.Float,
    'item_price_total_net': fields.Float,
    'shipment_price_net': fields.Float,
    'shipment_price_discount_net': fields.Float,
    'shipment_price_total_net': fields.Float,
    'gift_wrap_price_net': fields.Float,
    'gift_wrap_price_discount_net': fields.Float,
    'gift_wrap_price_total_net': fields.Float,
    'item_price_vat_rate': fields.Float,
    'item_price_vat': fields.Float,
    'item_price_discount_vat': fields.Float,
    'item_price_total_vat': fields.Float,
    'shipment_price_vat_rate': fields.Float,
    'shipment_price_vat': fields.Float,
    'shipment_price_discount_vat': fields.Float,
    'shipment_price_total_vat': fields.Float,
    'gift_wrap_price_vat_rate': fields.Float,
    'gift_wrap_price_vat': fields.Float,
    'gift_wrap_price_discount_vat': fields.Float,
    'gift_wrap_price_total_vat': fields.Float,
    'total_value_net': fields.Float,
    'total_value_vat': fields.Float,
    'total_value_gross': fields.Float,
    'transaction_currency_code': fields.String,
    'invoice_currency': fields.String(attribute=lambda x: x.invoice_currency.name, readonly=True),
    'invoice_currency_code': fields.String,
    'invoice_exchange_rate_date': fields.Date,
    'invoice_exchange_rate': fields.Float,
    'invoice_amount_net': fields.Float,
    'invoice_amount_vat': fields.Float,
    'invoice_amount_gross': fields.Float,
    'reverse_charge_vat_rate': fields.Float,
    'invoice_amount_reverse_charge_vat': fields.Float,
    'arrival_seller_vatin': fields.String(attribute=lambda x: '{}-{}'.format(x.arrival_seller_vatin.country_code, x.arrival_seller_vatin.number) if x.arrival_seller_vatin else None, readonly=True),
    'departure_seller_vatin': fields.String(attribute=lambda x: '{}-{}'.format(x.departure_seller_vatin.country_code, x.departure_seller_vatin.number) if x.departure_seller_vatin else None, readonly=True),
    'seller_vatin': fields.String(attribute=lambda x: '{}-{}'.format(x.seller_vatin.country_code, x.seller_vatin.number) if x.seller_vatin else None, readonly=True)
})


transaction_admin_dto = transaction_dto.clone('transaction_admin', {
    'id': fields.Integer(readonly=True),
    'account_id': fields.Integer,
    'transaction_input_id': fields.Integer,
    'item_id': fields.Integer,
    'customer_id': fields.Integer,
})
