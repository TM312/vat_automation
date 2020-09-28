from flask_restx import Model, fields
from app.namespaces.tax.vat import vat_dto


tax_rate_type_sub_dto = Model('tax_rate_type_sub', {
    'code': fields.String,
    'name': fields.String,
    'description': fields.String
})

tax_rate_type_dto = tax_rate_type_sub_dto.inherit('tax_rate_type', {
    'vats': fields.List(fields.Nested(vat_dto))
})
