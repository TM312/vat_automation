from app.extensions import db  # noqa
from ..model_parent import Business
from sqlalchemy.ext.declarative import declared_attr



class SellerFirm(Business):
    __mapper_args__ = {'polymorphic_identity': 'seller_firm'}

    claimed = db.Column(db.Boolean, default=False)
    establishment_country_code = db.Column(db.Integer, db.ForeignKey('country.code'))

    vat_numbers = db.relationship('VATIN', backref='business', lazy=True)

    # https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/inheritance.html
    @declared_attr
    def employees(cls):
        "Employees column, if not present already."
        return Business.__table__.c.get('employees', db.relationship(
            'Seller', backref='employer', lazy=True))

    distance_sales = db.relationship('DistanceSale', backref='seller_firm', lazy=True)
    items = db.relationship('Item', backref='seller_firm', lazy=True)

    # IDs for supported platforms
    accounts = db.relationship('Account', backref='seller_firm', lazy=True)

    # Columns related to Accounting/Tax Service
    accounting_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    accounting_firm_client_id = db.Column(db.String(120), default=None)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<SellerFirm: %r>' % self.name
