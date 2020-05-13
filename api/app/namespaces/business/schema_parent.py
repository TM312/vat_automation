from flask_restx import Model, fields

business_dto = Model('business', {
    'id': fields.Integer(readonly=True),
    'public_id': fields.String(readonly=True),
    'company_name': fields.String,
    'logo_image_name': fields.String,
    'created_on': fields.DateTime(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'b_type': fields.String
})
