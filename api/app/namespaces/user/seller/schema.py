from flask_restx import Model, fields

user_dto = Model('user', {
    'id': fields.Integer(readonly=True),
    'public_id': fields.String(readonly=True),
    'email': fields.String(),
    'company_name': fields.String(),
    'registered_on': fields.DateTime(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'role': fields.String(readonly=True),
    'claimed': fields.Boolean(readonly=True),
    'password_hash': fields.String(readonly=True),
    'avatar_hash': fields.String(readonly=True),
    'confirmed': fields.Boolean(readonly=True),
    'confirmed_on': fields.DateTime(readonly=True),
    'location': fields.String(readonly=True),
    'last_seen': fields.DateTime(readonly=True),
    'tax_auditor_company': fields.String(),
    'tax_auditor_seller_id': fields.String(),
    'password': fields.String()#,
    # 'tax_records': fields.List(fields.String),
    # 'clients': fields.List(fields.String)
})


employer
