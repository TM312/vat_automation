from flask_restx import Model, fields


account_dto = Model('account', {
    'id': fields.Integer(readonly=True),
    'given_id': fields.String,
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'created_on': fields.Date(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'channel_code': fields.String,
    'seller_firm_id': fields.Integer,
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True)

})
