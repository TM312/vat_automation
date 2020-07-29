from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
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
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    # account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

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
    _item_price_net = db.Column(db.Integer)
    _item_price_discount_net = db.Column(db.Integer)
    _item_price_total_net = db.Column(db.Integer)
    _shipment_price_net = db.Column(db.Integer)
    _shipment_price_discount_net = db.Column(db.Integer)
    _shipment_price_total_net = db.Column(db.Integer)
    _gift_wrap_price_net = db.Column(db.Integer)
    _gift_wrap_price_discount_net = db.Column(db.Integer)
    _gift_wrap_price_total_net = db.Column(db.Integer)
    _item_price_vat_rate = db.Column(db.Integer)
    _item_price_vat = db.Column(db.Integer)
    _item_price_discount_vat = db.Column(db.Integer)
    _item_price_total_vat = db.Column(db.Integer)
    _shipment_price_vat_rate = db.Column(db.Integer)
    _shipment_price_vat = db.Column(db.Integer)
    _shipment_price_discount_vat = db.Column(db.Integer)
    _shipment_price_total_vat = db.Column(db.Integer)
    _gift_wrap_price_vat_rate = db.Column(db.Integer)
    _gift_wrap_price_vat = db.Column(db.Integer)
    _gift_wrap_price_discount_vat = db.Column(db.Integer)
    _gift_wrap_price_total_vat = db.Column(db.Integer)
    _total_value_net = db.Column(db.Integer)
    _total_value_vat = db.Column(db.Integer)
    _total_value_gross = db.Column(db.Integer)
    transaction_currency_code = db.Column(db.String(8), db.ForeignKey('currency.code'), nullable=False)
    invoice_currency_code = db.Column(db.String(8), db.ForeignKey('currency.code'))
    invoice_exchange_rate_date = db.Column(db.Date)
    _invoice_exchange_rate = db.Column(db.Integer)
    _invoice_amount_net = db.Column(db.Integer)
    _invoice_amount_vat = db.Column(db.Integer)
    _invoice_amount_gross = db.Column(db.Integer)
    _vat_rate_reverse_charge = db.Column(db.Integer)
    _invoice_amount_vat_reverse_charge = db.Column(db.Integer)
    arrival_seller_vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))
    departure_seller_vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))
    seller_vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))

    #cent values
    @hybrid_property
    def item_price_net(self):
        return self._item_price_net / 100

    @item_price_net.setter
    def item_price_net(self, value):
        self._item_price_net = int(value * 100)

    @hybrid_property
    def item_price_discount_net(self):
        return self._item_price_discount_net / 100

    @item_price_discount_net.setter
    def item_price_discount_net(self, value):
        self._item_price_discount_net = int(value * 100)

    @hybrid_property
    def item_price_total_net(self):
        return self._item_price_total_net / 100

    @item_price_total_net.setter
    def item_price_total_net(self, value):
        self._item_price_total_net = int(value * 100)

    @hybrid_property
    def shipment_price_net(self):
        return self._shipment_price_net / 100

    @shipment_price_net.setter
    def shipment_price_net(self, value):
        self._shipment_price_net = int(value * 100)

    @hybrid_property
    def shipment_price_discount_net(self):
        return self._shipment_price_discount_net / 100

    @shipment_price_discount_net.setter
    def shipment_price_discount_net(self, value):
        self._shipment_price_discount_net = int(value * 100)

    @hybrid_property
    def shipment_price_total_net(self):
        return self._shipment_price_total_net / 100

    @shipment_price_total_net.setter
    def shipment_price_total_net(self, value):
        self._shipment_price_total_net = int(value * 100)

    @hybrid_property
    def gift_wrap_price_net(self):
        return self._gift_wrap_price_net / 100

    @gift_wrap_price_net.setter
    def gift_wrap_price_net(self, value):
        self._gift_wrap_price_net = int(value * 100)

    @hybrid_property
    def gift_wrap_price_discount_net(self):
        return self._gift_wrap_price_discount_net / 100

    @gift_wrap_price_discount_net.setter
    def gift_wrap_price_discount_net(self, value):
        self._gift_wrap_price_discount_net = int(value * 100)

    @hybrid_property
    def gift_wrap_price_total_net(self):
        return self._gift_wrap_price_total_net / 100

    @gift_wrap_price_total_net.setter
    def gift_wrap_price_total_net(self, value):
        self._gift_wrap_price_total_net = int(value * 100)

    @hybrid_property
    def item_price_vat(self):
        return self._item_price_vat / 100

    @item_price_vat.setter
    def item_price_vat(self, value):
        self._item_price_vat = int(value * 100)

    @hybrid_property
    def item_price_discount_vat(self):
        return self._item_price_discount_vat / 100

    @item_price_discount_vat.setter
    def item_price_discount_vat(self, value):
        self._item_price_discount_vat = int(value * 100)

    @hybrid_property
    def item_price_total_vat(self):
        return self._item_price_total_vat / 100

    @item_price_total_vat.setter
    def item_price_total_vat(self, value):
        self._item_price_total_vat = int(value * 100)

    @hybrid_property
    def shipment_price_vat(self):
        return self._shipment_price_vat / 100

    @shipment_price_vat.setter
    def shipment_price_vat(self, value):
        self._shipment_price_vat = int(value * 100)

    @hybrid_property
    def shipment_price_discount_vat(self):
        return self._shipment_price_discount_vat / 100

    @shipment_price_discount_vat.setter
    def shipment_price_discount_vat(self, value):
        self._shipment_price_discount_vat = int(value * 100)

    @hybrid_property
    def shipment_price_total_vat(self):
        return self._shipment_price_total_vat / 100

    @shipment_price_total_vat.setter
    def shipment_price_total_vat(self, value):
        self._shipment_price_total_vat = int(value * 100)

    @hybrid_property
    def gift_wrap_price_vat(self):
        return self._gift_wrap_price_vat / 100

    @gift_wrap_price_vat.setter
    def gift_wrap_price_vat(self, value):
        self._gift_wrap_price_vat = int(value * 100)

    @hybrid_property
    def gift_wrap_price_discount_vat(self):
        return self._gift_wrap_price_discount_vat / 100

    @gift_wrap_price_discount_vat.setter
    def gift_wrap_price_discount_vat(self, value):
        self._gift_wrap_price_discount_vat = int(value * 100)

    @hybrid_property
    def gift_wrap_price_total_vat(self):
        return self._gift_wrap_price_total_vat / 100

    @gift_wrap_price_total_vat.setter
    def gift_wrap_price_total_vat(self, value):
        self._gift_wrap_price_total_vat = int(value * 100)

    @hybrid_property
    def total_value_net(self):
        return self._total_value_net / 100

    @total_value_net.setter
    def total_value_net(self, value):
        self._total_value_net = int(value * 100)

    @hybrid_property
    def total_value_vat(self):
        return self._total_value_vat / 100

    @total_value_vat.setter
    def total_value_vat(self, value):
        self._total_value_vat = int(value * 100)

    @hybrid_property
    def total_value_gross(self):
        return self._total_value_gross / 100

    @total_value_gross.setter
    def total_value_gross(self, value):
        self._total_value_gross = int(value * 100)

    @hybrid_property
    def invoice_amount_net(self):
        return self._invoice_amount_net / 100

    @invoice_amount_net.setter
    def invoice_amount_net(self, value):
        self._invoice_amount_net = int(value * 100)

    @hybrid_property
    def invoice_amount_vat(self):
        return self._invoice_amount_vat / 100

    @invoice_amount_vat.setter
    def invoice_amount_vat(self, value):
        self._invoice_amount_vat = int(value * 100)

    @hybrid_property
    def invoice_amount_gross(self):
        return self._invoice_amount_gross / 100

    @invoice_amount_gross.setter
    def invoice_amount_gross(self, value):
        self._invoice_amount_gross = int(value * 100)

    @hybrid_property
    def vat_rate_reverse_charge(self):
        return self._vat_rate_reverse_charge / 100

    @vat_rate_reverse_charge.setter
    def vat_rate_reverse_charge(self, value):
        self._vat_rate_reverse_charge = int(value * 100)


    @hybrid_property
    def invoice_amount_vat_reverse_charge(self):
        return self._invoice_amount_vat_reverse_charge / 100

    @invoice_amount_vat_reverse_charge.setter
    def invoice_amount_vat_reverse_charge(self, value):
        self._invoice_amount_vat_reverse_charge = int(value * 100)



    #rates
    @hybrid_property
    def item_price_vat_rate(self):
        return self._item_price_vat_rate / 10_000

    @item_price_vat_rate.setter
    def item_price_vat_rate(self, value):
        self._item_price_vat_rate = int(value * 10_000)

    @hybrid_property
    def shipment_price_vat_rate(self):
        return self._shipment_price_vat_rate / 10_000

    @shipment_price_vat_rate.setter
    def shipment_price_vat_rate(self, value):
        self._shipment_price_vat_rate = int(value * 10_000)

    @hybrid_property
    def gift_wrap_price_vat_rate(self):
        return self._gift_wrap_price_vat_rate / 10_000

    @gift_wrap_price_vat_rate.setter
    def gift_wrap_price_vat_rate(self, value):
        self._gift_wrap_price_vat_rate = int(value * 10_000)

    @hybrid_property
    def invoice_exchange_rate(self):
        return self._invoice_exchange_rate / 10_000

    @invoice_exchange_rate.setter
    def invoice_exchange_rate(self, value):
        self._invoice_exchange_rate = int(value * 10_000)




















    def __repr__(self):
        return '<Transaction {}: Created On: {} | Type: {} | Tax Treatment: {}>'.format(self.id, self.created_on, self.type_code, self.tax_treatment_code)


#### ENUM ???ß
