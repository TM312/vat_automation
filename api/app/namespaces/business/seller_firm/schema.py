from flask_restx import Model, fields
from ..schema_parent import business_dto

seller_firm_dto = business_dto.inherit('seller_firm', {
    'claimed': fields.Boolean(readonly=True),
    'establishment_country_code': fields.String,
    'accounting_firm_id': fields.String,
    'accounting_firm_client_id': fields.String
})
