
from app.extensions import db


class Account(db.Model):
    """ Account model, e.g. Amazon --> MFN --> A2SC0NLSYTA68B (Unique Account Identifier) """
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(24), nullable=False)
    channel_code = db.Column(db.Integer, db.ForeignKey('channel.code'))
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)
