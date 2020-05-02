from datetime import datetime

from app.extensions import db  # noqa


class TaxRecord(db.Model):  # type: ignore
    """ Tax record model """
    __tablename__ = "tax_record"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                           nullable=False)
    accounting_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                                    nullable=False)

    modified_at = db.Column(db.DateTime, default=datetime.utcnow)
    downloaded = db.Column(db.Boolean, default=False)
    activity_period = db.Column(db.String(16), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                                 nullable=False)
    storage_dir = db.Column(db.String(128), nullable=False)

    inputs = db.relationship(
        'TaxRecordInput', backref='tax_record', lazy='joined')
    outputs = db.relationship(
        'TaxRecordOutput', backref='tax_record', lazy='joined')


    def __init__(self, **kwargs):
        super(TaxRecord, self).__init__(**kwargs)
        self.modified_at = None
        self.output_name = None

    def update(self, data_changes):  # : TaxRecordInterface):
        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()
        self.times_submitted += 1
        return self

    def __repr__(self):
        return '<Tax Record: %r>' % self.id


class TaxRecordInput(db.Model):  # type: ignore
    """ TaxRecordInput model """
    __tablename__ = "tax_record_input"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    platform = db.Column(db.String(40), default='amazon')
    tax_record_id = db.Column(db.Integer, db.ForeignKey('tax_record.id'),
                              nullable=False)
    original_input_name = db.Column(db.String(64), nullable=False)
    formatted_input_name = db.Column(db.String(64), nullable=False)
    times_submitted = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        super(TaxRecordInput, self).__init__(**kwargs)
        self.times_submitted = 1

    def update(self, data_changes):  # : TaxRecordInterface):
        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()
        self.times_submitted += 1
        return self


class TaxRecordOutput(db.Model):  # type: ignore
    """ TaxRecordOutput model """
    __tablename__ = "tax_record_output"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    tax_record_id = db.Column(db.Integer, db.ForeignKey('tax_record.id'),
                              nullable=False)
    output_name = db.Column(db.String(64), nullable=False)
    downloaded = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(TaxRecordOutput, self).__init__(**kwargs)


class TaxRecordOutputCountry(db.Model):  # type: ignore
    """ TaxRecordOutputCountry model """
    __tablename__ = "tax_record_output_country"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    countries = db.relationship(
        'TaxRecordOutput', backref='country', lazy=True)


    def __init__(self, **kwargs):
        super(TaxRecordOutputCountry, self).__init__(**kwargs)
