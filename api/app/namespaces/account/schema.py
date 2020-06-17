from flask_restx import Model, fields


account_dto = Model('account', {
    'id': fields.Integer(readonly=True),
    'given_id': fields.String,
    'created_by': fields.Integer(readonly=True),
    'created_on': fields.DateTime(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'channel_code': fields.String,
    'seller_firm_id': fields.Integer,
})
