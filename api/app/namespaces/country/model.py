from app.extensions import db


class Country(db.Model):  # type: ignore
    """ Country model """
    __tablename__ = "country"

    code = db.Column(db.String(4), primary_key=True)
    id = db.Column(db.Integer, autoincrement=True)
    country_name = db.Column(db.String(16), nullable=False)
    tax_codes = db.relationship('TaxRate', back_populates='country')

    currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'))
    distance_sales = db.relationship('DistanceSale', backref='country', lazy=True)
    seller_firms = db.relationship('SellerFirm', backref='establishment_country', lazy=True)

    transaction_arrivals = db.relationship('Transaction', backref='arrival_country', lazy=True)


    def __init__(self, **kwargs):
        super(Country, self).__init__(**kwargs)

    def __repr__(self):
        return '<Country: {}>'.format(self.code)
