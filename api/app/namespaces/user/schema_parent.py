from flask_restx import Model, fields

user_dto = Model('user', {
    'id': fields.Integer(readonly=True),
    'public_id': fields.String(readonly=True),
    'registered_on': fields.DateTime(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'confirmed': fields.Boolean(readonly=True),
    'confirmed_on': fields.DateTime(readonly=True),
    'last_seen': fields.DateTime(readonly=True),
    'role': fields.String(readonly=True),
    'name': fields.String,
    'email': fields.String,
    'password_hash': fields.String(readonly=True),
    'avatar_hash': fields.String(readonly=True),
    'location': fields.String(readonly=True),
    'password': fields.String,
    'u_type': fields.String(readonly=True)
})

user_dto_admin = user_dto.inherit('user_admin', {
    # 'id': fields.Integer(readonly=True),
    'employer_id': fields.Integer,
    'location': fields.String
})


action_dto = Model('action', {
    'id': fields.Integer(readonly=True),
    'timestamp': fields.DateTime(readonly=True),
    'user_id': fields.Integer(readonly=True),
    'method_name': fields.String(readonly=True),
    'service_context': fields.String(readonly=True)
})
