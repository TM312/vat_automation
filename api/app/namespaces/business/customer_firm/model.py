from app.extensions import db
from .. import Business

class CustomerFirm(Business):
    __mapper_args__ = {'polymorphic_identity': 'customer_firm'}

    transactions = db.relationship('Transaction', backref='customer_firm', lazy=True)


    def __repr__(self):
        return '<Customer: Name:{} – Address:{}>'.format(self.name, self.address)
