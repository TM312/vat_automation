from flask_restx import Model, fields


vatin_dto = Model('vatin', {
    'id': fields.Integer,
    'created_on': fields.DateTime,
    'modified_at': fields.DateTime,
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'initial_tax_date': fields.Date,
    '_country_code': fields.String,
    '_number': fields.String,
    'valid': fields.Boolean,
    'name': fields.String,
    'address': fields.String,
    'business_id': fields.Integer,
    'business_name': fields.String(attribute=lambda x: x.business.name)
})

vatin_verify_dto = Model('vatin_verify', {
    'status': fields.String,
    'verified': fields.Boolean,
    'country_code': fields.String,
    'number': fields.String

})

vatin_validate_dto = Model('vatin_validate', {
    'status': fields.String,
    'country_code': fields.String,
    'number': fields.String,
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'valid': fields.Boolean,
    'name': fields.String,
    'address': fields.String
})

vatin_sub_dto = Model('vatin_sub', {
    'created_on': fields.DateTime,
    'modified_at': fields.DateTime,
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'initial_tax_date': fields.Date,
    '_country_code': fields.String,
    '_number': fields.String,
    'valid': fields.Boolean,
    'name': fields.String,
    'address': fields.String,
    'business_name': fields.String(attribute=lambda x: x.business.name)
})
