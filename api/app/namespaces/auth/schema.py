from flask_restx import Model, fields

auth_dto = Model('token', {
    'id': fields.Integer(readonly=True),
    'token': fields.String(readonly=True),
    'iss': fields.String(readonly=True),
    'sub': fields.String(readonly=True),
    'blacklisted_on': fields.String(readonly=True)
})
