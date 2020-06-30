from flask_restx import Model, fields

business_dto = Model('business', {
    'id': fields.Integer(readonly=True),
    'public_id': fields.String(readonly=True),
    'created_by': fields.String(attribute=lambda x: x.creator.name),
    'created_on': fields.Date(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'name': fields.String,
    'address': fields.String,
    'b_type': fields.String(readonly=True)
})

business_sub_dto = Model('business_sub', {
    'public_id': fields.String(readonly=True),
    'created_by': fields.String(attribute=lambda x: x.creator.name),
    'created_on': fields.Date(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'name': fields.String,
    'address': fields.String,
    'b_type': fields.String(readonly=True)
})
