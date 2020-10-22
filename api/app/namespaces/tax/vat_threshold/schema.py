from flask_restx import Model, fields

vat_threshold_history_dto = Model('vat_threshold_history', {
    'public_id': fields.String(readonly=True),
    'valid_from': fields.Date,
    'valid_to': fields.Date,
    'comment': fields.String,
    'country_code': fields.String,
    'value': fields.Integer,
    'currency_code': fields.String
})


vat_threshold_sub_dto = Model('vat_threshold_sub', {
    'public_id': fields.String(readonly=True),

    #attribuitess
    'country_code': fields.String,
    'value': fields.String,
    'currency_code': fields.String

})

vat_threshold_dto = vat_threshold_sub_dto.clone('vat_threshold', {
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'created_on': fields.Date,
    'modified_at': fields.Date,
    'vat_threshold_history': fields.List(fields.Nested(vat_threshold_history_dto)),

})

vat_threshold_admin_dto = vat_threshold_dto.clone('vat_threshold_admin', {
    'id': fields.Integer(readonly=True),
})
