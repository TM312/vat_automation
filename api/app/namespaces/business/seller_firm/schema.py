from flask_restx import Model, fields
from ..schema_parent import business_dto

seller_firm_dto = business_dto.inherit('seller_firm', {
    'claimed': fields.Boolean(readonly=True),
    'establishment_country_code': fields.String,
    'establishment_country': fields.String(attribute=lambda x: x.establishment_country.name),
    'accounting_firm_id': fields.String,
    'accounting_firm_name': fields.String(attribute=lambda x: x.accounting_firm.name),
    'accounting_firm_client_id': fields.String,
    # 'items': fields.List(fields.Nested('app.namespaces.item.item_dto'))
})
