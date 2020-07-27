from flask_restx import Model, fields

from ..transaction import transaction_sub_dto
from ..transaction_input import transaction_input_sub_dto

account_sub_dto = Model('account_sub', {
    'public_id': fields.String(readonly=True),
    'given_id': fields.String,
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'created_on': fields.Date(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'channel_code': fields.String,

})


account_dto = account_sub_dto.clone('account', {
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True),
    'transaction_inputs': fields.List(fields.Nested(transaction_input_sub_dto)),
    # 'transactions': fields.List(fields.Nested(transaction_sub_dto))
})


account_admin_dto = account_dto.clone('account_admin', {
    'id': fields.Integer(readonly=True),
    'seller_firm_id': fields.Integer(readonly=True)
})
