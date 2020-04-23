from app.extensions import db




class CustomerType(db.Model):  # type: ignore
    """ CustomerType model: i.e. B2B / B2C """
    __tablename__ = "customer_type"

    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(256))
    customer = db.relationship(
        'Customer', backref='customer_type', lazy=True)

    def __init__(self, **kwargs):
        super(CustomerType, self).__init__(**kwargs)

    def __repr__(self):
        return '<CustomerType: {} – {}>'.format(self.code)


class Customer(db.Model):  # type: ignore
    """ Customer model: user/business buying from seller_firm through a transaction """
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    customer_type_code = db.Column(db.String(8), db.ForeignKey('customer_type.code'))

    !!!                 customer_vat_number = db.Column(db.Integer, db.ForeignKey('XXX'))

    transactions = db.relationship(
        'Transaction', backref='customer', lazy=True)

    def __init__(self, **kwargs):
        super(Customer, self).__init__(**kwargs)

    def __repr__(self):
        return '<Customer: Name:{} – Type:{} – VAT Number: {}>'.format(self.name, self.customer_type_code, self.customer_vat_number)
