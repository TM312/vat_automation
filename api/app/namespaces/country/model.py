from flask import current_app

from app.extensions import db
from app.namespaces.utils.ATs import eu_country_AT




class EU(db.Model):
    __tablename__ = "eu"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(64), unique=True)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date)
    countries = db.relationship(
        "Country",
        secondary=eu_country_AT,
        back_populates="eus"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.public_id = 'EU-{}-{}'.format(kwargs.get('valid_from'), kwargs.get('valid_to'))

    def update(self, data_changes):
        for key, val in data_changes.items():
            if key.lower() != 'id':
                setattr(self, key, val)
        return self


class Country(db.Model):  # type: ignore
    """ Country model """
    __tablename__ = "country"

    code = db.Column(db.String(4), primary_key=True)

    vat_country_code = db.Column(db.String(4))
    name = db.Column(db.String(64), nullable=False)
    # valid_from = db.Column(db.Date)
    # valid_to = db.Column(db.Date)

    currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'))

    # non-mirrored relationships
    eus = db.relationship(
        "EU",
        secondary=eu_country_AT,
        back_populates="countries"
    )

    distance_sales = db.relationship('DistanceSale', backref='arrival_country', lazy=True)
    seller_firms = db.relationship('SellerFirm', backref='establishment_country')

    transaction_inputs_departure_country = db.relationship('TransactionInput', backref='departure_country', foreign_keys='TransactionInput.departure_country_code', lazy=True)
    transaction_inputs_arrival_country = db.relationship('TransactionInput', backref='arrival_country', foreign_keys='TransactionInput.arrival_country_code', lazy=True)


    transactions_tax_jurisdiction = db.relationship('Transaction', backref='tax_jurisdiction', foreign_keys='Transaction.tax_jurisdiction_code', lazy=True)
    transactions_departure_country = db.relationship('Transaction', backref='departure_country', foreign_keys='Transaction.departure_country_code', lazy=True)
    transactions_arrival_country = db.relationship('Transaction', backref='arrival_country', foreign_keys='Transaction.arrival_country_code', lazy=True)


    tax_records = db.relationship('TaxRecord', backref='tax_jurisdiction', lazy=True)
    vats = db.relationship('Vat', backref='country', lazy=True)
    vat_thresholds = db.relationship('VatThreshold', backref='country', lazy=True)
    vatins = db.relationship('VATIN', backref='country', lazy=True)


    def __repr__(self):
        return '<Country: {}>'.format(self.code)

    def update(self, data_changes):
        for key, val in data_changes.items():
            if key.lower() != 'code':
                setattr(self, key, val)
        return self
