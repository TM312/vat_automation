from app.extensions import db


channel_tax_code_AT = db.Table(
    'channel_tax_code_AT',
    db.Column('channel_code', db.Integer, db.ForeignKey('channel.code'), primary_key=True),
    db.Column('tax_code_code', db.Integer, db.ForeignKey('tax_code.code'), primary_key=True)
    )


class Platform(db.Model):
    """ Platform model """
    __tablename__ = "platform"

    name = db.Column(db.String(32), primary_key=True)
    channels = db.relationship('Channel', backref='platform', lazy=True)

    __mapper_args__ = {'polymorphic_on': name}

    def __repr__(self):
        return '<Platform: {}>'.format(self.name)


class Channel(db.Model):
    """ Channel model, i.e. codes: MFN, AFN """
    __tablename__ = "channel"

    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    platform_name = db.Column(
        db.Integer, db.ForeignKey('platform.name'))
    description = db.Column(db.String(256))
    accounts = db.relationship('Account', backref='channel', lazy=True)
    marketplaces = db.relationship('Marketplace', backref='channel', lazy=True)
    tax_codes = db.relationship(
        "TaxCode",
        secondary=channel_tax_code_AT,
        back_populates="channels"
    )


    def __init__(self, **kwargs):
        super(Channel, self).__init__(**kwargs)


class Account(db.Model):
    """ Account model, e.g. Amazon --> MFN --> A2SC0NLSYTA68B (Unique Account Identifier) """
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(24), nullable=False)
    channel_code = db.Column(
        db.Integer, db.ForeignKey('channel.code'))
    seller_firm_id = db.Column(
        db.Integer, db.ForeignKey('business.id'))
    transactions = db.relationship(
        'Transaction', backref='account', lazy=True)

    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)


class Marketplace(db.Model):
    """ Marketplace model """
    __tablename__ = "marketplace"

    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    transactions = db.relationship(
        'Transaction', backref='marketplace', lazy=True)

    def __init__(self, **kwargs):
        super(Marketplace, self).__init__(**kwargs)
