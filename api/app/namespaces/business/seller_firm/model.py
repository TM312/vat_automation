from app.extensions import db  # noqa
from ..model_parent import Business
from sqlalchemy.ext.declarative import declared_attr



class SellerFirm(Business):
    __mapper_args__ = {'polymorphic_identity': 'seller_firm'}

    claimed = db.Column(db.Boolean, default=False)
    establishment_country_code = db.Column(db.String(8), db.ForeignKey('country.code'))


    # https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/inheritance.html
    @declared_attr
    def employees(cls):
        'Employees column, if not present already.'
        # Pass foreign_keys= as a Python executable string for lazy evaluation (https://stackoverflow.com/questions/54703652/sqlalchemy-multiple-relationships-between-tables)
        return Business.__table__.c.get('employees', db.relationship('Seller', backref='employer', primaryjoin='Seller.employer_id==Business.id'))

    distance_sales = db.relationship('DistanceSale', backref='seller_firm', lazy=True)
    items = db.relationship('Item', backref='seller_firm', lazy='joined')

    # IDs for supported platforms
    accounts = db.relationship('Account', backref='seller_firm', lazy='joined')

    # Columns related to Accounting/Tax Service
    accounting_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    accounting_firm_client_id = db.Column(db.String(120), default=None)

    tax_records = db.relationship('TaxRecord', backref='seller_firm', lazy='joined')

    @property
    def transaction_ready(self):
        return (len(self.items) > 0 and len(self.distance_sales) > 0 and len(self.accounts) > 0)


    def __repr__(self):
        return '<SellerFirm: {} | Address: {}>'.format(self.name, self.name)
