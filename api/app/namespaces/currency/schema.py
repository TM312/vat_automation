from flask_restx import Model, fields

currency_dto = Model('currency', {
    'code': fields.String,
    'name': fields.String
})
