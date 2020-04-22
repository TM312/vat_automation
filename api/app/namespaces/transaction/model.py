import datetime

from app.extensions import db  # noqa


class TransactionType(db.Model):  # type: ignore
    """ Transaction model, i.e. Sale/Refund/Return/Acquisition/Movement """
    __tablename__ = "transaction_type"

    name = db.Column(db.String(16), primary_key=True)
    tax_treatments = db.relationship(
        'TaxTreatment', backref='transaction_type', lazy=True)

    def __init__(self, **kwargs):
        super(TransactionType, self).__init__(**kwargs)

    def __repr__(self):
        return '<TransactionType: {}>'.format(self.name)



class TaxTreatment(db.Model):  # type: ignore
    """ Transaction model,  i.e. locale sale/locale sale reverse charge/ ..."""
    __tablename__ = "tax_treatment"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    transaction_type_name = db.Column(db.String(16), db.ForeignKey('transaction_type.name'),
              nullable=False)
    transactions = db.relationship(
        'Transaction', backref='transaction_customer_type', lazy=True)

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


class TransactionCustomerType(db.Model):  # type: ignore
    """ TransactionCustomerType model: i.e. B2B / B2C """
    __tablename__ = "transaction_customer_type"

    name = db.Column(db.String(8), primary_key=True)
    transactions = db.relationship(
        'Transaction', backref='transaction_customer_type', lazy=True)

    def __init__(self, **kwargs):
        super(TaxTreatment, self).__init__(**kwargs)

    def __repr__(self):
        return '<TaxTreatment: {} – {}>'.format(self.name, self.transaction_type_name)



class Transaction(db.Model):  # type: ignore
    """ Transaction model """
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(128), nullable=False)

    added_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    source = added_on = db.Column(db.String(128), nullable=False)

    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    accounting_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                         nullable=False) # owner is always a seller_firm


    tax_treatment_name = db.Column(db.String(8), db.ForeignKey('tax_treatment.name'),
                                   nullable=False)

    unique_account_id_id = db.Column(db.Integer, db.ForeignKey('unique_account_id.id'))

    marketplace_name = db.Column(db.Integer, db.ForeignKey('marketplace.name'))


    tax_calculation_date = db.Column(db.Date)
    arrival_date = db.Column(db.Date)
    shipment_date = db.Column(db.Date)
    tax_date = db.Column(db.Date)

    item_id = db.Column(db.String(48), db.ForeignKey('item.id'))

    quantity = db.Column(db.Integer, default=1)


    discriminator = db.Column('t_type', db.String(32)) #t_type: transaction_type
    __mapper_args__ = {'polymorphic_on': discriminator}

    def __repr__(self):
        return '<{}: id:{} – public_id:{} - added_on:{} uploader_id: {}>'.format(self.t_type, self.id, self.public_id, self.added_on, self.uploader_id)



    class Sale(Transaction):
        __mapper_args__ = {'polymorphic_identity': 'sale'}

        shipment_id = db.Column(db.String(128))


        customer_type_name = db.Column(db.String(8), db.ForeignKey('transaction_customer_type.name'),
                                       nullable=False)


    def __init__(self, **kwargs):
        super(Sale, self).__init__(**kwargs)



    class Return(Transaction):
        __mapper_args__ = {'polymorphic_identity': 'return'}

        return_id = db.Column(db.String(128))


    def __init__(self, **kwargs):
        super(Return, self).__init__(**kwargs)




class Refund(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'refund'}

    refund_id = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(Refund, self).__init__(**kwargs)




class Movement(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'movement'}

    movement_id = db.Column(db.String(128))


    def __init__(self, **kwargs):
        super(Movement, self).__init__(**kwargs)




    class Acquisition(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'acquisition'}

    acquisition_id = db.Column(db.String(128))


    def __init__(self, **kwargs):
        super(Acquisition, self).__init__(**kwargs)
