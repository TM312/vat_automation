from flask_restx import Model, fields

user_dto = Model('user', {
    'id': fields.Integer(readonly=True),
    'public_id': fields.String(readonly=True),
    'username': fields.String,
    'email': fields.String,
    'registered_on': fields.DateTime(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'role': fields.String(readonly=True),
    'password_hash': fields.String(readonly=True),
    'avatar_hash': fields.String(readonly=True),
    'confirmed': fields.Boolean(readonly=True),
    'confirmed_on': fields.DateTime(readonly=True),
    'location': fields.String(readonly=True),
    'last_seen': fields.DateTime(readonly=True),
    'password': fields.String,
    'u_type': fields.String
})

user_dto_admin = user_dto.clone('user_admin', {
    'employer_id': fields.Integer,
    'actions': fields.List(),
})

action_dto = Model('action', {
    'id': fields.Integer(readonly=True),
    'timestamp': fields.DateTime(readonly=True),
    'user_id': fields.Integer(readonly=True),
    'method_name': fields.String(readonly=True),
    'service_context': fields.String(readonly=True),
})
