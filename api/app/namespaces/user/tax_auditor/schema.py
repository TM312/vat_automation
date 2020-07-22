from flask_restx import Model, fields
from ..schema_parent import user_dto, user_sub_dto, user_dto_admin
from ...business.seller_firm import seller_firm_sub_dto


tax_auditor_sub_dto = user_sub_dto.inherit('tax_auditor_sub', {
    'key_accounts': fields.List(fields.Nested(seller_firm_sub_dto)),
    'len_key_accounts': fields.String(attribute=lambda x: len(x.key_accounts), readonly=True)
})


tax_auditor_dto = user_dto.inherit('tax_auditor', {
    'key_accounts': fields.List(fields.Nested(seller_firm_sub_dto)),
    'len_key_accounts': fields.String(attribute=lambda x: len(x.key_accounts), readonly=True)
})


tax_auditor_dto_admin = user_dto_admin.inherit('tax_auditor_admin', {
    'key_accounts': fields.List(fields.Nested(seller_firm_sub_dto)),
    'len_key_accounts': fields.String(attribute=lambda x: len(x.key_accounts), readonly=True)
})
