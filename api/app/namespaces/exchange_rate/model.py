from datetime import datetime, date

from app.extensions import db  # noqa


class ExchangeRate(db.Model):
    __tablename__ = "exchange_rate"
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(32), default="ECB")
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.Date, default=date.today)
    !!! base = db.Column(db.String(32), db.ForeignKey('currency.code', name=) nullable=False)
    !!! target = db.Column(db.String(32),  db.ForeignKey('currency.code', name=) nullable=False)

    rate = db.Column(db.Numeric(scale=5), nullable=False)



    def __repr__(self):
        return '<ExchangeRate: Date: {} | Base: {} - Target: {} }>'.format(self.date, self.base, self.target)
