from datetime import datetime
from uuid import uuid4
from hashlib import md5

from flask import current_app
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property


from app.extensions import db, bcrypt

# from app.namespaces.utils.ATs import tax_record_user_AT


class User(db.Model):  # type: ignore
    """ User model """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)

    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    name = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(32), unique=True)
    # https://docs.sqlalchemy.org/en/13/core/constraints.html
    employer_id = db.Column(db.Integer, db.ForeignKey('business.id', name='fk_user_employer_id_business'))
    role = db.Column(db.String, nullable=False) # roles = ['employee', '_', 'admin']
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(40))
    location = db.Column(db.String(32))

    transaction_input_uploads = db.relationship('TransactionInput', backref='uploader', order_by='desc(TransactionInput.created_on)', lazy=True)

    created_accounts = db.relationship('Account', backref='creator', order_by='desc(Account.created_on)', lazy=True)
    created_businesses = db.relationship('Business', backref='creator', order_by="desc(Business.created_on)", primaryjoin="Business.created_by==User.id", post_update=True)
    created_items = db.relationship('Item', backref='creator', order_by='desc(Item.created_on)', lazy=True)
    created_distance_sales = db.relationship('DistanceSale', backref='creator', order_by='desc(DistanceSale.created_on)', lazy=True)
    created_tax_records = db.relationship('TaxRecord', backref='creator', order_by='desc(TaxRecord.created_on)', lazy=True)
    created_vat_thresholds = db.relationship('VatThreshold', backref='creator', order_by='desc(VatThreshold.created_on)', lazy=True)

    notifications = db.relationship('SellerFirmNotification', backref='user', lazy='select', primaryjoin='SellerFirmNotification.created_by==User.id')


    # downloaded_tax_records = db.relationship('TaxRecord', secondary=tax_record_user_AT, back_populates="downloaded_by_users")

    actions = db.relationship('Action', backref='user', order_by='desc(Action.timestamp)', lazy=True)

    u_type = db.Column(db.String(56))
    __mapper_args__ = {'polymorphic_on': u_type}

    @property
    def initials(self):
        return ''.join(name[0].upper() for name in self.name.split())

    @hybrid_property
    def employer_public_id(self):
        return self.employer.public_id

    @hybrid_property
    def employer_name(self):
        return self.employer.name


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        BCRYPT_LOG_ROUNDS = current_app.config.BCRYPT_LOG_ROUNDS
        self.password_hash = bcrypt.generate_password_hash(
            password, rounds=BCRYPT_LOG_ROUNDS).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def gravatar_hash(self):
        return md5(self.email.lower().encode('utf-8')).hexdigest()

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
        self.modified_at = datetime.utcnow()
        return self

    def update_last_seen(self):
        self.last_seen = datetime.utcnow()
        return self

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.avatar_hash = self.gravatar_hash()
        self.confirmed_on = None

    def __repr__(self):
        return '<User: {} | Type: {} | Role: {}>.'.format(self.email, self.u_type, self.role)




class Action(db.Model):  # type: ignore
    """ Action model """
    __tablename__ = "action"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    method_name = db.Column(db.String(32))
    service_context = db.Column(db.String(32))
