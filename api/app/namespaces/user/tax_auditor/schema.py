from flask_restx import Model, fields
from ..schema_parent import user_dto, user_dto_admin


tax_auditor_dto = user_dto.clone('tax_auditor', {})

tax_auditor_dto_admin = user_dto_admin.clone('tax_auditor_admin', {})
