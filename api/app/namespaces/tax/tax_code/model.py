from app.extensions import db


class TaxCode(db.Model):  # type: ignore
    """ Item tax_code, e.g. A_GEN_STANDARD """
    __tablename__ = "tax_code"

    code = db.Column(db.String(8), primary_key=True)
    description = db.Column(db.String(128), nullable=False)
    countries = db.relationship('TaxRate', back_populates='tax_code')
    channels = db.relationship(
        "Channel",
        secondary=channel_tax_code_AT,
        back_populates="tax_codes"
    )
    items = db.relationship("Item", backref="tax_code", lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<TaxCode:{} valid from:{}>'.format(self.code, self.description)
