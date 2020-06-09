from flask_restx import Model, fields


vat_dto = Model('vat', {
    'id': fields.Integer,
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'country_code': fields.String,
    'tax_code_code': fields.String,
    'tax_rate_type_code': fields.String,
    'rate': fields.Float
})
