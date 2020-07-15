from flask_restx import Model, fields

from .. import business_dto
from ...user.tax_auditor import tax_auditor_sub_dto
from ..seller_firm import seller_firm_sub_dto





accounting_firm_dto = business_dto.inherit('accounting_firm', {
    'employees': fields.List(fields.Nested(tax_auditor_sub_dto)),
    'len_employees': fields.Integer(attribute=lambda x: len(x.employees), readonly=True),
    'clients': fields.List(fields.Nested(seller_firm_sub_dto))
})
