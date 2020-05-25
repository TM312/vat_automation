from app.extensions import db




class Customer(db.Model):  # type: ignore
    """ Customer model: user/business buying from seller_firm through a transaction """
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    address = db.Column(db.String(64))
!!!     vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))
    modified_at = db.Column(db.DateTime)
    times_modified = db.Column(db.Integer, default=0)

    transactions = db.relationship('Transaction', backref='customer', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<Customer: Name:{} – Type:{} – VAT Number: {}>'.format(self.name, self.customer_relationship_code, self.customer_vat_number)

    def update(self, data_changes):
        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()
        self.times_modified + = 1
        return self
