from flask_restx import Model, fields
from app.namespaces.account import account_sub_dto

channel_sub_dto = Model('channel_sub', {
    'code': fields.String,
    'name': fields.String,
    'platform_code': fields.String,
    'description': fields.String
})

channel_dto = channel_sub_dto.clone('channel', {
    'accounts': fields.List(fields.Nested(account_sub_dto))

})
