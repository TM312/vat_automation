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
        for key, val in data_changes.items():
            """
            Change of state 'active' is tracked for each distance sale. A distance sale history object is created whenever one of these attributes is being updated.
            """
            if key == 'active':
                valid_from = date.today() if not isinstance(data_changes.get('valid_from'), date) else data_changes.get('valid_from')

                 # Get the current distance sale history
                distance_sale_history = DistanceSaleHistory.query.filter_by(distance_sale_id = self.id).order_by(DistanceSaleHistory.valid_from.desc()).first()
                if isinstance(distance_sale_history, DistanceSaleHistory):
                    distance_sale_history.valid_to = valid_from-timedelta(days=1)

                else:
                    arrival_country_code = (
                        data_changes.get('arrival_country_code')
                        if isinstance(data_changes.get('arrival_country_code'), str)
                        else self.arrival_country_code
                    )

                    #create new distance sale history
                    new_distance_sale_history = DistanceSaleHistory(
                        valid_from = valid_from,
                        arrival_country_code = arrival_country_code,
                        active = val,
                        distance_sale_id = self.id
                    )
                    db.session.add(new_distance_sale_history)
                    self.distance_sale_history.append(new_distance_sale_history)

            setattr(self, key, val)
        self.modified_at = datetime.utcnow()
        return self


class DistanceSaleHistory(db.Model):  # type: ignore
    """ Distance sale history model """
    __tablename__ = "distance_sale_history"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)

    distance_sale_id = db.Column(db.Integer, db.ForeignKey('distance_sale.id'), nullable=False)

    valid_from = db.Column(db.Date, default=datetime.strptime('01-06-2018', '%d-%m-%Y').date)
    valid_to = db.Column(db.Date, default=datetime.strptime('31-12-2030', '%d-%m-%Y').date)

    arrival_country_code = db.Column(db.String(8), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    comment = db.Column(db.String(256))
