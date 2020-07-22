from flask_restx import Model, fields

transaction_type_dto = Model('transaction_type', {
    'code': fields.String,
    'description': fields.String
})

transaction_sub_dto = Model('transaction_sub', {
    'tax_jurisdiction': fields.String(attribute=lambda x: x.tax_jurisdiction.name, readonly=True),
    'arrival_country': fields.String(attribute=lambda x: x.arrival_country.name, readonly=True),
    'departure_country': fields.String(attribute=lambda x: x.departure_country.name, readonly=True),
    'type_code': fields.String,
    'tax_treatment_code': fields.String,
    'tax_date': fields.Date,
    'tax_calculation_date': fields.Date,
    'transaction_currency': fields.String(attribute=lambda x: x.transaction_currency.name, readonly=True),
})

transaction_dto = transaction_sub_dto.inherit('transaction', {
    'created_on': fields.DateTime,
    'transaction_input_public_id': fields.String(attribute=lambda x: x.transaction_input.public_id, readonly=True),
    # 'account_public_id': fields.String(attribute=lambda x: x.account.public_id, readonly=True),
    # 'item_public_id': fields.String(attribute=lambda x: x.item.public_id, readonly=True),
    'amazon_vat_calculation_service': fields.Boolean,
    'customer_relationship_checked': fields.Boolean,
    'customer_relationship': fields.String,
    'customer_firm_public_id': fields.String(attribute=lambda x: x.customer_firm.public_id if x.customer_firm else None, readonly=True),
    'customer_firm_name': fields.String(attribute=lambda x: x.customer_firm.name if x.customer_firm else None, readonly=True),
    'customer_firm_vatin': fields.String(attribute=lambda x: '{}-{}'.format(x.customer_firm_vatin.country_code, x.customer_firm_vatin.number) if x.customer_firm_vatin else None, readonly=True),
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
    'vat_rate_reverse_charge': fields.Float,
    'invoice_amount_vat_reverse_charge': fields.Float,
    'arrival_seller_vatin': fields.String(attribute=lambda x: '{}-{}'.format(x.arrival_seller_vatin.country_code, x.arrival_seller_vatin.number) if x.arrival_seller_vatin else None, readonly=True),
    'departure_seller_vatin': fields.String(attribute=lambda x: '{}-{}'.format(x.departure_seller_vatin.country_code, x.departure_seller_vatin.number) if x.departure_seller_vatin else None, readonly=True),
    'seller_vatin': fields.String(attribute=lambda x: '{}-{}'.format(x.seller_vatin.country_code, x.seller_vatin.number) if x.seller_vatin else None, readonly=True)
})


transaction_admin_dto = transaction_dto.inherit('transaction_admin', {
    'id': fields.Integer(readonly=True),
    'account_id': fields.Integer,
    'transaction_input_id': fields.Integer,
    'item_id': fields.Integer,
    'customer_firm_id': fields.Integer,
})
