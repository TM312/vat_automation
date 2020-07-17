from app.extensions import db
from datetime import datetime


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    subject = db.Column(db.String(128))
    status = db.Column(db.String(16))
    message = db.Column(db.String(256))

    n_type = db.Column(db.String(56))
    __mapper_args__ = {'polymorphic_on': n_type}





class TransactionNotification(Notification):
    __mapper_args__ = {'polymorphic_identity': 'transaction'}
    transaction_input_id = db.Column(db.Integer, db.ForeignKey('transaction_input.id'), nullable=False)
    original_filename = db.Column(db.String(128))

    def __repr__(self):
        return '<Notification {}: status: {} | message: {} (file: {})>'.format(self.created_on, self.status, self.message, self.original_filename)
