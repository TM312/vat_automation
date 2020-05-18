from app.extensions import db
from ..model_parent import Platform
from sqlalchemy.ext.declarative import declared_attr


class Amazon(Platform):
    """ Amazon model """
    __mapper_args__ = {'polymorphic_identity': 'AMZ'}
    distance_sales = db.relationship('DistanceSale', backref='AMZ', lazy=True)

    def __init__(self, **kwargs):
        super(Amazon, self).__init__(**kwargs)



class DistanceSale(db.Model):  # type: ignore
    """ Distance Sale model """
    __tablename__ = "distance_sale"

    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id')
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    original_filename = db.Column(db.String(128))
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date, default=current_app.config['TAX_DEFAULT_VALIDITY'])

    platform_code = db.Column(db.String(32), db.ForeignKey('platform.code'), nullable=False)
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    arrival_country_code = db.Column(db.String(8), db.ForeignKey('country.code'), nullable=False)
    status = db.Column(db.Boolean, nullable=False)



    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<DistanceSale: {} {} {} {}>'.format(self.seller_firm_id, self.arrival_country_code, self.valid_from, self.valid_to)
