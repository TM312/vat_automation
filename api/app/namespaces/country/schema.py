from flask_restx import Model, fields

country_dto = Model('country', {
    'code': fields.String,
    'vat_country_code': fields.String,
    'name': fields.String,
    'valid_from': fields.DateTime,
    'valid_to': fields.DateTime,
    'currency_code': fields.String
})

country_sub_dto = Model('country_sub', {
    'code': fields.String,
    'vat_country_code': fields.String,
    'name': fields.String,
    'valid_from': fields.DateTime,
    'valid_to': fields.DateTime,
    'currency_code': fields.String
})

eu_dto = Model('eu', {
    'id': fields.String,
    'valid_from': fields.DateTime,
    'valid_to': fields.DateTime,
    'countries': fields.List(fields.Nested(country_sub_dto))
})
