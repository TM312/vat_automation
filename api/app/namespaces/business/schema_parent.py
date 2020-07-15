from flask_restx import Model, fields


business_sub_dto = Model('business_sub', {
    'public_id': fields.String(readonly=True),
    'created_by': fields.String(attribute=lambda x: x.creator.name),
    'created_on': fields.Date(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'name': fields.String,
    'address': fields.String,
    'b_type': fields.String(readonly=True),
    'len_vat_numbers': fields.String(attribute=lambda x: len(x.vat_numbers), readonly=True),
})

business_dto = business_sub_dto.inherit('business', {})

business_admin_dto = business_dto.inherit('business_admin', {
    'id': fields.Integer(readonly=True)
})
