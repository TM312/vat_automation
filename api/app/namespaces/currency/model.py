from app.extensions import db


class Currency(db.Model):  # type: ignore
    """ Currency model """
    __tablename__ = "currency"

    code = db.Column(db.String(4), primary_key=True)
    country_codes = db.relationship('Country', backref='currency', lazy=True)
    exchange_rates = db.relationship('ExchangeRatesBase', backref='currency', lazy=True)
    item_informations = db.relationship('ItemInformation', backref='currency', lazy=True)



    def __init__(self, **kwargs):
        super(Currency, self).__init__(**kwargs)

    def __repr__(self):
        return '<Currency: {}>'.format(self.code)
