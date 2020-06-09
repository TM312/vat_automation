from app.extensions import db
from ...utils.ATs import tax_treatment_transaction_type_AT



class TaxTreatment(db.Model):  # type: ignore
    """ Transaction model,  i.e. LOCAL_SALE, LOCAL_SALE_REVERSE_CHARGE, DISTANCE_SALE, INTRA_COMMUNITY_SALE, EXPORT, LOCAL_ACQUISITION, INTRA_COMMUNITY_ACQUISITION, IMPORT """

    __tablename__ = "tax_treatment"

    code = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(48), nullable=False)
    description = db.Column(db.String(512))


    transaction_types = db.relationship(
        "TransactionType",
        secondary=tax_treatment_transaction_type_AT,
        back_populates="tax_treatments"
    )

    transactions = db.relationship('Transaction', backref='tax_treatment', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<TaxTreatment: {}>'.format(self.code)


# Transaction Type --> TaxTreatment
# SALE
#   LOCAL SALE
# 	LOCAL SALE REVERSE CHARGE
# 	DISTANCE SALE
# 	INTRA-COMMUNITY SALE
# 	EXPORT
# REFUND
#   LOCAL SALE
# 	LOCAL SALE REVERSE CHARGE
# 	DISTANCE SALE
# 	INTRA-COMMUNITY SALE
# 	EXPORT
# ACQUISITION
#   LOCAL ACQUISITION
# 	INTRA-COMMUNITY ACQUISITION
# 	IMPORT
# MOVEMENT
#   INTRA-COMMUNITY SALE
# 	EXPORT
# 	INTRA-COMMUNITY ACQUISITION
# 	IMPORT
