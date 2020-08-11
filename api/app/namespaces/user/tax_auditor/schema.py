from flask_restx import Model, fields
from ..schema_parent import user_dto, user_sub_dto, user_dto_admin

tax_auditor_sub_dto = user_sub_dto.clone('tax_auditor_sub', {
})

seller_firm_sub_dto = Model('seller_firm_sub', {
    'public_id': fields.String(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'name': fields.String,
    'address': fields.String,
    'b_type': fields.String(readonly=True),
    'claimed': fields.Boolean(readonly=True),
    'establishment_country_code': fields.String,
    'establishment_country': fields.String(attribute=lambda x: x.establishment_country.name if x.establishment_country else None),
    'transaction_ready': fields.Boolean(readonly=True),
})



tax_auditor_dto = tax_auditor_sub_dto.clone('tax_auditor', {
    'key_accounts': fields.List(fields.Nested(seller_firm_sub_dto)),
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
    'employer_id': fields.Integer,
    'location': fields.String
})
