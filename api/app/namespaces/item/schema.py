from flask_restx import Model, fields

item_dto = Model('item', {
    'id': fields.Integer(readonly=True),
    'created_by': fields.Integer,
    'created_on': fields.DateTime,
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
