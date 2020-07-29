from flask_restx import Model, fields

tax_record_sub_dto = Model('tax_record_sub', {
    'public_id': fields.String(readonly=True),
    'tax_jurisdiction': fields.String(attribute=lambda x: x.tax_jurisdiction.name, readonly=True),
    'start_date': fields.Date(readonly=True),
    'end_date': fields.Date(readonly=True),
})

tax_record_dto = Model('tax_record', {
    'created_on': fields.DateTime(readonly=True),
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True),
    'filename': fields.String
})

tax_record_dto_admin = tax_record_dto.clone('tax_record_admin', {
    'id': fields.Integer(readonly=True),
    'active': fields.Boolean(readonly=True)
})
