import datetime
import uuid
import hashlib
import jwt

from flask import current_app
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db  # noqa
from app.extensions import bcrypt
from .interface import UserInterface



class User(db.Model):  # type: ignore
    """ User model """
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    email = db.Column(db.String(254), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    role = db.Column(db.String, default='seller')  # roles = ['seller', 'admin']
    password_hash = db.Column(db.String(128), nullable=False)
    avatar_hash = db.Column(db.String(32))
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(64))
    last_seen = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.avatar_hash = self.gravatar_hash()
        self.confirmed_on = None

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')


    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password, rounds=current_app.config['BCRYPT_LOG_ROUNDS']).decode('utf-8')


    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def update(self, data_changes: UserInterface):
        for key, val in data_changes.items():
            if key == 'password':
                self.password = self.set_password(value)
            setattr(self, key, val)
        self.modified_at = datetime.datetime.utcnow()
        return self


    @staticmethod
    def encode_auth_token(public_id : str, token_lifespan : int):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'iss': current_app.config['COMPANY_NAME'].lower(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=token_lifespan),
                'iat': datetime.datetime.utcnow(),
                'sub': public_id
            }
            auth_token = jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            return auth_token

        except Exception as e:
            return e





    def __repr__(self):
        return '<User: %r>' % self.email
