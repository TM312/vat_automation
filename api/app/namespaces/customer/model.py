from app.extensions import db




class CustomerRelationship(db.Model):  # type: ignore
    """ CustomerRelationship model: i.e. B2B / B2C """
    __tablename__ = "customer_relationship"

    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(256))
    customers = db.relationship('Customer', backref='customer_relationship', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<CustomerRelationship: {} – {}>'.format(self.code)


class Customer(db.Model):  # type: ignore
    """ Customer model: user/business buying from seller_firm through a transaction """
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    type_code = db.Column(db.String(8), db.ForeignKey('customer_relationship.code'))
    vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))

    transactions = db.relationship('Transaction', backref='customer', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<Customer: Name:{} – Type:{} – VAT Number: {}>'.format(self.name, self.customer_relationship_code, self.customer_vat_number)
