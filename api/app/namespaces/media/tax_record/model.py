import datetime

from app.extensions import db  # noqa
#from .interface import TaxRecordInterface


class TaxRecord(db.Model):  # type: ignore
    """ Tax record model """
    __tablename__ = "tax_record"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    times_submitted = db.Column(db.Integer, nullable=False)
    downloaded = db.Column(db.Boolean, default=False)
    platform = db.Column(db.String(36), default='Amazon')
    activity_period = db.Column(db.String(10), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                                 nullable=False)
    storage_dir = db.Column(db.String(120), nullable=False)
    original_input_name = db.Column(db.String(50), nullable=False)
    formatted_input_name = db.Column(db.String(50), nullable=False)
    output_name = db.Column(db.String(50))

    def __init__(self, **kwargs):
        super(TaxRecord, self).__init__(**kwargs)
        self.times_submitted = 1
        self.modified_at = None
        self.output_name = None

    def update(self, data_changes):  # : TaxRecordInterface):
        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.datetime.utcnow()
        return self

    def __repr__(self):
        return '<Tax Record: %r>' % self.id
