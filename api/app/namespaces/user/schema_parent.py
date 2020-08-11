from flask_restx import Model, fields



user_sub_dto = Model('user_sub', {
    'public_id': fields.String(readonly=True),
    'registered_on': fields.Date(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'last_seen': fields.DateTime(readonly=True),
    'role': fields.String(readonly=True),
    'name': fields.String,
    'initials': fields.String,
})


user_dto = user_sub_dto.clone('user', {
    'confirmed': fields.Boolean(readonly=True),
    'confirmed_on': fields.Date(readonly=True),
    'email': fields.String,
    'employer_public_id': fields.String,
    'employer_name': fields.String,
    'avatar_hash': fields.String(readonly=True),
    'location': fields.String(readonly=True),
    'u_type': fields.String(readonly=True)

    # 'password_hash': fields.String(readonly=True),
    # 'password': fields.String,
})



user_dto_admin = user_dto.clone('user_admin', {
    'id': fields.Integer(readonly=True),
    'employer_id': fields.Integer,
})





action_dto = Model('action', {
    'id': fields.Integer(readonly=True),
    'timestamp': fields.DateTime(readonly=True),
    'user_id': fields.Integer(readonly=True),
    'method_name': fields.String(readonly=True),
    'service_context': fields.String(readonly=True)
})
