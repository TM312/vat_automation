from datetime import datetime
import uuid

from app.extensions import db

from sqlalchemy.dialects.postgresql import UUID


class DistanceSale(db.Model):  # type: ignore
    """ Distance Sale model """
    __tablename__ = "distance_sale"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    original_filename = db.Column(db.String(128))
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date)

    platform_code = db.Column(db.String(32), db.ForeignKey('platform.code'), nullable=False)
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    arrival_country_code = db.Column(db.String(8), db.ForeignKey('country.code'), nullable=False)
    active = db.Column(db.Boolean, nullable=False)




    def __repr__(self):
        return '<DistanceSale: {} {} {} {}>'.format(self.seller_firm_id, self.arrival_country_code, self.valid_from, self.valid_to)
