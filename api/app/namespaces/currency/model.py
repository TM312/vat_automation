from app.extensions import db


class Currency(db.Model):  # type: ignore
    """ Currency model """
    __tablename__ = "currency"

    code = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    countries = db.relationship('Country', backref='currency', lazy=True)
    items = db.relationship('Item', backref='currency', lazy=True)
    transactions_transaction_currency = db.relationship('Transaction', backref='transaction_currency', foreign_keys='Transaction.transaction_currency_code', lazy=True)
    transactions_invoice_currency = db.relationship('Transaction', backref='invoice_currency', foreign_keys='Transaction.invoice_currency_code', lazy=True)


    bases = db.relationship('ExchangeRate', primaryjoin='Currency.code==ExchangeRate.base', lazy=True)
    targets = db.relationship('ExchangeRate', primaryjoin='Currency.code==ExchangeRate.target', lazy=True)



    def __repr__(self):
        return '<Currency: {}>'.format(self.code)
