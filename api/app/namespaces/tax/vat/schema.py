from flask_restx import Model, fields

vat_history_dto = Model('vat_history', {
    'public_id': fields.String(readonly=True),
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'comment': fields.String,
    #mirrored attributes
    'country_code': fields.String,
    'tax_code_code': fields.String,
    'tax_rate_type_code': fields.String,
    'rate': fields.Float
})


vat_sub_dto = Model('vat', {
    'public_id': fields.String(readonly=True),
    'country_code': fields.String,
    'tax_code_code': fields.String,
    'tax_rate_type_code': fields.String,
    'rate': fields.Float
})


vat_dto = vat_sub_dto.clone('vat', {
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'created_on': fields.Date,
    'modified_at': fields.Date,
    'vat_history': fields.List(fields.Nested(vat_history_dto))
})

vat_admin_dto = vat_dto.clone('vat_admin', {
    'id': fields.Integer
})
