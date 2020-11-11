
from app.extensions import db
from app.namespaces.utils.ATs import channel_tax_code_AT

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

    def __repr__(self):
        return '<Channel: {} - {}>'.format(self.code, self.name)


    def update(self, data_changes):
        for key, val in data_changes.items():
            if key.lower() != 'code':
                setattr(self, key, val)
        return self
