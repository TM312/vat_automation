from flask_restx import Model, fields

exchange_rate_dto = Model('exchange_rate', {
    'id': fields.Integer(readonly=True),
    'source': fields.String,
    'created_on': fields.DateTime,
    'date': fields.Date,
    'base': fields.String,
    'target': fields.String,
    'rate': fields.Float,
})
