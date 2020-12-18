from datetime import datetime
from uuid import uuid4

from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property


class TransactionInput(db.Model):
    """ TransactionInput model """
    __tablename__ = "transaction_input"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid4)
    original_filename = db.Column(db.String(128))
    bundle_id = db.Column(db.Integer, db.ForeignKey('bundle.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id')) #User --> uploader
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    processed = db.Column(db.Boolean, default=False)
    processed_on = db.Column(db.DateTime)
    transactions = db.relationship('Transaction', backref='transaction_input', lazy=True, cascade='all, delete-orphan')

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account_given_id = db.Column(db.String(128), nullable=False)
    public_activity_period = db.Column(db.String(64))
    channel_code = db.Column(db.String(64))
    marketplace = db.Column(db.String(128))
    transaction_type_public_code = db.Column(db.String(40))
    given_id = db.Column(db.String(64))
    activity_id = db.Column(db.String(64))
    shipment_date = db.Column(db.Date)
    arrival_date = db.Column(db.Date)
    complete_date = db.Column(db.Date)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item_sku = db.Column(db.String(128))
    item_asin = db.Column(db.String(64))
    item_name = db.Column(db.String(256))
    item_manufacture_country = db.Column(db.String(128))
    item_quantity = db.Column(db.Integer)
    item_weight_g = db.Column(db.Integer)
    item_weight_g_total = db.Column(db.Integer)

    _item_price_discount_gross = db.Column(db.Integer, default=0)
    _item_price_gross = db.Column(db.Integer, default=0)
    _item_price_total_gross = db.Column(db.Integer, default=0)
    _shipment_price_discount_gross = db.Column(db.Integer, default=0)
    _shipment_price_gross = db.Column(db.Integer, default=0)
    _shipment_price_total_gross = db.Column(db.Integer, default=0)
    _sale_total_value_gross = db.Column(db.Integer, default=0)
    _gift_wrap_price_discount_gross = db.Column(db.Integer, default=0)
    _gift_wrap_price_gross = db.Column(db.Integer, default=0)
    _gift_wrap_price_total_gross = db.Column(db.Integer, default=0)
    currency_code = db.Column(db.String(8), db.ForeignKey('currency.code'))
    departure_country_code = db.Column(db.String(8), db.ForeignKey('country.code'))
    departure_postal_code = db.Column(db.String(24))
    departure_city = db.Column(db.String(128))
    arrival_country_code = db.Column(db.String(8), db.ForeignKey('country.code'))
    arrival_postal_code = db.Column(db.String(24))
    arrival_city = db.Column(db.String(128))
    arrival_address = db.Column(db.String(128))

    sale_departure_country_code = db.Column(db.String(8))
    sale_arrival_country_code = db.Column(db.String(8))

    shipment_mode = db.Column(db.String(64))
    shipment_conditions = db.Column(db.String(24))
    invoice_number = db.Column(db.String(64))
    invoice_url = db.Column(db.String(256))
    customer_name = db.Column(db.String(64))
    customer_vat_number = db.Column(db.String(24))
    customer_vat_number_country_code = db.Column(db.String(8))
    supplier_vat_number = db.Column(db.String(24))
    supplier_name = db.Column(db.String(128))

    tax_calculation_date = db.Column(db.Date)
    _unit_cost_price_net = db.Column(db.Integer, default=0)

    _item_price_discount_net = db.Column(db.Integer, default=0)
    _item_price_discount_vat = db.Column(db.Integer, default=0)
    _item_price_net = db.Column(db.Integer, default=0)
    _item_price_vat = db.Column(db.Integer, default=0)
    _item_price_total_net = db.Column(db.Integer, default=0)
    _item_price_total_vat = db.Column(db.Integer, default=0)
    _item_price_vat_rate = db.Column(db.Integer, default=0)
    _shipment_price_discount_net = db.Column(db.Integer, default=0)
    _shipment_price_discount_vat = db.Column(db.Integer, default=0)
    _shipment_price_net = db.Column(db.Integer, default=0)
    _shipment_price_vat = db.Column(db.Integer, default=0)
    _shipment_price_total_net = db.Column(db.Integer, default=0)
    _shipment_price_total_vat = db.Column(db.Integer, default=0)
    _shipment_price_vat_rate = db.Column(db.Integer, default=0)
    _sale_total_value_net = db.Column(db.Integer, default=0)
    _sale_total_value_vat = db.Column(db.Integer, default=0)
    _gift_wrap_price_discount_net = db.Column(db.Integer, default=0)
    _gift_wrap_price_discount_vat = db.Column(db.Integer, default=0)
    _gift_wrap_price_net = db.Column(db.Integer, default=0)
    _gift_wrap_price_vat = db.Column(db.Integer, default=0)
    _gift_wrap_price_total_net = db.Column(db.Integer, default=0)
    _gift_wrap_price_total_vat = db.Column(db.Integer, default=0)
    _gift_wrap_price_tax_rate = db.Column(db.Integer, default=0)
    item_given_tax_code_code = db.Column(db.String(40))
    departure_seller_vat_country_code = db.Column(db.String(8))
    departure_seller_vat_number = db.Column(db.String(24))
    arrival_seller_vat_country_code = db.Column(db.String(8))
    arrival_seller_vat_number = db.Column(db.String(24))
    seller_vat_country_code = db.Column(db.String(8))
    seller_vat_number = db.Column(db.String(24))
    tax_calculation_imputation_country = db.Column(db.String(24))
    tax_jurisdiction = db.Column(db.String(24))
    tax_jurisdiction_level = db.Column(db.String(24))
    _invoice_amount_vat = db.Column(db.Integer)
    invoice_currency_code = db.Column(db.String(8))
    _invoice_exchange_rate = db.Column(db.Integer)
    invoice_exchange_rate_date = db.Column(db.Date)
    export = db.Column(db.Boolean)

    #weights
    @hybrid_property
    def item_weight_kg(self):
        return self.item_weight_g / 1000 if self.item_weight_g is not None else None

    @item_weight_kg.setter
    def item_weight_kg(self, value):
        self.item_weight_g = int(round(value * 1000)) if value is not None else None

    @hybrid_property
    def item_weight_kg_total(self):
        return self.item_weight_g_total / 1000 if self.item_weight_g_total is not None else None

    @item_weight_kg_total.setter
    def item_weight_kg_total(self, value):
        self.item_weight_g_total = int(round(value * 1000)) if value is not None else None


    #cent values
    @hybrid_property
    def item_price_discount_gross(self):
        return self._item_price_discount_gross / 100 if self._item_price_discount_gross is not None else None

    @item_price_discount_gross.setter
    def item_price_discount_gross(self, value):
        self._item_price_discount_gross = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def item_price_gross(self):
        return self._item_price_gross / 100 if self._item_price_gross is not None else None

    @item_price_gross.setter
    def item_price_gross(self, value):
        self._item_price_gross = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def item_price_total_gross(self):
        return self._item_price_total_gross / 100 if self._item_price_total_gross is not None else None

    @item_price_total_gross.setter
    def item_price_total_gross(self, value):
        self._item_price_total_gross = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def shipment_price_discount_gross(self):
        return self._shipment_price_discount_gross / 100 if self._shipment_price_discount_gross is not None else None

    @shipment_price_discount_gross.setter
    def shipment_price_discount_gross(self, value):
        self._shipment_price_discount_gross = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def shipment_price_gross(self):
        return self._shipment_price_gross / 100 if self._shipment_price_gross is not None else None

    @shipment_price_gross.setter
    def shipment_price_gross(self, value):
        self._shipment_price_gross = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def shipment_price_total_gross(self):
        return self._shipment_price_total_gross / 100 if self._shipment_price_total_gross is not None else None

    @shipment_price_total_gross.setter
    def shipment_price_total_gross(self, value):
        self._shipment_price_total_gross = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def sale_total_value_gross(self):
        return self._sale_total_value_gross / 100 if self._sale_total_value_gross is not None else None

    @sale_total_value_gross.setter
    def sale_total_value_gross(self, value):
        self._sale_total_value_gross = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def gift_wrap_price_discount_gross(self):
        return self._gift_wrap_price_discount_gross / 100 if self._gift_wrap_price_discount_gross is not None else None

    @gift_wrap_price_discount_gross.setter
    def gift_wrap_price_discount_gross(self, value):
        self._gift_wrap_price_discount_gross = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def gift_wrap_price_gross(self):
        return self._gift_wrap_price_gross / 100 if self._gift_wrap_price_gross is not None else None

    @gift_wrap_price_gross.setter
    def gift_wrap_price_gross(self, value):
        self._gift_wrap_price_gross = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def gift_wrap_price_total_gross(self):
        return self._gift_wrap_price_total_gross / 100 if self._gift_wrap_price_total_gross is not None else None

    @gift_wrap_price_total_gross.setter
    def gift_wrap_price_total_gross(self, value):
        self._gift_wrap_price_total_gross = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def unit_cost_price_net(self):
        return self._unit_cost_price_net / 100 if self._unit_cost_price_net is not None else None

    @unit_cost_price_net.setter
    def unit_cost_price_net(self, value):
        self._unit_cost_price_net = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def item_price_discount_net(self):
        return self._item_price_discount_net / 100 if self._item_price_discount_net is not None else None

    @item_price_discount_net.setter
    def item_price_discount_net(self, value):
        self._item_price_discount_net = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def item_price_discount_vat(self):
        return self._item_price_discount_vat / 100 if self._item_price_discount_vat is not None else None

    @item_price_discount_vat.setter
    def item_price_discount_vat(self, value):
        self._item_price_discount_vat = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def item_price_net(self):
        return self._item_price_net / 100 if self._item_price_net is not None else None

    @item_price_net.setter
    def item_price_net(self, value):
        self._item_price_net = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def item_price_vat(self):
        return self._item_price_vat / 100 if self._item_price_vat is not None else None

    @item_price_vat.setter
    def item_price_vat(self, value):
        self._item_price_vat = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def item_price_total_net(self):
        return self._item_price_total_net / 100 if self._item_price_total_net is not None else None

    @item_price_total_net.setter
    def item_price_total_net(self, value):
        self._item_price_total_net = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def item_price_total_vat(self):
        return self._item_price_total_vat / 100 if self._item_price_total_vat is not None else None

    @item_price_total_vat.setter
    def item_price_total_vat(self, value):
        self._item_price_total_vat = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def shipment_price_discount_net(self):
        return self._shipment_price_discount_net / 100 if self._shipment_price_discount_net is not None else None

    @shipment_price_discount_net.setter
    def shipment_price_discount_net(self, value):
        self._shipment_price_discount_net = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def shipment_price_discount_vat(self):
        return self._shipment_price_discount_vat / 100 if self._shipment_price_discount_vat is not None else None

    @shipment_price_discount_vat.setter
    def shipment_price_discount_vat(self, value):
        self._shipment_price_discount_vat = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def shipment_price_net(self):
        return self._shipment_price_net / 100 if self._shipment_price_net is not None else None

    @shipment_price_net.setter
    def shipment_price_net(self, value):
        self._shipment_price_net = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def shipment_price_vat(self):
        return self._shipment_price_vat / 100 if self._shipment_price_vat is not None else None

    @shipment_price_vat.setter
    def shipment_price_vat(self, value):
        self._shipment_price_vat = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def shipment_price_total_net(self):
        return self._shipment_price_total_net / 100 if self._shipment_price_total_net is not None else None

    @shipment_price_total_net.setter
    def shipment_price_total_net(self, value):
        self._shipment_price_total_net = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def shipment_price_total_vat(self):
        return self._shipment_price_total_vat / 100 if self._shipment_price_total_vat is not None else None

    @shipment_price_total_vat.setter
    def shipment_price_total_vat(self, value):
        self._shipment_price_total_vat = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def sale_total_value_net(self):
        return self._sale_total_value_net / 100 if self._sale_total_value_net is not None else None

    @sale_total_value_net.setter
    def sale_total_value_net(self, value):
        self._sale_total_value_net = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def sale_total_value_vat(self):
        return self._sale_total_value_vat / 100 if self._sale_total_value_vat is not None else None

    @sale_total_value_vat.setter
    def sale_total_value_vat(self, value):
        self._sale_total_value_vat = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def gift_wrap_price_discount_net(self):
        return self._gift_wrap_price_discount_net / 100 if self._gift_wrap_price_discount_net is not None else None

    @gift_wrap_price_discount_net.setter
    def gift_wrap_price_discount_net(self, value):
        self._gift_wrap_price_discount_net = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def gift_wrap_price_discount_vat(self):
        return self._gift_wrap_price_discount_vat / 100 if self._gift_wrap_price_discount_vat is not None else None

    @gift_wrap_price_discount_vat.setter
    def gift_wrap_price_discount_vat(self, value):
        self._gift_wrap_price_discount_vat = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def gift_wrap_price_net(self):
        return self._gift_wrap_price_net / 100 if self._gift_wrap_price_net is not None else None

    @gift_wrap_price_net.setter
    def gift_wrap_price_net(self, value):
        self._gift_wrap_price_net = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def gift_wrap_price_vat(self):
        return self._gift_wrap_price_vat / 100 if self._gift_wrap_price_vat is not None else None

    @gift_wrap_price_vat.setter
    def gift_wrap_price_vat(self, value):
        self._gift_wrap_price_vat = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def gift_wrap_price_total_net(self):
        return self._gift_wrap_price_total_net / 100 if self._gift_wrap_price_total_net is not None else None

    @gift_wrap_price_total_net.setter
    def gift_wrap_price_total_net(self, value):
        self._gift_wrap_price_total_net = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def gift_wrap_price_total_vat(self):
        return self._gift_wrap_price_total_vat / 100 if self._gift_wrap_price_total_vat is not None else None

    @gift_wrap_price_total_vat.setter
    def gift_wrap_price_total_vat(self, value):
        self._gift_wrap_price_total_vat = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def invoice_amount_vat(self):
        return self._invoice_amount_vat / 100 if self._invoice_amount_vat is not None else None

    @invoice_amount_vat.setter
    def invoice_amount_vat(self, value):
        self._invoice_amount_vat = int(round(value * 100)) if value is not None else None

    #rate values

    @hybrid_property
    def item_price_vat_rate(self):
        return self._item_price_vat_rate / 10_000 if self._item_price_vat_rate is not None else None

    @item_price_vat_rate.setter
    def item_price_vat_rate(self, value):
        self._item_price_vat_rate = int(round(value * 10_000)) if value is not None else None

    @hybrid_property
    def shipment_price_vat_rate(self):
        return self._shipment_price_vat_rate / 10_000 if self._shipment_price_vat_rate is not None else None

    @shipment_price_vat_rate.setter
    def shipment_price_vat_rate(self, value):
        self._shipment_price_vat_rate = int(round(value * 10_000)) if value is not None else None

    @hybrid_property
    def gift_wrap_price_tax_rate(self):
        return self._gift_wrap_price_tax_rate / 10_000 if self._gift_wrap_price_tax_rate is not None else None

    @gift_wrap_price_tax_rate.setter
    def gift_wrap_price_tax_rate(self, value):
        self._gift_wrap_price_tax_rate = int(round(value * 10_000)) if value is not None else None

    @hybrid_property
    def invoice_exchange_rate(self):
        return self._invoice_exchange_rate / 10_000 if self._invoice_exchange_rate is not None else None

    @invoice_exchange_rate.setter
    def invoice_exchange_rate(self, value):
        self._invoice_exchange_rate = int(round(value * 10_000)) if value is not None else None













































    def __repr__(self):
        return '<TransactionInput {}: Account: {} | Activity Period: {} | Channel: {} | Public Type: {} | Marketplace: {}>'.format(self.id, self.account_given_id, self.public_activity_period, self.channel_code, self.transaction_type_public_code, self.marketplace)

    def update(self, data_changes):
        for k, v in data_changes.items():
            setattr(self, k, v)
        return self

    # @property
    # def seller_firm_id(self):
    #     return self.account.seller_firm_id

    # @property
    # def seller_firm(self):
    #     return self.account.seller_firm


    def update_processed(self):
        self.processed = True
        self.processed_on = datetime.utcnow()
