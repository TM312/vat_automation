from datetime import datetime, date
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db
from ..utils.ATs import tax_record_user_AT



class TaxRecord(db.Model):
    """ Tax Record model """
    __tablename__ = 'tax_record'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)
    active = db.Column(db.Boolean, default=True)
    created_on = db.Column(db.Date, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    downloaded_by_users = db.relationship('User', secondary=tax_record_user_AT, back_populates='downloaded_tax_records')

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    filename = db.Column(db.String(128), unique=True, nullable=False)

    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    tax_jurisdiction_code = db.Column(db.String(8), db.ForeignKey('country.code'), nullable=False)


    def __repr__(self):
        return '<SellerFirm: {} | validity: {}-{}>'.format(self.seller_firm.name, str(start_date), str(end_date))
