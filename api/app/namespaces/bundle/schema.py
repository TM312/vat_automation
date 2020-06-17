from flask_restx import Model, fields


bundle_dto = Model('bundle', {
    'id': fields.Integer(readonly=True),
})
