from flask_restx import Model, fields

accounting_firm_dto = Model('business', {
    'id': fields.Integer(readonly=True),
    'public_id': fields.String(readonly=True),
    'company_name': fields.String(),
    'logo_image_name': fields.String(),
    'registered_on': fields.DateTime(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'type': fields.String()
    'employees': fields.List(fields.String),
    'clients': fields.List(fields.String)
})
