
from app.extensions import db


channel_tax_code_AT = db.Table(
    'channel_tax_code_AT',
    db.Column('channel_code', db.Integer, db.ForeignKey('channel.code'), primary_key=True),
    db.Column('tax_code_code', db.Integer, db.ForeignKey('tax_code.code'), primary_key=True)
    )


class Channel(db.Model):
    """ Channel model, i.e. codes: MFN, AFN """
    __tablename__ = "channel"

    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    platform_code = db.Column(db.Integer, db.ForeignKey('platform.code'))
    description = db.Column(db.String(256))
    accounts = db.relationship('Account', backref='channel', lazy=True)
    marketplaces = db.relationship('Marketplace', backref='channel', lazy=True)
    tax_codes = db.relationship(
        "TaxCode",
        secondary=channel_tax_code_AT,
        back_populates="channels"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
