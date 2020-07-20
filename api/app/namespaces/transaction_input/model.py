from datetime import datetime
from uuid import uuid4

from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID


class TransactionInput(db.Model):
    """ TransactionInput model """
    __tablename__ = "transaction_input"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid4)
    original_filename = db.Column(db.String(128), nullable=False)
    bundle_id = db.Column(db.Integer, db.ForeignKey('bundle.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #User --> uploader

    processed = db.Column(db.Boolean, default=False)
    processed_on = db.Column(db.DateTime)
    transactions = db.relationship('Transaction', backref='transaction_input', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('TransactionNotification', backref='transaction_input', order_by="desc(TransactionNotification.created_on)", lazy=True, cascade='all, delete-orphan')

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account_given_id = db.Column(db.String(128), nullable=False)
    public_activity_period = db.Column(db.String(64))
    channel_code = db.Column(db.String(64))
    marketplace = db.Column(db.String(96))
    transaction_type_public_code = db.Column(db.String(40))
    given_id = db.Column(db.String(64))
    activity_id = db.Column(db.String(64))
    shipment_date = db.Column(db.Date)
    arrival_date = db.Column(db.Date)
    complete_date = db.Column(db.Date)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item_sku = db.Column(db.String(128))
    item_name = db.Column(db.String(128))
    item_manufacture_country = db.Column(db.String(128))
    item_quantity = db.Column(db.Integer)
    item_weight_kg = db.Column(db.Numeric(scale=4))
    item_weight_kg_total = db.Column(db.Numeric(scale=4))

    item_price_discount_gross = db.Column(db.Numeric(scale=2))
    item_price_gross = db.Column(db.Numeric(scale=2))
    item_price_total_gross = db.Column(db.Numeric(scale=2))
    shipment_price_discount_gross = db.Column(db.Numeric(scale=2))
    shipment_price_gross = db.Column(db.Numeric(scale=2))
    shipment_price_total_gross = db.Column(db.Numeric(scale=2))
    sale_total_value_gross = db.Column(db.Numeric(scale=2))
    gift_wrap_price_discount_gross = db.Column(db.Numeric(scale=2))
    gift_wrap_price_gross = db.Column(db.Numeric(scale=2))
    gift_wrap_price_total_gross = db.Column(db.Numeric(scale=2))
    currency_code = db.Column(db.String(8), db.ForeignKey('currency.code'))
    departure_country_code = db.Column(db.String(8))
    departure_postal_code = db.Column(db.String(24))
    departure_city = db.Column(db.String(32))
    arrival_country_code = db.Column(db.String(8))
    arrival_postal_code = db.Column(db.String(24))
    arrival_city = db.Column(db.String(32))
    arrival_address = db.Column(db.String(64))
    shipment_mode = db.Column(db.String(40))
    shipment_conditions = db.Column(db.String(24))
    invoice_number = db.Column(db.String(64))
    invoice_url = db.Column(db.String(256))
    customer_firm_name = db.Column(db.String(64))
    customer_firm_vat_number = db.Column(db.String(24))
    customer_firm_vat_number_country_code = db.Column(db.String(8))
    supplier_vat_number = db.Column(db.String(24))
    supplier_name = db.Column(db.String(64))

    check_tax_calculation_date = db.Column(db.Date)
    check_unit_cost_price_net = db.Column(db.Numeric(scale=2))

    check_item_price_discount_net = db.Column(db.Numeric(scale=2))
    check_item_price_discount_vat = db.Column(db.Numeric(scale=2))
    check_item_price_net = db.Column(db.Numeric(scale=2))
    check_item_price_vat = db.Column(db.Numeric(scale=2))
    check_item_price_total_net = db.Column(db.Numeric(scale=2))
    check_item_price_total_vat = db.Column(db.Numeric(scale=2))
    check_item_price_vat_rate = db.Column(db.Numeric(scale=5))
    check_shipment_price_discount_net = db.Column(db.Numeric(scale=2))
    check_shipment_price_discount_vat = db.Column(db.Numeric(scale=2))
    check_shipment_price_net = db.Column(db.Numeric(scale=2))
    check_shipment_price_vat = db.Column(db.Numeric(scale=2))
    check_shipment_price_total_net = db.Column(db.Numeric(scale=2))
    check_shipment_price_total_vat = db.Column(db.Numeric(scale=2))
    check_shipment_price_vat_rate = db.Column(db.Numeric(scale=5))
    check_sale_total_value_net = db.Column(db.Numeric(scale=2))
    check_sale_total_value_vat = db.Column(db.Numeric(scale=2))
    check_gift_wrap_price_discount_net = db.Column(db.Numeric(scale=2))
    check_gift_wrap_price_discount_vat = db.Column(db.Numeric(scale=2))
    check_gift_wrap_price_net = db.Column(db.Numeric(scale=2))
    check_gift_wrap_price_vat = db.Column(db.Numeric(scale=2))
    check_gift_wrap_price_total_net = db.Column(db.Numeric(scale=2))
    check_gift_wrap_price_total_vat = db.Column(db.Numeric(scale=2))
    check_gift_wrap_price_tax_rate = db.Column(db.Numeric(scale=5))
    check_item_tax_code_code = db.Column(db.String(8))
    check_departure_seller_vat_country_code = db.Column(db.String(8))
    check_departure_seller_vat_number = db.Column(db.String(24))
    check_arrival_seller_vat_country_code = db.Column(db.String(8))
    check_arrival_seller_vat_number = db.Column(db.String(24))
    check_seller_vat_country_code = db.Column(db.String(8))
    check_seller_vat_number = db.Column(db.String(24))
    check_tax_calculation_imputation_country = db.Column(db.String(24))
    check_tax_jurisdiction = db.Column(db.String(24))
    check_tax_jurisdiction_level = db.Column(db.String(24))
    check_invoice_amount_vat = db.Column(db.Numeric(scale=2))
    check_invoice_currency_code = db.Column(db.String(8))
    check_invoice_exchange_rate = db.Column(db.Numeric(scale=5))
    check_invoice_exchange_rate_date = db.Column(db.Date)
    check_export = db.Column(db.Boolean)


    def __repr__(self):
        return '<TransactionInput {}: Account: {} | Activity Period: {} | Channel: {} | Public Type: {} | Marketplace: {}>'.format(self.id, self.account_given_id, self.public_activity_period, self.channel_code, self.transaction_type_public_code, self.marketplace)

    def update(self, data_changes):
        for k, v in data_changes.items():
            setattr(self, k, v)
        return self



    def update_processed(self):
        self.processed = True
        self.processed_on = datetime.utcnow()
