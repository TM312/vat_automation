import datetime
import uuid
import hashlib

from flask import current_app
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db  # noqa
from app.extensions import bcrypt


class User(db.Model):  # type: ignore
    """ User model """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True,
                          nullable=False, default=uuid.uuid4)
    username = db.Column(db.String(32), unique=True, nullable=True)
    email = db.Column(db.String(32), unique=True, nullable=True) #nullable=True exists for unclaimed accounts
    employer_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    registered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    role = db.Column(db.String, nullable=False) # roles = ['employee', '_', 'admin']
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(40))
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(32))
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    transaction_uploads = db.relationship(
        'Transaction', backref='uploader', order_by="desc(Transaction.added_on)", lazy=True)

    actions = db.relationship(
        'Action', backref='user', order_by="desc(Action.timestamp)", lazy=True)

    discriminator = db.Column('u_type', db.String(56))
    __mapper_args__ = {'polymorphic_on': discriminator}


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password, rounds=current_app.config['BCRYPT_LOG_ROUNDS']).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def update(self, data_changes):
        for key, val in data_changes.items():
            if key == 'password':
                self.password = self.set_password(value)
            setattr(self, key, val)
        self.modified_at = datetime.datetime.utcnow()
        return self

    def update_last_seen(self):
        self.last_seen = datetime.datetime.utcnow()
        return self


class Action(db.Model):  # type: ignore
    """ Action model """
    __tablename__ = "action"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                         nullable=False)
    method_name = db.Column(db.String(32))
    service_context = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(Action, self).__init__(**kwargs)
