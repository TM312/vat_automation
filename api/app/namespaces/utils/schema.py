
from flask_restx import Model, fields

notification_dto = Model('notification', {
    'id': fields.Integer,
    'created_on': fields.DateTime,
    'subject': fields.String,
    'status': fields.String,
    'message': fields.String,
    'n_type': fields.String(readonly=True)
})

transaction_notification_dto = notification_dto.clone('transaction_notification', {
    'transaction_input_id': fields.Integer(readonly=True),
    'original_filename': fields.String,
})


response_object_dto: {
    'status': fields.String,
    'message': fields.String,
    'token': fields.String,

}
