from uuid import uuid4
from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from .ATs import tag_notification_AT


"""
NULLABLE FALSE DOES NOT WORK ON STI CLASSES --> OTHER CLASSES WILL CONTAIN NULL VALUES THERE

"""

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid4)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
    subject = db.Column(db.String(128))
    status = db.Column(db.String(16))
    message = db.Column(db.String(256))
    tags = db.relationship(
        "Tag",
        secondary=tag_notification_AT,
        back_populates="notifications"
    )

    n_type = db.Column(db.String(56))
    __mapper_args__ = {'polymorphic_on': n_type}

    def modify(self):
        self.modified_at = datetime.utcnow()
        return self



class TransactionNotification(Notification):
    __mapper_args__ = {'polymorphic_identity': 'transaction'}
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    reference_value = db.Column(db.String(256))
    calculated_value = db.Column(db.String(256))
    original_filename = db.Column(db.String(128))

    def __repr__(self):
        return '<Notification {}: status: {} | ref val: {} | calc val: {}>'.format(self.created_on, self.status, self.reference_value, self.calculated_value)


class SellerFirmNotification(Notification):
    __mapper_args__ = {'polymorphic_identity': 'seller_firm'}
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Notification {}: status: {} | seller_firm_id: {}>'.format(self.created_on, self.status, self.seller_firm_id)
