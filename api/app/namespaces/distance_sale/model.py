from datetime import datetime, timedelta, date
from uuid import uuid4

from app.extensions import db

from sqlalchemy.dialects.postgresql import UUID


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
    active = db.Column(db.Boolean, nullable=False)

    distance_sale_history = db.relationship('DistanceSaleHistory', backref='distance_sale', lazy=True, cascade='all, delete-orphan')


    def __repr__(self):
        return '<DistanceSale (seller firm id: {}): {} -> {}>'.format(self.seller_firm_id, self.arrival_country_code, self.active)

    def update(self, data_changes):
        from .service import DistanceSaleHistoryService

        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()

        DistanceSaleHistoryService.handle_update(self.id, data_changes)

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
    active = db.Column(db.Boolean)

    comment = db.Column(db.String(256))

    def attr_as_dict(self):
        return {
            'created_by': self.created_by,
            'valid_from': self.valid_from,
            'original_filename': self.original_filename,
            'seller_firm_id': self.seller_firm_id,
            'arrival_country_code': self.arrival_country_code,
            'active': self.active
        }
