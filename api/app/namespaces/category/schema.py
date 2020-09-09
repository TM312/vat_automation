import json
from flask_restx import Model, fields


category_dto = Model('category', {
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'created_on': fields.Date,
    'business': fields.String(attribute=lambda x: x.business.name, readonly=True)
})
