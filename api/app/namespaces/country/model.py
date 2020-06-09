from flask import current_app

from app.extensions import db
from ..utils.ATs import eu_country_AT


#### ^potentially change to
#db.Column('country_code', db.String(4), db.ForeignKey('country.code'), primary_key=True) !!!!

class EU(db.Model):
    __tablename__ = "eu"
    id = db.Column(db.Integer, primary_key=True)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date)
    countries = db.relationship(
        "Country",
        secondary=eu_country_AT,
        back_populates="eus"
    )


class Country(db.Model):  # type: ignore
    """ Country model """
    __tablename__ = "country"

    code = db.Column(db.String(4), primary_key=True)
    vat_country_code = db.Column(db.String(4))
    name = db.Column(db.String(64), nullable=False)
    valid_from = db.Column(db.Date)
    valid_to = db.Column(db.Date)

    #tax_codes = db.relationship('Vat', back_populates='country')
    eus = db.relationship(
        "EU",
        secondary=eu_country_AT,
        back_populates="countries"
    )

    currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'))
    distance_sales = db.relationship('DistanceSale', backref='country', lazy=True)
    seller_firms = db.relationship('SellerFirm', backref='establishment_country', lazy=True)

    transactions = db.relationship('Transaction', backref='tax_jurisdiction', lazy=True)
    tax_records = db.relationship('TaxRecord', backref='tax_jurisdiction', lazy=True)
    vats = db.relationship('Vat', backref='country', lazy=True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<Country: {}>'.format(self.code)
