from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db  # noqa

from ..utils.ATs import tax_treatment_transaction_type_AT, tax_record_transaction_AT



class TransactionType(db.Model):  # type: ignore
    """ Transaction model, i.e. SALE/REFUND/RETURN/ACQUISITION/MOVEMENT """
    __tablename__ = "transaction_type"

    code = db.Column(db.String(32), primary_key=True)
    description = db.Column(db.String(128))

    tax_treatments = db.relationship(
        "TaxTreatment",
        secondary=tax_treatment_transaction_type_AT,
        back_populates="transaction_types"
     )

    def __repr__(self):
        return '<TransactionType: {}>'.format(self.code)


class Transaction(db.Model):  # type: ignore
    """ Transaction model """
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid4)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    tax_records = db.relationship('TaxRecord', secondary=tax_record_transaction_AT, back_populates='transactions')
    notifications = db.relationship('TransactionNotification', backref='transaction', order_by="desc(TransactionNotification.created_on)", lazy=True, cascade='all, delete-orphan')

    transaction_input_id = db.Column(db.Integer, db.ForeignKey('transaction_input.id'))
    # account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    # item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    type_code = db.Column(db.String(32), db.ForeignKey('transaction_type.code'), nullable=False)
    amazon_vat_calculation_service = db.Column(db.Boolean, nullable=False)

    customer_relationship_checked = db.Column(db.Boolean, nullable=False)
    customer_relationship = db.Column(db.String(16), nullable=False)
    customer_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    customer_firm_vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))

    tax_jurisdiction_code = db.Column(db.String(4), db.ForeignKey('country.code'), nullable=False)
    arrival_country_code = db.Column(db.String(4), db.ForeignKey('country.code'), nullable=False)
    departure_country_code = db.Column(db.String(4), db.ForeignKey('country.code'), nullable=False)


    tax_treatment_code = db.Column(db.String(40), db.ForeignKey('tax_treatment.code'), nullable=False)

    tax_date = db.Column(db.Date, nullable=False)
    tax_calculation_date = db.Column(db.Date, nullable=False)
    item_tax_code_code = db.Column(db.String(40), nullable=False)
    item_tax_rate_type_code = db.Column(db.String(8), db.ForeignKey('tax_rate_type.code'), nullable=False)
    shipment_tax_rate_type_code = db.Column(db.String(8), db.ForeignKey('tax_rate_type.code'), nullable=False)
    gift_wrap_tax_rate_type_code = db.Column(db.String(8), db.ForeignKey('tax_rate_type.code'), nullable=False)
    item_price_net = db.Column(db.Numeric(scale=2))
    item_price_discount_net = db.Column(db.Numeric(scale=2))
    item_price_total_net = db.Column(db.Numeric(scale=2))
    shipment_price_net = db.Column(db.Numeric(scale=2))
    shipment_price_discount_net = db.Column(db.Numeric(scale=2))
    shipment_price_total_net = db.Column(db.Numeric(scale=2))
    gift_wrap_price_net = db.Column(db.Numeric(scale=2))
    gift_wrap_price_discount_net = db.Column(db.Numeric(scale=2))
    gift_wrap_price_total_net = db.Column(db.Numeric(scale=2))
    item_price_vat_rate = db.Column(db.Numeric(scale=5))
    item_price_vat = db.Column(db.Numeric(scale=2))
    item_price_discount_vat = db.Column(db.Numeric(scale=2))
    item_price_total_vat = db.Column(db.Numeric(scale=2))
    shipment_price_vat_rate = db.Column(db.Numeric(scale=5))
    shipment_price_vat = db.Column(db.Numeric(scale=2))
    shipment_price_discount_vat = db.Column(db.Numeric(scale=2))
    shipment_price_total_vat = db.Column(db.Numeric(scale=2))
    gift_wrap_price_vat_rate = db.Column(db.Numeric(scale=5))
    gift_wrap_price_vat = db.Column(db.Numeric(scale=2))
    gift_wrap_price_discount_vat = db.Column(db.Numeric(scale=2))
    gift_wrap_price_total_vat = db.Column(db.Numeric(scale=2))
    total_value_net = db.Column(db.Numeric(scale=2))
    total_value_vat = db.Column(db.Numeric(scale=2))
    total_value_gross = db.Column(db.Numeric(scale=2))
    transaction_currency_code = db.Column(db.String(8), db.ForeignKey('currency.code'), nullable=False)
    invoice_currency_code = db.Column(db.String(8), db.ForeignKey('currency.code'))
    invoice_exchange_rate_date = db.Column(db.Date)
    invoice_exchange_rate = db.Column(db.Numeric(scale=5))
    invoice_amount_net = db.Column(db.Numeric(scale=2))
    invoice_amount_vat = db.Column(db.Numeric(scale=2))
    invoice_amount_gross = db.Column(db.Numeric(scale=2))
    vat_rate_reverse_charge = db.Column(db.Numeric(scale=2))
    invoice_amount_vat_reverse_charge = db.Column(db.Numeric(scale=2))
    arrival_seller_vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))
    departure_seller_vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))
    seller_vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))



    def __repr__(self):
        return '<Transaction {}: Created On: {} | Type: {} | Tax Treatment: {}>'.format(self.id, self.created_on, self.type_code, self.tax_treatment_code)


#### ENUM ???ß
