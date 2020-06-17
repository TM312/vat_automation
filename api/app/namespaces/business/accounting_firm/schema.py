from flask_restx import fields

from .. import business_dto
from ..seller_firm import seller_firm_dto
from ...user.tax_auditor import tax_auditor_dto


accounting_firm_dto = business_dto.inherit('accounting_firm', {
    'employees': fields.List(fields.Nested(tax_auditor_dto)),
    'clients': fields.List(fields.Nested(seller_firm_dto))
})
