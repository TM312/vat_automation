
from app.extensions import db
from ..utils.ATs import channel_tax_code_AT

class Channel(db.Model):
    """ Channel model, i.e. codes: MFN, AFN """
    __tablename__ = "channel"

    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(64))
    platform_code = db.Column(db.String(8), db.ForeignKey('platform.code'))
    description = db.Column(db.String(256))
    accounts = db.relationship('Account', backref='channel', lazy=True)
    tax_codes = db.relationship(
        "TaxCode",
        secondary=channel_tax_code_AT,
        back_populates="channels"
    )
