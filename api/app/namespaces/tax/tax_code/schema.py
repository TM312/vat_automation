from flask_restx import Model, fields


tax_code_dto = Model('tax_code', {
    'code': fields.String,
    'description': fields.String
})
