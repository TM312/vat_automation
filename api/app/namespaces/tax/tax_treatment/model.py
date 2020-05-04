from app.extensions import db

class TaxTreatment(db.Model):  # type: ignore
    """ Transaction model,  i.e. LOCAL_SALE, LOCAL_SALE_REVERSE_CHARGE, DISTANCE_SALE, INTRA_COMMUNITY_SALE, EXPORT, LOCAL_ACQUISITION, INTRA_COMMUNITY_ACQUISITION, IMPORT """

    __tablename__ = "tax_treatment"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(256))
    transaction_type_code = db.Column(db.String(16), db.ForeignKey('transaction_type.code'),
                                      nullable=False)
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
