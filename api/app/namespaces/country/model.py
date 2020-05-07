from flask import current_app

from app.extensions import db

eu_country_AT = db.Table(
    'eu_country_AT',
    db.Column('eu_id', db.Integer, db.ForeignKey('eu.id'), primary_key=True),
    db.Column('country_code', db.Integer, db.ForeignKey('country.code'), primary_key=True)
    )

#### ^potentially change to
#db.Column('country_code', db.String(4), db.ForeignKey('country.code'), primary_key=True)

class EU(db.Model):
    __tablename__ = "eu"
    id = db.Column(db.Integer, primary_key=True)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date, default=current_app.config['TAX_DEFAULT_VALIDITY'])
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
    name = db.Column(db.String(16), nullable=False)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date, default=current_app.config['TAX_DEFAULT_VALIDITY'])

    tax_codes = db.relationship('TaxRate', back_populates='country')
    eus = db.relationship(
        "EU",
        secondary=eu_country_AT,
        back_populates="countries"
    )

    currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), default=None)
    distance_sales = db.relationship('DistanceSale', backref='country', lazy=True)
    seller_firms = db.relationship('SellerFirm', backref='establishment_country', lazy=True)

    transaction_arrivals = db.relationship('Transaction', backref='arrival_country', lazy=True)


    def __init__(self, **kwargs):
        super(Country, self).__init__(**kwargs)

    def __repr__(self):
        return '<Country: {}>'.format(self.code)
