
from flask_restx import Model, fields

notification_dto = Model('notification', {
    'public_id': fields.String(readonly=True),
    'created_on': fields.DateTime(readonly=True),
    'subject': fields.String(readonly=True),
    'reference_value': fields.String(readonly=True),
    'calculated_value': fields.String(readonly=True),
    'status': fields.String(readonly=True),
    'message': fields.String(readonly=True),
    'n_type': fields.String(readonly=True)
})

transaction_notification_dto = notification_dto.clone('transaction_notification', {
    'transaction_id': fields.Integer(readonly=True),
    'original_filename': fields.String(readonly=True),
})

transaction_notification_admin_dto = transaction_notification_dto.clone('transaction_notification', {
    'id': fields.Integer(readonly=True)
})
