from flask_restx import Model, fields

from ..transaction import transaction_dto

account_dto = Model('account', {
    'id': fields.Integer(readonly=True),
    'given_id': fields.String,
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'created_on': fields.Date(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'channel_code': fields.String,
    'seller_firm_id': fields.Integer,
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True),
    'transactions': fields.List(fields.Nested(transaction_dto)),

})


account_sub_dto = Model('account_sub', {
    'public_id': fields.String(readonly=True),
    'given_id': fields.String,
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'created_on': fields.Date(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'channel_code': fields.String,
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True)
})
