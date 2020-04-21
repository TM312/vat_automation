from app.extensions import db


class ItemInformation(db.Model):  # type: ignore
    """ ItemInformation model """
    __tablename__ = "item_information"

    id = db.Column(db.Integer, primary_key=True)
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                               nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_to = db.Column(db.DateTime)
    sku = db.Column(db.String(48), nullable=False)
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

    tax_code_id = db.Column(db.Integer, db.ForeignKey('tax_rate_type.id'), nullable=False)

    # item_purchase_price_currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
    # item_purchase_price_net = db.Column(db.Float(precision=28))

    item_unit_cost_price_currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
    item_unit_cost_price_net = db.Column(db.Float(precision=28))

    transactions = db.relationship('Transaction', backref='item_information', lazy=True)



    def __init__(self, **kwargs):
        super(ItemInformation, self).__init__(**kwargs)
        #self.item_volume_m3 = (self.item_length_mm * self.item_width_mm * self.item_height_mm) / (1000**3)

    def __repr__(self):
        return '<ItemInformation: {} {} {} {}>'.format(self.seller_firm_id, self.item_sku, self.valid_from, self.valid_to)
