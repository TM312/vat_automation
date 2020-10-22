from flask_restx import Model, fields


vat_threshold_dto = Model('vat', {
    # 'id': fields.Integer,
    # 'valid_from': fields.Date,
    # 'valid_to': fields.Date,
    # 'country_code': fields.String,
    # 'tax_code_code': fields.String,
    # 'tax_rate_type_code': fields.String,
    # 'rate': fields.Float
})


vat_threshold_history_dto = Model('vat_threshold_history', {
    # 'public_id': fields.String(readonly=True),
    # 'valid_from': fields.Date,
    # 'valid_to': fields.Date,
    # 'comment': fields.String,
    # 'name': fields.String,
    # 'unit_cost_price_currency_code': fields.String,
    # 'unit_cost_price_net': fields.Float,
    # 'tags': fields.List(fields.Nested(tag_dto))
})
