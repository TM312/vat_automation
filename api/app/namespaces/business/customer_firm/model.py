from ..model_parent import Business

class CustomerFirm(Business):
    __mapper_args__ = {'polymorphic_identity': 'customer_firm'}

    vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))
    transactions = db.relationship('Transaction', backref='customer', lazy=True)


    def __repr__(self):
        return '<Customer: Name:{} – Type:{} – VAT Number: {}>'.format(self.name, self.address, self.vatin.country_code, self.vatin.number)
