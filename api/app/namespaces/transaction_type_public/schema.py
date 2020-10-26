from flask_restx import Model, fields

transaction_type_public_dto = Model('transaction_type_public', {
    'code': fields.String,
    'description': fields.String,
    'platform_code': fields.String,
    'transaction_type_code': fields.String
})
