from flask_restx import Model, fields

user_tag_dto = Model('user_tag', {
    'name': fields.String,

})
