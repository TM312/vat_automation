from flask_restx import Model, fields


channel_dto = Model('channel', {
    'id': fields.Integer(readonly=True),
    'code': fields.String,
    'name': fields.String,
    'platform_code': fields.String,
    'description': fields.String
})
