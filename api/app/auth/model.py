import datetime
import uuid
import jwt

from flask import current_app
from app.extensions import db


class Token(db.Model):
    """ Token model """
    __tablename__ = "token"

    id = db.Column(db.Integer(), primary_key=True)
    token = db.Column(db.String(), unique=True, nullable=False)
    iat = db.Column(db.DateTime(), nullable=False)
    sub = db.Column(db.String(36), nullable=False)
    blacklisted_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def __init__(self, token, iat, sub):
        super(Token, self).__init__()
        self.token = token
        self.iat = iat
        self.sub = sub

    def __repr__(self):
        return '<id {}: token: {}'.format(self.id, self.token)
