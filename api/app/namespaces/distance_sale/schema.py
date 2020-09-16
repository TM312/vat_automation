#import json
from flask_restx import Model, fields


distance_sale_history_dto = Model('distance_sale_history', {
    'public_id': fields.String(readonly=True),
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'arrival_country_code': fields.String,
    'active': fields.Boolean,
    'comment': fields.String
})

distance_sale_sub_dto = Model('distance_sale_sub', {
    'public_id': fields.String(readonly=True),
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'arrival_country_code': fields.String,
    'arrival_country': fields.String(attribute=lambda x: x.arrival_country.name, readonly=True),
    'active': fields.Boolean
})

distance_sale_dto = distance_sale_sub_dto.clone('distance_sale', {
    'created_on': fields.Date,
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True),
    'original_filename': fields.String,
    'distance_sale_history': fields.List(fields.Nested(distance_sale_history_dto))
})

distance_sale_admin_dto = distance_sale_dto.clone('distance_sale_admin', {
    'id': fields.Integer,
    'seller_firm_id': fields.Integer,
})


class DistanceSaleSubSchema:

    @staticmethod
    def get_distance_sale_sub(distance_sale):
        distance_sale_as_dict = {
            'public_id': str(distance_sale.public_id),
            'valid_from': str(distance_sale.valid_from),
            'valid_to': str(distance_sale.valid_to),
            'arrival_country_code': distance_sale.arrival_country_code,
            'arrival_country': distance_sale.arrival_country.name,
            'active': distance_sale.active,
        }
        return distance_sale_as_dict
