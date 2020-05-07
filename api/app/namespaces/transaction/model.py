from datetime import datetime

from app.extensions import db  # noqa


class TransactionType(db.Model):  # type: ignore
    """ Transaction model, i.e. SALE/REFUND/RETURN/ACQUISITION/MOVEMENT """
    __tablename__ = "transaction_type"

    code = db.Column(db.String(16), primary_key=True)
    description = db.Column(db.String(128))

    tax_treatment_codes = db.relationship(
        "TaxTreatment",
         secondary=tax_treatment_transaction_type_AT,
        back_populates="transaction_types"
     )

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
    bundle_id = db.Column(db.Integer, db.ForeignKey('bundle.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    transaction_input_id = db.Column(db.Integer, db.ForeignKey('transaction_input.id'))
    transaction_input = db.relationship("TransactionInput", back_populates="transaction")

    tax_treatment_code = db.Column(db.String(8), db.ForeignKey('tax_treatment.code'), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    marketplace_name = db.Column(db.Integer, db.ForeignKey('marketplace.name'))
    public_id = db.Column(db.String(128), nullable=False)
    activity_id = db.Column(db.String(128), nullable=False)

    item_id = db.Column(db.String(48), db.ForeignKey('item.id'), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    transaction_type_code = db.Column(db.String(8))

    item_quantity = db.Column(db.Integer, default=1)

    shipment_date = db.Column(db.Date)
    tax_date = db.Column(db.Date)
    arrival_date = db.Column(db.Date)

    arrival_country_code = db.Column(db.String(4), db.ForeignKey('country.code'))
    arrival_postal_code = db.Column(db.String(16))
    arrival_city = db.Column(db.String(256))
    arrival_address = db.Column(db.String(256))

    currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)








    tax_calculation_date = db.Column(db.Date)
    item_price_discount_net = db.Column(db.Float(precision=24))
    item_price_discount_vat = db.Column(db.Float(precision=24))
    item_price_net = db.Column(db.Float(precision=24))
    item_price_vat = db.Column(db.Float(precision=24))
    item_price_total_net = db.Column(db.Float(precision=24))
    item_price_total_vat = db.Column(db.Float(precision=24))
    item_price_tax_rate_rate = db.Column(db.Float(precision=24))
    shipment_price_discount_net = db.Column(db.Float(precision=24))
    shipment_price_discount_vat = db.Column(db.Float(precision=24))
    shipment_price_net = db.Column(db.Float(precision=24))
    shipment_price_vat = db.Column(db.Float(precision=24))
    shipment_price_total_net = db.Column(db.Float(precision=24))
    shipment_price_total_vat = db.Column(db.Float(precision=24))
    shipment_price_tax_rate_rate = db.Column(db.Float(precision=24))
    sale_total_value_net = db.Column(db.Float(precision=24))
    sale_total_value_vat = db.Column(db.Float(precision=24))
    gift_wrap_price_discount_net = db.Column(db.Float(precision=24))
    gift_wrap_price_discount_vat = db.Column(db.Float(precision=24))
    gift_wrap_price_net = db.Column(db.Float(precision=24))
    gift_wrap_price_vat = db.Column(db.Float(precision=24))
    gift_wrap_price_total_net = db.Column(db.Float(precision=24))
    gift_wrap_price_total_vat = db.Column(db.Float(precision=24))
    gift_wrap_price_tax_rate = db.Column(db.Float(precision=24))
    item_tax_code_code = db.Column(db.String(8))
    departure_seller_vat_country_code = db.Column(db.String(8))
    departure_seller_vat_number = db.Column(db.String(24))
    arrival_seller_vat_country_code = db.Column(db.String(8))
    arrival_seller_vat_number = db.Column(db.String(24))
    seller_vat_country_code = db.Column(db.String(8))
    seller_vat_number = db.Column(db.String(24))
    tax_calculation_imputation_country = db.Column(db.String(24))
    tax_jurisdiction = db.Column(db.String(24))
    tax_jurisdiction_level = db.Column(db.String(24))
    invoice_amount_vat = db.Column(db.Float(precision=24))
    invoice_currency_code = db.Column(db.String(8))
    invoice_exchange_rate = db.Column(db.Float(precision=24))
    invoice_exchange_rate_date = db.Column(db.Date)
    export = db.Column(db.Boolean)



    def __repr__(self):
        return '<{}: id:{} – public_id:{} - created_on:{}>'.format(self.transaction_type_code, self.id, self.public_id, self.created_on)



#### ENUM ???ß
