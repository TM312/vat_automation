import datetime

from app.extensions import db  # noqa


class TransactionType(db.Model):  # type: ignore
    """ Transaction model, i.e. Sale/Refund/Return/Acquisition/Movement """
    __tablename__ = "transaction_type"

    name = db.Column(db.String(16), primary_key=True)
    description = db.Column(db.String(256))
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
    description = db.Column(db.String(256))
    transaction_type_name = db.Column(db.String(16), db.ForeignKey('transaction_type.name'),
              nullable=False)
    transactions = db.relationship(
        'Transaction', backref='customer_type', lazy=True)

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


class Transaction(db.Model):  # type: ignore
    """ Transaction model """
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(128), nullable=False)

    added_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    source = db.Column(db.String(128), nullable=False)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #User --> uploader

    # accounting_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'))

    owner_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                         nullable=False) # owner is always a seller_firm


    tax_treatment_name = db.Column(db.String(8), db.ForeignKey('tax_treatment.name'),
                                   nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    marketplace_name = db.Column(db.Integer, db.ForeignKey('marketplace.name'))

    customer_id = db.relationship(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    item_id = db.Column(db.String(48), db.ForeignKey('item.id'))

    item_quantity = db.Column(db.Integer, default=1)


    tax_calculation_date = db.Column(db.Date)

    shipment_date = db.Column(db.Date)
    tax_date = db.Column(db.Date)
    arrival_date = db.Column(db.Date)

    arrival_country_code = db.Column(db.String(4), db.ForeignKey('country.code'))
    arrival_postal_code = db.Column(db.String(16))
    arrival_city = db.Column(db.String(256))
    arrival_address = db.Column(db.String(256))

    currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'),
                              nullable=False)


    transaction_calculation_reference = db.relationship('TransactionCalculationReference', uselist=False, back_populates='transaction')

    discriminator = db.Column('t_type', db.String(32)) #t_type: transaction_type
    __mapper_args__ = {'polymorphic_on': discriminator}

    def __repr__(self):
        return '<{}: id:{} – public_id:{} - added_on:{} uploader_id: {}>'.format(self.t_type, self.id, self.public_id, self.added_on, self.uploader_id)


"TRANSACTION_EVENT_ID" - -> transaction.public_id
"ACTIVITY_TRANSACTION_ID" - -> transaction.shipment_id
"TAX_CALCULATION_DATE" - -> transaction.tax_calculation_date

"TRANSACTION_DEPART_DATE" - -> transaction.shipment_date
"TRANSACTION_COMPLETE_DATE" - -> transaction.tax_date

new_sale_transaction = Sale(
    shipment_id=user.id,
    accounting_firm_id=user.employer_id,
    activity_period=activity_period,
    owner_id=seller_firm.id,
    storage_dir=final_dirpath,
)




class TransactionCalculationReference(db.Model):
       """ Calculation reference """
    __tablename__ = "transaction_calculation_reference"

    id = db.Column(db.Integer, primary_key=True)

    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    transaction = db.relationship("Transaction", back_populates="transaction_calculation_reference")
    export = db.Column(db.String(8))
    tax_code = db.Column(db.String(8))

    arrival_seller_vat_number = db.Column(db.String(48))
    arrival_seller_vat_number_country = db.Column(db.String(8))

    departure_seller_vat_number = db.Column(db.String(48))
    departure_seller_vat_number_country = db.Column(db.String(8))

    seller_vat_number = db.Column(db.String(40))
    seller_vat_number_country = db.Column(db.String(8))

    invoice_amount_vat = db.Column(db.Float())
    invoice_currency_code = db.Column(db.String(8))
    invoice_exchange_rate = db.Column(db.Float())
    invoice_exchange_rate_date = db.Column(db.Date())

    gift_wrap_price_discount_net = db.Column(db.Float())
    gift_wrap_price_discount_vat = db.Column(db.Float())
    gift_wrap_price_net = db.Column(db.Float())
    gift_wrap_price_vat = db.Column(db.Float())
    gift_wrap_price_total_net = db.Column(db.Float())
    gift_wrap_price_total_vat = db.Column(db.Float())
    gift_wrap_price_vat_rate = db.Column(db.Float())

    item_price_discount_net = db.Column(db.Float())
    item_price_discount_vat = db.Column(db.Float())
    item_price_net = db.Column(db.Float())
    item_price_vat = db.Column(db.Float())
    item_price_total_net = db.Column(db.Float())
    item_price_total_vat = db.Column(db.Float())
    item_price_vat_rate = db.Column(db.Float())

    shipment_price_discount_net = db.Column(db.Float())
    shipment_price_discount_vat = db.Column(db.Float())
    shipment_price_net = db.Column(db.Float())
    shipment_price_vat = db.Column(db.Float())
    shipment_price_total_net = db.Column(db.Float())
    shipment_price_total_vat = db.Column(db.Float())
    shipment_price_vat_rate = db.Column(db.Float())

    sale_total_value_net = db.Column(db.Float())
    sale_total_value_vat = db.Column(db.Float())

    tax_jurisdiction = db.Column(db.String(40))
    tax_jurisdiction_level = db.Column(db.String(40))

    vat_calculation_imputation_country = db.Column(db.String(8))



    def __init__(self, **kwargs):
        super(TransactionCalculationReference, self).__init__(**kwargs)






class Sale(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'sale'}

    shipment_id = db.Column(db.String(128))



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
