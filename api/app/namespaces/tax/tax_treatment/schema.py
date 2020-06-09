from flask_restx import Model, fields


tax_treatment_dto = Model('tax_treatment', {
    'code': fields.String,
    'name': fields.String
    'description': fields.String
})
