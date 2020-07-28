from flask_restx import Model, fields

from .. import business_sub_dto
from ...user.tax_auditor import tax_auditor_sub_dto
from ..seller_firm import seller_firm_sub_dto


accounting_firm_sub_dto = business_sub_dto.clone('accounting_firm_sub', {
    'len_employees': fields.Integer(readonly=True),
    'len_clients': fields.Integer(readonly=True)
})

accounting_firm_dto = accounting_firm_sub_dto.clone('accounting_firm', {
    'employees': fields.List(fields.Nested(tax_auditor_sub_dto)),
    'clients': fields.List(fields.Nested(seller_firm_sub_dto))
})
