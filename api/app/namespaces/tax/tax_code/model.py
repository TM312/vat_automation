from app.extensions import db
from ...utils.ATs import channel_tax_code_AT


class TaxCode(db.Model):  # type: ignore
    """ Item tax_code, e.g. A_GEN_STANDARD """
    __tablename__ = "tax_code"

    code = db.Column(db.String(40), primary_key=True)
    description = db.Column(db.String(128), nullable=False)
    #countries = db.relationship('Vat', back_populates='tax_code')
    channels = db.relationship(
        "Channel",
        secondary=channel_tax_code_AT,
        back_populates="tax_codes"
    )
    items = db.relationship("Item", backref="tax_code", lazy=True)
    vats = db.relationship('Vat', backref='tax_code', lazy=True)


    def __repr__(self):
        return '<TaxCode:{} valid from:{}>'.format(self.code, self.description)
