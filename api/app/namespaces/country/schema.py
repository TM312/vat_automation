from flask_restx import Model, fields


country_sub_dto = Model('country_sub', {
    'code': fields.String,
    'vat_country_code': fields.String,
    'name': fields.String,
    'currency_code': fields.String
})

country_dto = country_sub_dto.clone('country', {
})

eu_dto = Model('eu', {
    'public_id': fields.String,
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'countries': fields.List(fields.Nested(country_sub_dto))
})

eu_admin_dto = eu_dto.clone('eu_admin', {
    'id': fields.Integer
})
