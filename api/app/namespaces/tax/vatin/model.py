from datetime import datetime, date, timedelta
import uuid

from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID

from .helpers import VIES_OPTIONS



class VATIN(db.Model):
    """ VATIN model """
    __tablename__ = "vatin"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
    last_validated = db.Column(db.Date, nullable=False)
    valid_from = db.Column(db.Date, nullable=False)

    initial_tax_date = db.Column(db.Date)

    country_code = db.Column(db.String(4), nullable=False)
    number = db.Column(db.String(16), nullable=False)
    valid = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(128))
    address = db.Column(db.String(256))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    transactions = db.relationship('Transaction', backref='vatin', lazy=True)

    @hybrid_property
    def valid_to(self):
        return self.valid_from + timedelta(days=30) #!!! timedelta needs to be updated manually


    def __str__(self):
        unformated_number = "{}{}".format(self.country_code, self.number,)

        country = VIES_OPTIONS.get(self.country_code, {})
        if len(country) == 3:
            return country[2](unformated_number)
        return unformated_number

    def __repr__(self):
        return "<VATIN {}>".format(self.__str__())

    def update(self, data_changes):
        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()
        return self
