import datetime
import uuid
import hashlib

from flask import current_app
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db  # noqa
from app.extensions import bcrypt

from ..model_association_tables import clients



class User(db.Model):  # type: ignore
    """ User model """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True,
                          nullable=False, default=uuid.uuid4)
    email = db.Column(db.String(254), unique=True, nullable=True) #nullable=True exists for unclaimed accounts
    company_name = db.Column(db.String(120), default=None)
    registered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # roles = ['seller', 'tax_auditor', 'admin']
    role = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(64))
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    discriminator = db.Column('type', db.String(50))
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

    def last_seen(self):
        self.last_seen = datetime.datetime.utcnow()
        return self



# clients = db.relationship(
    #     'User', secondary=clients,
    #     primaryjoin=(clients.c.tax_auditor_id == id),
    #     secondaryjoin=(clients.c.client_id == id),
    #     backref=db.backref('tax_auditors', lazy='dynamic'), lazy='dynamic')









 # def follow(self, client):
    #     if not self.is_following(self, client):
    #         self.clients.append(client)

    # def unfollow(self, client):
    #     if self.is_following(client):
    #         self.clients.remove(client)

    # def is_following(self, client):
    #     return self.clients.filter(
    #         clients.c.client_id == client.id).count() > 0
