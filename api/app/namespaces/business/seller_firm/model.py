from app.extensions import db  # noqa
from ..model_parent import Business
from sqlalchemy.ext.declarative import declared_attr
# from ...utils.ATs import tax_auditor_seller_firm_AT



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

    distance_sales = db.relationship('DistanceSale', backref='seller_firm', lazy='joined', cascade = 'all, delete-orphan')
    items = db.relationship('Item', backref='seller_firm', lazy='joined', cascade='all, delete-orphan')

    # IDs for supported platforms
    accounts = db.relationship('Account', backref='seller_firm', lazy='joined', cascade='all, delete-orphan')

    # Columns related to Accounting/Tax Service
    accounting_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    accounting_firm_client_id = db.Column(db.String(120), default=None)
    # tax_auditors = db.relationship('TaxAuditor', secondary=tax_auditor_seller_firm_AT, back_populates='key_accounts')


    tax_records = db.relationship('TaxRecord', backref='seller_firm', lazy='joined', cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='seller_firm', lazy='joined', cascade='all, delete-orphan', primaryjoin='Transaction.seller_firm_id==Business.id')


    @property
    def transaction_ready(self):
        return (len(self.items) > 0 and len(self.accounts) > 0)

    def __repr__(self):
        return '<SellerFirm: {} | Address: {}>'.format(self.name, self.address)
