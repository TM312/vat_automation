from flask_restx import Model, fields



business_sub_dto = Model('business_sub', {
    'public_id': fields.String(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'name': fields.String,
    'address': fields.String,
    'b_type': fields.String(readonly=True),
})


business_dto = business_sub_dto.clone('business', {
    'created_by': fields.String(attribute=lambda x: x.creator.name if x.created_by else None),
    'created_on': fields.Date(readonly=True),
})



business_admin_dto = business_dto.clone('business_admin', {
    'id': fields.Integer(readonly=True)
})
