
from app.extensions import db
from app.namespaces.utils.ATs import tax_treatment_transaction_type_AT


class TransactionType(db.Model):  # type: ignore
    """ Transaction model, i.e. SALE/REFUND/RETURN/ACQUISITION/MOVEMENT """
    __tablename__ = "transaction_type"

    code = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(128))

    tax_treatments = db.relationship(
        "TaxTreatment",
        secondary=tax_treatment_transaction_type_AT,
        back_populates="transaction_types"
    )

    transaction_types_public = db.relationship('TransactionTypePublic', backref='transaction_type', lazy=True)

    def __repr__(self):
        return '<TransactionType: {}>'.format(self.code)
