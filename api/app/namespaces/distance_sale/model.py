from datetime import datetime, timedelta, date
from uuid import uuid4

from app.extensions import db

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property


class DistanceSale(db.Model):  # type: ignore
    """ Distance Sale model """
    __tablename__ = "distance_sale"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
    original_filename = db.Column(db.String(128))

    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    arrival_country_code = db.Column(db.String(8), db.ForeignKey('country.code'), nullable=False)
    active = db.Column(db.Boolean, default=False)
    ship_from_rule = db.Column(db.Boolean, default=False)
    _taxable_turnover_amount = db.Column(db.Integer, default=0)
    last_tax_date = db.Column(db.Date)

    #non-mirrored relationships here
    distance_sale_history = db.relationship('DistanceSaleHistory', backref='distance_sale', lazy=True, cascade='all, delete-orphan')

    @hybrid_property
    def taxable_turnover_amount(self):
        # https://ec.europa.eu/taxation_customs/sites/taxation/files/resources/documents/taxation/vat/traders/vat_community/vat_in_ec_annexi.pdf
        if self.arrival_country_code != 'HU':
            return self._taxable_turnover_amount / 100 if self._taxable_turnover_amount is not None else None
        else:
            if self._taxable_turnover_amount == 0:
                return 0
            else:
                from app.namespaces.exchange_rate.service import ExchangeRateService
                exchange_rate_HUN_EUR = ExchangeRateService.get_by_base_target_date('HUF', 'EUR', self.last_tax_date)
                return round(self._taxable_turnover_amount / 100 * exchange_rate_HUN_EUR, 2) if self._taxable_turnover_amount is not None else None

    @taxable_turnover_amount.setter
    def taxable_turnover_amount(self, value):
        self._taxable_turnover_amount = int(
            round(value * 100)) if value is not None else None


    def __repr__(self):
        return '<DistanceSale (seller firm id: {}): {} -> active: {} | ship_from_rule: {}>'.format(self.seller_firm_id, self.arrival_country_code, self.active, self.ship_from_rule)

    def update(self, data_changes):

        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()

        # DistanceSaleHistoryService.handle_update(self.id, data_changes)
        """
        In order to use HistoryService.handle_update(*) there need to be the following methods in place:
            - distance_sale_history.update(data_changes)
            - DistanceSaleHistoryService.get_oldest(distance_sale_id)
            - DistanceSaleHistoryService.get_current(distance_sale_id)
            - DistanceSaleHistoryService.get_by_relationship_date(distance_sale_id, date)
            - DistanceSaleHistoryService.create_empty(distance_sale_id)

        """
        from app.namespaces.utils.service import HistoryService
        from .service import DistanceSaleHistoryService
        HistoryService.handle_update(self.id, DistanceSaleHistory, DistanceSaleHistoryService, data_changes)

        return self


class DistanceSaleHistory(db.Model):  # type: ignore
    """ Distance sale history model """
    __tablename__ = "distance_sale_history"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)

    distance_sale_id = db.Column(db.Integer, db.ForeignKey('distance_sale.id'), nullable=False)
    valid_from = db.Column(db.Date, default=datetime.strptime('01-06-2018', '%d-%m-%Y').date)
    valid_to = db.Column(db.Date, default=datetime.strptime('31-12-2035', '%d-%m-%Y').date)

    created_by = db.Column(db.Integer)
    original_filename = db.Column(db.String(128))
    seller_firm_id = db.Column(db.Integer)
    arrival_country_code = db.Column(db.String(8))
    active = db.Column(db.Boolean, default=False)
    ship_from_rule = db.Column(db.Boolean, default=False)
    _taxable_turnover_amount = db.Column(db.Integer, default=0)
    last_tax_date = db.Column(db.Date)

    comment = db.Column(db.String(256))

    @hybrid_property
    def taxable_turnover_amount(self):
        #https://ec.europa.eu/taxation_customs/sites/taxation/files/resources/documents/taxation/vat/traders/vat_community/vat_in_ec_annexi.pdf
        if self.arrival_country_code != 'HU':
            return self._taxable_turnover_amount / 100 if self._taxable_turnover_amount is not None else None
        else:
            from app.namespaces.exchange_rate.service import ExchangeRateService
            exchange_rate_HUN_EUR = ExchangeRateService.get_by_base_target_date('HUF', 'EUR', self.last_tax_date)
            return (self._taxable_turnover_amount / 100 * exchange_rate_HUN_EUR) if self._taxable_turnover_amount is not None else None

    @taxable_turnover_amount.setter
    def taxable_turnover_amount(self, value):
        self._taxable_turnover_amount = int(round(value * 100)) if value is not None else None

    def attr_as_dict(self):
        return {
            'created_by': self.created_by,
            'valid_from': self.valid_from,
            'original_filename': self.original_filename,
            'seller_firm_id': self.seller_firm_id,
            'arrival_country_code': self.arrival_country_code,
            'active': self.active,
            'ship_from_rule': self.ship_from_rule,
            'taxable_turnover_amount': self.taxable_turnover_amount,
            'last_tax_date': self.last_tax_date

        }

    def update(self, data_changes):
        for key, val in data_changes.items():
            setattr(self, key, val)
        return self
