from flask_restx import Model, fields

tax_record_dto = Model('tax_record', {
    'id': fields.Integer(readonly=True),
    'created_on': fields.DateTime(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'times_submitted': fields.Integer(readonly=True),
    'downloaded': fields.Boolean(readonly=True),
    'platform': fields.String(readonly=True),
    'activity_period': fields.String(readonly=True),
    'unique_account_identifier' : fields.String(readonly=True),
    'owner_id': fields.String(readonly=True),
    'storage_dir': fields.String(readonly=True),
    'original_input_name': fields.String(readonly=True),
    'formatted_input_name': fields.String(readonly=True),
    'output_name': fields.String(readonly=True)
})

owner
