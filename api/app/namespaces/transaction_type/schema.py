from flask_restx import Model, fields

transaction_type_dto = Model('transaction_type', {
    'code': fields.String,
    #'name': fields.String,
    'description': fields.String
})
