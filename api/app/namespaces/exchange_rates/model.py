from datetime import datetime, date

from app.extensions import db  # noqa


class ExchangeRateCollection(db.Model):
    """ ExchangeRates parent_model """
    __tablename__ = "exchange_rate_collection"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    exchange_rates_eur = db.relationship(
        'ExchangeRatesEUR', backref='exchange_rate_collection', lazy=True)
    exchange_rates_gbp = db.relationship(
        'ExchangeRatesGBP', backref='exchange_rate_collection', lazy=True)
    exchange_rates_czk = db.relationship(
        'ExchangeRatesPLN', backref='exchange_rate_collection', lazy=True)
    exchange_rates_pln = db.relationship(
        'ExchangeRatesPLN', backref='exchange_rate_collection', lazy=True)


    def __init__(self, **kwargs):
        super(ExchangeRateCollection, self).__init__(**kwargs)

    def __repr__(self):
        return '<ExchangeRates: %r>' % self.date



    discriminator = db.Column('exchange_rates_currency', db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}

class ExchangeRatesBase(db.Model):
    """ ExchangeRates BASE model """
    __tablename__ = "exchange_rates"
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(32), default="ECB")
    date = db.Column(db.Date, default=date.today)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    exchange_rate_collection_id = db.Column(db.Integer, db.ForeignKey('exchange_rate_collection.id'),
                                            nullable=False)
    currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'),
                              nullable=False)

    eur = db.Column(db.Numeric(scale=8))
    gbp = db.Column(db.Numeric(scale=8))
    czk = db.Column(db.Numeric(scale=8))
    pln = db.Column(db.Numeric(scale=8))

    discriminator = db.Column('base', db.String(32))
    __mapper_args__ = {'polymorphic_on': discriminator}


class ExchangeRatesEUR(ExchangeRatesBase):
    """ ExchangeRates EUR model """
    __mapper_args__ = {'polymorphic_identity': 'eur'}

    exchange_rates_eur_id = db.Column('id', db.Integer, db.ForeignKey('exchange_rates.id'),
                         primary_key=True)

    def __init__(self, **kwargs):
        super(ExchangeRatesEUR, self).__init__(**kwargs)
        self.currency_code = 'EUR'

    def __repr__(self):
        return '<ExchangeRatesEUR: %r>' % self.exchange_rate_collection.date


class ExchangeRatesGBP(ExchangeRatesBase):
    """ ExchangeRates GPB model """
    __mapper_args__ = {'polymorphic_identity': 'gbp'}

    gbp_id = db.Column('id', db.Integer, db.ForeignKey('exchange_rates.id'),
                                      primary_key=True)

    def __init__(self, **kwargs):
        super(ExchangeRatesGBP, self).__init__(**kwargs)
        self.currency_code = 'GBP'

    def __repr__(self):
        return '<ExchangeRatesGBP: %r>' % self.exchange_rate_collection.date


class ExchangeRatesCZK(ExchangeRatesBase):
    """ ExchangeRates CZK model """
    __mapper_args__ = {'polymorphic_identity': 'czk'}

    czk_id = db.Column('id', db.Integer, db.ForeignKey('exchange_rates.id'),
                                      primary_key=True)

    def __init__(self, **kwargs):
        super(ExchangeRatesCZK, self).__init__(**kwargs)
        self.currency_code = 'CZK'

    def __repr__(self):
        return '<ExchangeRatesCZK: %r>' % self.exchange_rate_collection.date


class ExchangeRatesPLN(ExchangeRatesBase):
    """ ExchangeRates PLN model """
    __mapper_args__ = {'polymorphic_identity': 'pln'}

    pln_id = db.Column('id', db.Integer, db.ForeignKey('exchange_rates.id'),
                                      primary_key=True)

    def __init__(ExchangeRatesPLN, **kwargs):
        super(ExchangeRatesPLN, self).__init__(**kwargs)
        self.currency_code = 'PLN'

    def __repr__(self):
        return '<ExchangeRatesPLN: %r>' % self.exchange_rate_collection.date
