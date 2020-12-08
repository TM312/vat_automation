from uuid import uuid4
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from app.extensions import db


class Vat(db.Model):  # type: ignore
    """ Vat model """
    __tablename__ = "vat"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid4)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)

    country_code = db.Column(db.String(4), db.ForeignKey('country.code'))
    tax_code_code = db.Column(db.String(40), db.ForeignKey('tax_code.code'))
    tax_rate_type_code = db.Column(db.String(8), db.ForeignKey('tax_rate_type.code'), nullable=False)

    _rate = db.Column(db.Integer)


    vat_history = db.relationship('VatHistory', backref='vat', lazy=True, cascade='all, delete-orphan')


    @hybrid_property
    def rate(self):
        return self._rate / 10_000 if self._rate is not None else None

    @rate.setter
    def rate(self, value):
        self._rate = int(round(value * 10_000)) if value is not None else None

    def __repr__(self):
        return '<Vat: valid: {}-{} – country_code: {} - tax_code: {} – tax_rate_type_code: {} – rate {}>'.format(self.valid_from, self.valid_to, self.country_code, self.tax_code_code, self.tax_rate_type_code, self.rate)

    def update(self, data_changes):

        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()

        """
        In order to use HistoryService.handle_update(*) there need to be the following methods in place:
            - vat_history.update(data_changes)
            - VatHistoryService.get_oldest(vat_id)
            - VatHistoryService.get_current(vat_id)
            - VatHistoryService.get_by_relationship_date(vat_id, date)
            - VatHistoryService.create_empty(vat_id)

        """
        from app.namespaces.utils.service import HistoryService
        from .service import VatHistoryService
        HistoryService.handle_update(self.id, VatHistory, VatHistoryService, data_changes)

        return self



class VatHistory(db.Model):  # type: ignore
    """ Vat history model """
    __tablename__ = "vat_history"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)

    vat_id = db.Column(db.Integer, db.ForeignKey('vat.id'), nullable=False)
    valid_from = db.Column(db.Date, default=datetime.strptime('01-06-2018', '%d-%m-%Y').date)
    valid_to = db.Column(db.Date, default=datetime.strptime('31-12-2035', '%d-%m-%Y').date)

    country_code = db.Column(db.String(4))
    tax_code_code = db.Column(db.String(40))
    tax_rate_type_code = db.Column(db.String(8), nullable=False)

    _rate = db.Column(db.Integer)

    comment = db.Column(db.String(256))

    @hybrid_property
    def rate(self):
        return self._rate / 10_000 if self._rate is not None else None

    @rate.setter
    def rate(self, value):
        self._rate = int(round(value * 10_000)) if value is not None else None


    def attr_as_dict(self):
        return {
            'created_by': self.created_by,
            'valid_from': self.valid_from,
            'country_code': self.country_code,
            'tax_code_code': self.tax_code_code,
            'tax_rate_type_code': self.tax_rate_type_code,
            'rate': self.rate
        }

    def update(self, data_changes):
        for key, val in data_changes.items():
            setattr(self, key, val)
        return self
