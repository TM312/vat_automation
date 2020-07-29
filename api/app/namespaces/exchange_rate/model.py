from datetime import datetime, date
from sqlalchemy.ext.hybrid import hybrid_property

from app.extensions import db  # noqa


class ExchangeRate(db.Model):
    __tablename__ = "exchange_rate"
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(32), default="ECB")
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.Date, default=date.today)
    base = db.Column(db.String(32), db.ForeignKey('currency.code'), nullable=False)
    target = db.Column(db.String(32),  db.ForeignKey('currency.code'), nullable=False)

    _rate = db.Column(db.Integer, nullable=False)

    @hybrid_property
    def rate(self):
        return self._rate / 10_000 if self._rate is not None else None

    @rate.setter
    def rate(self, value):
        self._rate = int(value * 10_000) if value is not None else None



    def __repr__(self):
        return '<ExchangeRate: Date: {} | Pair: {}-{} | Rate: {} >'.format(self.date, self.base, self.target, self.rate)
