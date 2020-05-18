from datetime import datetime
from app.extensions import db

class Token(db.Model):
    """ Token model """
    __tablename__ = "token"

    id = db.Column(db.Integer, primary_key=True)
    auth_token = db.Column(db.String(256), unique=True, nullable=False)
    iat = db.Column(db.DateTime, nullable=False)
    sub = db.Column(db.String(36), nullable=False)
    blacklisted_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<id {}: auth_token: {}'.format(self.id, self.auth_token)
