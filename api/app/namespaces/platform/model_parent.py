from app.extensions import db


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
    channel_ids = db.relationship('ChannelID', backref='channel', lazy=True)
    marketplaces = db.relationship('Marketplace', backref='channel', lazy=True)

    def __init__(self, **kwargs):
        super(Channel, self).__init__(**kwargs)


class ChannelID(db.Model):
    """ ChannelID model """
    __tablename__ = "channel_id"

    id = db.Column(db.String(24), primary_key=True)
    channel_code = db.Column(
        db.Integer, db.ForeignKey('channel.code'))
    seller_firm_id = db.Column(
        db.Integer, db.ForeignKey('business.id'))
    transactions = db.relationship(
        'Transaction', backref='channel_id', lazy=True)

    def __init__(self, **kwargs):
        super(ChannelID, self).__init__(**kwargs)


class Marketplace(db.Model):
    """ Marketplace model """
    __tablename__ = "marketplace"

    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    transactions = db.relationship(
        'Transaction', backref='marketplace', lazy=True)

    def __init__(self, **kwargs):
        super(Marketplace, self).__init__(**kwargs)
