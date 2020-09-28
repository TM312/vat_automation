from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from app.extensions import db


class Vat(db.Model):  # type: ignore
    """ Vat model """
    __tablename__ = "vat"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid4)

    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date)

    country_code = db.Column(db.String(4), db.ForeignKey('country.code'))
    tax_code_code = db.Column(db.String(40), db.ForeignKey('tax_code.code'))
    tax_rate_type_code = db.Column(db.ForeignKey('tax_rate_type.code'), nullable = False)

    _rate = db.Column(db.Integer)

    @hybrid_property
    def rate(self):
        return self._rate / 10_000 if self._rate is not None else None

    @rate.setter
    def rate(self, value):
        self._rate = int(round(value * 10_000)) if value is not None else None

    def __repr__(self):
        return '<Vat: valid: {}-{} – country_code: {} - tax_code: {} – tax_rate_type_code: {} – rate {}>'.format(self.valid_from, self.valid_to, self.country_code, self.tax_code_code, self.tax_rate_type_code, self.rate)
