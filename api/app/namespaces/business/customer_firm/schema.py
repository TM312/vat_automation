from flask_restx import fields

from .. import business_dto
from ...transaction import transaction_sub_dto

customer_firm_dto = business_dto.inherit('customer_firm', {
    'transactions': fields.List(fields.Nested(transaction_sub_dto))
})
