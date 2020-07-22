from flask_restx import Model, fields
from ..account import account_sub_dto

channel_dto = Model('channel', {
    'id': fields.Integer(readonly=True),
    'code': fields.String,
    'name': fields.String,
    'platform_code': fields.String,
    'description': fields.String,
    'accounts': fields.List(fields.Nested(account_sub_dto))

})
