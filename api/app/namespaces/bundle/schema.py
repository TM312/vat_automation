from flask_restx import Model, fields
from ..transaction_input import transaction_input_dto


bundle_dto = Model('bundle', {
    'id': fields.Integer(readonly=True),
    'transaction_inputs': fields.List(fields.Nested(transaction_input_dto))
})
