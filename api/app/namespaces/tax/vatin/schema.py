from flask_restx import Model, fields


vatin_verify_dto = Model('vatin_verify', {
    'status': fields.String(readonly=True),
    'verified': fields.Boolean(readonly=True),
    'country_code': fields.String,
    'number': fields.String
})

vatin_validate_dto = vatin_verify_dto.inherit('vatin_validate', {
    'request_data': fields.Date,
    'valid': fields.Boolean,
    'name': fields.String,
    'address': fields.String
})

vatin_sub_dto = vatin_validate_dto.inherit('vatin_sub', {
    'public_id': fields.String(readonly=True),
    'created_on': fields.DateTime,
    'modified_at': fields.DateTime,
    'valid_from': fields.Date,
    'valid_to': fields.Date(readonly=True),
    'initial_tax_date': fields.Date,
    'business_name': fields.String(attribute=lambda x: x.business.name)
})

vatin_dto = vatin_sub_dto.inherit('vatin', {
})

vatin_admin_dto = vatin_sub_dto.inherit('vatin_admin', {
    'id': fields.Integer,
    'business_id': fields.Integer,

})
