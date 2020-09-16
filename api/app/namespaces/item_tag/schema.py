from flask_restx import Model, fields

item_tag_dto = Model('item_tag', {
    'name': fields.String,

})
