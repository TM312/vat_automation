from flask_restx import Model, fields


item_sub_dto = Model('item_sub', {
    'public_id': fields.String(readonly=True),
    'original_filename': fields.String,
    'sku': fields.String,
    'brand_name': fields.String,
    'name': fields.String,
    'weight_kg': fields.Float,
    'tax_code_code': fields.String,
    'unit_cost_price_currency_code': fields.String,
    'unit_cost_price_net': fields.Float
})

item_dto = item_sub_dto.clone('item', {
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'created_on': fields.Date,
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True),
    'ean': fields.String,
    'asin': fields.String,
    'fnsku': fields.String,
    'valid_from': fields.Date,
    'valid_to': fields.Date,
})

item_admin_dto = item_dto.clone('item_admin', {
    'id': fields.Integer(readonly=True),
    'seller_firm_id': fields.Integer
})


class ItemSubSchema:

    @staticmethod
    def get_item_sub(item):
        item_as_dict = {
            'public_id': str(item.public_id),
            'original_filename': item.original_filename,
            'sku': item.sku,
            'brand_name': item.brand_name,
            'name': item.name,
            'weight_kg': item.weight_kg,
            'tax_code_code': item.tax_code_code,
            'unit_cost_price_currency_code': item.unit_cost_price_currency_code,
            'unit_cost_price_net': item.unit_cost_price_net
        }
        return item_as_dict
