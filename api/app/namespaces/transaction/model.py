from datetime import datetime

from app.extensions import db  # noqa


class TransactionType(db.Model):  # type: ignore
    """ Transaction model, i.e. SALE/REFUND/RETURN/ACQUISITION/MOVEMENT """
    __tablename__ = "transaction_type"

    code = db.Column(db.String(16), primary_key=True)
    description = db.Column(db.String(256))
    tax_treatments = db.relationship(
        'TaxTreatment', backref='transaction_type', lazy=True)

    def __init__(self, **kwargs):
        super(TransactionType, self).__init__(**kwargs)

    def __repr__(self):
        return '<TransactionType: {}>'.format(self.name)

class Bundle(db.Model):
    """ Bundle model """
    __tablename__ = "bundle"

    id = db.Column(db.Integer, primary_key=True)
    transactions = db.relationship('Transaction', backref='bundle', lazy=True)

    def __init__(self, **kwargs):
        super(Bundle, self).__init__(**kwargs)

    def __repr__(self):
        return '<Bundle: {}>'.format(self.id)


class Transaction(db.Model):  # type: ignore
    """ Transaction model """
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(128), nullable=False)
    activity_id = db.Column(db.String(128))
    bundle_id = db.Column(db.Integer, db.ForeignKey('bundle.id'), nullable=False)
    added_on = db.Column(db.DateTime, default=datetime.utcnow)
    #source = db.Column(db.String(128), nullable=False)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #User --> uploader

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    marketplace_name = db.Column(db.Integer, db.ForeignKey('marketplace.name'))

    item_id = db.Column(db.String(48), db.ForeignKey('item.id'))

    tax_treatment_code = db.Column(db.String(8), db.ForeignKey('tax_treatment.code'),
                                   nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)



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


    transaction_input = db.relationship('TransactionInput', uselist=False, back_populates='transaction')

    discriminator = db.Column('t_type', db.String(32)) #t_type: transaction_type
    __mapper_args__ = {'polymorphic_on': discriminator}

    def __repr__(self):
        return '<{}: id:{} – public_id:{} - added_on:{} uploader_id: {}>'.format(self.t_type, self.id, self.public_id, self.added_on, self.uploader_id)




class TransactionCalculationReference(db.Model):
       """ Calculation reference """
    __tablename__ = "transaction_calculation_reference"

    id = db.Column(db.Integer, primary_key=True)

    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    transaction = db.relationship("Transaction", back_populates="transaction_input")

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
    tax_jurisdiction_level = db.Column(db.String(32))

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
