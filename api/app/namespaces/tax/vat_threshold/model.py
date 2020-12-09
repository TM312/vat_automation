from uuid import uuid4
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from app.extensions import db


class VatThreshold(db.Model):  # type: ignore
    """ Vat threshold model """
    __tablename__ = "vat_threshold"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid4)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)

    #attribuitess
    country_code = db.Column(db.String(4), db.ForeignKey('country.code'))
    value = db.Column(db.Integer)
    currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'))

    # non-mirrored relationships
    vat_threshold_history = db.relationship('VatThresholdHistory', backref='vat_threshold', lazy=True, cascade='all, delete-orphan')


    def __repr__(self):
        return '<Vat Threshold: valid: {}-{} – country_code: {} - value: {}>'.format(self.valid_from, self.valid_to, self.country_code, self.value)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        if kwargs.get('currency_code') is None:
            from app.namespaces.country.service import CountryService
            country = CountryService.get_by_code(kwargs.get('country_code'))
            self.currency_code = country.currency_code




    def update(self, data_changes):
        from .service import VatThresholdHistoryService

        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()

        VatThresholdHistoryService.handle_update(self.id, data_changes)

        return self

    def update(self, data_changes):
        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()

        """
        In order to use HistoryService.handle_update(*) there need to be the following methods in place:
            - vat_threshold_history.update(data_changes)
            - VatThresholdHistoryService.get_oldest(vat_threshold_id)
            - VatThresholdHistoryService.get_current(vat_threshold_id)
            - VatThresholdHistoryService.get_by_relationship_date(vat_threshold_id: int, date: date)
            - VatThresholdHistoryService.create_empty(vat_threshold_id)

        """
        from app.namespaces.utils.service import HistoryService
        from .service import VatThresholdHistoryService
        try:

            HistoryService.handle_update(self.id, VatThresholdHistory, VatThresholdHistoryService, data_changes)
        except:
            raise

        db.session.commit()

        return self



class VatThresholdHistory(db.Model):  # type: ignore
    """ Vat threshold history model """
    __tablename__ = "vat_threshold_history"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid4)

     #meta data
    vat_threshold_id = db.Column(db.Integer, db.ForeignKey('vat_threshold.id'), nullable=False)
    valid_from = db.Column(db.Date, default=datetime.strptime('01-07-2019', '%d-%m-%Y').date)
    valid_to = db.Column(db.Date, default=datetime.strptime('31-12-2035', '%d-%m-%Y').date)
    comment = db.Column(db.String(256))

    # mirrored attributes (no relationships!)
    created_by = db.Column(db.Integer)
    country_code = db.Column(db.String(4))
    value = db.Column(db.Integer)
    currency_code = db.Column(db.String(4))


    def __repr__(self):
        return '<Vat Threshold History: valid: {}-{} – country_code: {} - value: {}>'.format(str(self.valid_from), str(self.valid_to), self.country_code, self.value)


    def attr_as_dict(self):
        return {
            'valid_from': self.valid_from,
            'created_by': self.created_by,
            'country_code': self.country_code,
            'value': self.value,
            'currency_code': self.currency_code
        }

    def update(self, data_changes):
        for key, val in data_changes.items():
            setattr(self, key, val)
        return self
