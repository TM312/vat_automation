from uuid import uuid4

from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID

class Bundle(db.Model):
    """ Bundle model """
    __tablename__ = "bundle"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid4)
    transaction_inputs = db.relationship('TransactionInput', backref='bundle', order_by='TransactionInput.complete_date', lazy=True)


    def __repr__(self):
        return '<Bundle: {}>'.format(self.id)
