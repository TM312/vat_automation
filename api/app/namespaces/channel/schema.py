from flask_restx import Model, fields
from app.namespaces.account import account_sub_dto

channel_dto = Model('channel', {
    'code': fields.String,
    'name': fields.String,
    'platform_code': fields.String,
    'description': fields.String,
    'accounts': fields.List(fields.Nested(account_sub_dto))

})
