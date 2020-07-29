from flask_restx import Model, fields
from ..schema_parent import user_dto, user_sub_dto, user_dto_admin
from ...business.seller_firm import seller_firm_sub_dto


tax_auditor_sub_dto = user_sub_dto.clone('tax_auditor_sub', {
    # 'key_accounts': fields.List(fields.Nested(seller_firm_sub_dto)),
    # 'len_key_accounts': fields.String(attribute=lambda x: len(x.key_accounts), readonly=True)
})


tax_auditor_dto = tax_auditor_sub_dto.clone('tax_auditor', {
    'confirmed': fields.Boolean(readonly=True),
    'confirmed_on': fields.Date(readonly=True),
    'email': fields.String,
    'employer_public_id': fields.String,
    'employer_name': fields.String,
    'avatar_hash': fields.String(readonly=True),
    'location': fields.String(readonly=True),
    'u_type': fields.String(readonly=True)
})


tax_auditor_dto_admin = tax_auditor_dto.clone('tax_auditor_admin', {
    'id': fields.Integer(readonly=True),
    # 'employer_id': fields.Integer,
    'location': fields.String
    # 'key_accounts': fields.List(fields.Nested(seller_firm_sub_dto)),
    # 'len_key_accounts': fields.String(attribute=lambda x: len(x.key_accounts), readonly=True)
})
