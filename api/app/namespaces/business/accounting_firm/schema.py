from flask_restx import Model, fields

from .. import business_sub_dto



tax_auditor_sub_dto = Model('tax_auditor_sub', {
    'public_id': fields.String(readonly=True),
    'registered_on': fields.Date(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'last_seen': fields.DateTime(readonly=True),
    'role': fields.String(readonly=True),
    'name': fields.String,
    'initials': fields.String,
})

seller_firm_sub_dto = business_sub_dto.clone('seller_firm_sub', {
    'claimed': fields.Boolean(readonly=True),
    'establishment_country_code': fields.String,
    'transaction_ready': fields.Boolean(readonly=True),
})


accounting_firm_sub_dto = business_sub_dto.clone('accounting_firm_sub', {
})

accounting_firm_dto = accounting_firm_sub_dto.clone('accounting_firm', {
    'employees': fields.List(fields.Nested(tax_auditor_sub_dto)),
    'clients': fields.List(fields.Nested(seller_firm_sub_dto))
})
