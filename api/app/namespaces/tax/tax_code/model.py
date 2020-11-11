from app.extensions import db
from app.namespaces.utils.ATs import channel_tax_code_AT


class TaxCode(db.Model):  # type: ignore
    """ Item tax_code, e.g. A_GEN_STANDARD """
    __tablename__ = "tax_code"

    code = db.Column(db.String(40), primary_key=True)
    description = db.Column(db.String(128), nullable=False)
    channels = db.relationship(
        "Channel",
        secondary=channel_tax_code_AT,
        back_populates="tax_codes"
    )
    items = db.relationship("Item", backref="tax_code", lazy=True)
    vats = db.relationship('Vat', backref='tax_code', lazy=True)


    def __repr__(self):
        return '<TaxCode:{}>'.format(self.code)


    def update(self, data_changes):
        for key, val in data_changes.items():
            if key.lower() != 'code':
                setattr(self, key, val)
        return self
