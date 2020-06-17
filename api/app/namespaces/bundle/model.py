from app.extensions import db

class Bundle(db.Model):
    """ Bundle model """
    __tablename__ = "bundle"

    id = db.Column(db.Integer, primary_key=True)
    transaction_inputs = db.relationship('TransactionInput', backref='bundle', lazy=True)


    def __repr__(self):
        return '<Bundle: {}>'.format(self.id)
