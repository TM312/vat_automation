from flask_restx import Model, fields

distance_sale_dto = Model('distance_sale', {
    'id': fields.Integer,
    'created_on': fields.DateTime,
    'created_by': fields.Integer,
    'original_filename': fields.String,
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'platform_code': fields.String,
    'seller_firm_id': fields.Integer,
    'arrival_country_code': fields.String,
    'active': fields.Boolean
})
