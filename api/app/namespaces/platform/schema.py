from flask_restx import Model, fields

platform_dto = Model('platform', {
    'code': fields.String,
    'name': fields.String,
    #'channels': fields...,
    #'transaction_types_public': fields...
})
