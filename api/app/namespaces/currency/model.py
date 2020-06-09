from app.extensions import db


class Currency(db.Model):  # type: ignore
    """ Currency model """
    __tablename__ = "currency"

    code = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    countries = db.relationship('Country', backref='currency', lazy=True)
    items = db.relationship('Item', backref='currency', lazy=True)
    transactions = db.relationship('Transaction', backref='currency', lazy=True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<Currency: {}>'.format(self.code)
