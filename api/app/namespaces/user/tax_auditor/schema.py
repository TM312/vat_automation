from flask_restx import Model, fields
from .. import user_dto, user_dto_admin


tax_auditor_dto = user_dto.clone('tax_auditor', {
    'employer': fields.String,
    'tax_record_countries': fields.List(),
    'key_accounts': fields.List()
})

tax_auditor_dto_admin = user_dto_admin.clone('tax_auditor_admin', {
    'employer': fields.String,
    'tax_record_countries': fields.List(),
    'key_accounts': fields.List()
})
