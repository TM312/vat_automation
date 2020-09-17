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



class TaxRateType(db.Model):  # type: ignore
    """ TaxRateTypeCountry model, e.g. codes: R, R2, Z, S """
    __tablename__ = "tax_rate_type"

    code = db.Column(db.String(8), primary_key=True)
    description = db.Column(db.String(256))
    vats = db.relationship('Vat', backref='tax_rate_type', lazy=True)
    #transaction_items = db.relationship('Transaction', backref='tax_rate_type', lazy=True)
    transaction_items = db.relationship('Transaction', backref='item_tax_rate_type', foreign_keys='Transaction.item_tax_rate_type_code', lazy=True)
    transaction_shipments = db.relationship('Transaction', backref='shipment_tax_rate_type', foreign_keys='Transaction.shipment_tax_rate_type_code', lazy=True)
    transaction_gift_wraps = db.relationship('Transaction', backref='gift_wrap_tax_rate_type', foreign_keys='Transaction.gift_wrap_tax_rate_type_code', lazy=True)



    def __repr__(self):
        return '<TaxRateType: {}'.format(self.code)
