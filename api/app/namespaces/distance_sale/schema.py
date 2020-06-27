from flask_restx import Model, fields

distance_sale_dto = Model('distance_sale', {
    'id': fields.Integer,
    'created_on': fields.Date,
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'original_filename': fields.String,
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'platform_code': fields.String,
    'platform': fields.String(attribute=lambda x: x.platform.name, readonly=True),
    'seller_firm_id': fields.Integer,
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True),
    'arrival_country_code': fields.String,
    'arrival_country': fields.String(attribute=lambda x: x.arrival_country.name, readonly=True),
    'active': fields.Boolean
})
