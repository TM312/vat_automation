import json
from flask_restx import Model, fields


vatin_verify_dto = Model('vatin_verify', {
    'status': fields.String(readonly=True),
    'verified': fields.Boolean(readonly=True),
    'country_code': fields.String,
    'number': fields.String
})

vatin_validate_dto = vatin_verify_dto.clone('vatin_validate', {
    'request_date': fields.Date,
    'valid': fields.Boolean,
    'name': fields.String,
    'address': fields.String
})

vatin_sub_dto = Model('vatin_sub', {
    'country_code': fields.String,
    'number': fields.String,
    'public_id': fields.String(readonly=True),
    'created_on': fields.DateTime,
    'modified_at': fields.DateTime,
    'request_date': fields.Date,
    'valid': fields.Boolean,
    'name': fields.String,
    'address': fields.String,
    'valid_from': fields.Date,
    'valid_to': fields.Date(readonly=True),
    'initial_tax_date': fields.Date,
})

vatin_dto = vatin_sub_dto.clone('vatin', {
    'business_name': fields.String(attribute=lambda x: x.business.name)
})

vatin_admin_dto = vatin_sub_dto.clone('vatin_admin', {
    'id': fields.Integer,
    'business_id': fields.Integer,

})


class VatinSchemaSocket:

    @staticmethod
    def get_vatin_sub(vatin):
        vatin_as_dict = {
            'country_code': vatin.country_code,
            'number': vatin.number,
            'public_id': vatin.public_id,
            'created_on': str(vatin.created_on),
            'modified_at': str(vatin.modified_at),
            'request_date': str(vatin.request_date),
            'valid': vatin.valid,
            'name': vatin.name,
            'address': vatin.address,
            'valid_from': str(vatin.valid_from),
            'valid_to': str(vatin.valid_to),
            'initial_tax_date': str(vatin.initial_tax_date)
        }
        return vatin_as_dict
