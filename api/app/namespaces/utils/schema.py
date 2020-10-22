
from flask_restx import Model, fields
from app.namespaces.tag import tag_dto

notification_dto = Model('notification', {
    'public_id': fields.String(readonly=True),
    'created_on': fields.DateTime(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'subject': fields.String(readonly=True),
    'status': fields.String(readonly=True),
    'message': fields.String(readonly=True),
    'tags': fields.List(fields.Nested(tag_dto))
})

transaction_notification_dto = notification_dto.clone('transaction_notification', {
    'original_filename': fields.String(readonly=True),
    'reference_value': fields.String(readonly=True),
    'calculated_value': fields.String(readonly=True),
})

seller_firm_notification_dto = notification_dto.clone('transaction_notification', {
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name , readonly=True),
    'seller_firm_public_id': fields.String(attribute=lambda x: x.seller_firm.public_id, readonly=True),
    'created_by': fields.String(attribute=lambda x: x.user.name , readonly=True),
})

transaction_notification_admin_dto = transaction_notification_dto.clone('transaction_notification', {
    'id': fields.Integer(readonly=True),
    'transaction_id': fields.Integer(readonly=True),
    'n_type': fields.String(readonly=True)
})
