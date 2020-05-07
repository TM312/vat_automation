from app.extensions import db


tax_treatment_transaction_type_AT = db.Table(
    'tax_treatment_transaction_type_AT',
    db.Column('tax_treatment_code', db.Integer, db.ForeignKey('tax_treatment.code'), primary_key=True),
    db.Column('transaction_type_code', db.Integer, db.ForeignKey('transaction_type.code'), primary_key=True)
    )


class TaxTreatment(db.Model):  # type: ignore
    """ Transaction model,  i.e. LOCAL_SALE, LOCAL_SALE_REVERSE_CHARGE, DISTANCE_SALE, INTRA_COMMUNITY_SALE, EXPORT, LOCAL_ACQUISITION, INTRA_COMMUNITY_ACQUISITION, IMPORT """

    __tablename__ = "tax_treatment"

    code = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(48), nullable=False)
    description = db.Column(db.String(512))


    transaction_type_codes = db.relationship(
        "TransactionType",
        secondary=tax_treatment_transaction_type_AT,
        back_populates="tax_treatments"
    )

    transactions = db.relationship(
        'Transaction', backref='tax_treatment', lazy=True)

    def __init__(self, **kwargs):
        super(TaxTreatment, self).__init__(**kwargs)

    def __repr__(self):
        return '<TaxTreatment: {} – {}>'.format(self.name, self.transaction_type_name)


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
