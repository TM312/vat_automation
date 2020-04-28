from app.extensions import db
from ..model_parent import Platform
from sqlalchemy.ext.declarative import declared_attr


class Amazon(Platform):
    """ Amazon model """
    __mapper_args__ = {'polymorphic_identity': 'amazon'}
    distance_sales = db.relationship(
        'DistanceSale', backref='amazon', lazy=True)

    def __init__(self, **kwargs):
        super(Amazon, self).__init__(**kwargs)



class DistanceSale(db.Model):  # type: ignore
    """ Distance Sale model """
    __tablename__ = "distance_sale"

    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(32), db.ForeignKey('platform.name'),
                               nullable=False)
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                               nullable=False)
    arrival_country_code = db.Column(db.String(8), db.ForeignKey('country.code'),
                                     nullable=False)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date, default=current_app.config['TAX_DEFAULT_VALIDITY'])

    def __init__(self, **kwargs):
        super(DistanceSale, self).__init__(**kwargs)

    def __repr__(self):
        return '<DistanceSale: {} {} {} {}>'.format(self.seller_firm_id, self.country_code, self.valid_from, self.valid_to)
