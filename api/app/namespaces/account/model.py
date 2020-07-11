from datetime import datetime
import uuid

from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID


class Account(db.Model):
    """ Account model, e.g. Amazon --> MFN --> A2SC0NLSYTA68B (Unique Account Identifier) """
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    given_id = db.Column(db.String(24), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
    channel_code = db.Column(db.String(8), db.ForeignKey('channel.code'))
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    transactions = db.relationship('Transaction', backref='account', lazy=True)


    def update(self, data_changes):
        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()
        return self
