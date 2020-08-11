from flask_restx import Model, fields

tag_dto = Model('tag', {
    'code': fields.String,

})
