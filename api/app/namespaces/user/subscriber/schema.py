from flask_restx import Model, fields
from ..schema_parent import user_dto, user_sub_dto, user_dto_admin

subscriber_sub_dto = user_sub_dto.clone('subscriber_sub', {
    'email': fields.String,
    'name': fields.String,
    'u_type_indicated': fields.String,
    'feedback': fields.String
})


subscriber_dto = Model('subscriber', {
    'email': fields.String
})


subscriber_dto_admin = user_dto.clone('subscriber_admin', {
    'id': fields.Integer(readonly=True)
})
