from datetime import datetime
from app.extensions import db


class Item(db.Model):  # type: ignore
    """ Item model """
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    original_filename = db.Column(db.String(128))
    sku = db.Column(db.String(48), nullable=False)
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date)
    brand_name = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    ean = db.Column(db.String(64), nullable=False)
    asin = db.Column(db.String(64), nullable=False)
    fnsku = db.Column(db.String(64), nullable=False)
    # length_mm = db.Column(db.Integer, nullable=False)
    # width_mm = db.Column(db.Integer, nullable=False)
    # height_mm = db.Column(db.Integer, nullable=False)
    # volume_m3 = db.Column(db.Float(precision=28), nullable=False)
    # volume_f3 = db.Column(db.Float(precision=28), nullable=False)
    weight_kg = db.Column(db.Float(precision=28), nullable=False)
    # storage_size = db.Column(db.String(32), nullable=False)
    # storage_media_type = db.Column(db.String(32), nullable=False)
    # storage_category = db.Column(db.String(32), nullable=False)

    tax_code_code = db.Column(db.String(8), db.ForeignKey('tax_code.code'))

    # item_purchase_price_currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
    # item_purchase_price_net = db.Column(db.Float(precision=28))

    unit_cost_price_currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
    unit_cost_price_net = db.Column(db.Float(precision=28))

    transactions = db.relationship('Transaction', backref='item', lazy=True)



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.item_volume_m3 = (self.item_length_mm * self.item_width_mm * self.item_height_mm) / (1000**3)

    def __repr__(self):
        return '<Item: Seller_id: {} – SKU: {} – validity: {}-{}>'.format(self.seller_firm_id, self.sku, self.valid_from, self.valid_to)

    def update(self, data_changes):
        for key, val in data_changes.items():
            setattr(self, key, val)
        return self
