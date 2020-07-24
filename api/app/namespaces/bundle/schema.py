from flask_restx import Model, fields
from ..transaction_input import transaction_input_sub_dto


bundle_sub_dto = Model('bundle_sub', {
    'public_id': fields.String(readonly=True)
})

bundle_dto = bundle_sub_dto.inherit('bundle', {
    'transaction_inputs': fields.List(fields.Nested(transaction_input_sub_dto))
})

bundle_admin_dto = bundle_dto.inherit('bundle_admin', {
    'id': fields.Integer(readonly=True)
})
