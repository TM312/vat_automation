# from marshmallow import fields, Schema


# class TokenSchema(Schema):
#     """
#     Token Schema
#     """
#     #id = fields.Int(dump_only=True)
#     token = fields.Str(dump_only=True)
#     #iss = fields.Str(dump_only=True)
#     #exp = fields.DateTime(dump_only=True)
#     #iat = fields.DateTime(dump_only=True)
#     #sub = fields.Str(dump_only=True)
#     token_lifespan = fields.Int(load_only=True)

from flask_restx import Model, fields

auth_dto = Model('token', {
    'id': fields.Integer(readonly=True),
    'token': fields.String(readonly=True),
    'iss': fields.String(readonly=True),
    'sub': fields.String(readonly=True),
    'blacklisted_on': fields.String(readonly=True)
})
