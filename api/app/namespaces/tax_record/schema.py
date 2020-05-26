from flask_restx import Model, fields

tax_record_dto = Model('tax_record', {
    'public_id': fields.String(readonly=True),
    'created_on': fields.DateTime(readonly=True),
    'created_by': fields.Integer(read_only=True),
    'seller_firm': fields.String(attribute='seller_firm.name', readonly=True), #!!! eventuell hier Anpassungen: es soll Name angezeigt werden
    'tax_jurisdiction': fields.String(attribute='tax_jurisdiction.name', readonly=True)
    'start_date': fields.Date(readonly=True),
    'end_date': fields.Date(readonly=True)
    'filename': fields.String,

})

tax_record_dto_admin = tax_record_dto.clone('tax_record_admin', {
    'id': fields.Integer(readonly=True),
    'active': fields.Boolean(readonly=True)
})
