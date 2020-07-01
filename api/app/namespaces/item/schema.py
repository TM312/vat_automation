from flask_restx import Model, fields

item_dto = Model('item', {
    'id': fields.Integer(readonly=True),
    'public_id': fields.String(readonly=True),
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'created_on': fields.Date,
    'original_filename': fields.String,
    'sku': fields.String,
    'seller_firm_id': fields.Integer,
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'brand_name': fields.String,
    'name': fields.String,
    'ean': fields.String,
    'asin': fields.String,
    'fnsku': fields.String,
    'weight_kg': fields.Float,
    'tax_code_code': fields.String,
    'unit_cost_price_currency_code': fields.String,
    'unit_cost_price_net': fields.Float
})


item_sub_dto = Model('item_sub', {
    'public_id': fields.String(readonly=True),
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'created_on': fields.Date,
    'original_filename': fields.String,
    'sku': fields.String,
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True),
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'brand_name': fields.String,
    'name': fields.String,
    'ean': fields.String,
    'asin': fields.String,
    'fnsku': fields.String,
    'weight_kg': fields.Float,
    'tax_code_code': fields.String,
    'unit_cost_price_currency_code': fields.String,
    'unit_cost_price_net': fields.Float
})
