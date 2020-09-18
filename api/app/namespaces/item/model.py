from datetime import datetime, timedelta, date
from uuid import uuid4

from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property


from ..utils.ATs import item_tag_item_AT



class Item(db.Model):  # type: ignore
    """ Item model """
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
    given_id = db.Column(db.String(40))
    active = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    original_filename = db.Column(db.String(128))
    sku = db.Column(db.String(48))
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    brand_name = db.Column(db.String(256))
    name = db.Column(db.String(256))
    ean = db.Column(db.String(64))
    asin = db.Column(db.String(64))
    fnsku = db.Column(db.String(64))
    # length_mm = db.Column(db.Integer, nullable=False)
    # width_mm = db.Column(db.Integer, nullable=False)
    # height_mm = db.Column(db.Integer, nullable=False)
    # volume_m3 = db.Column(db.Float(precision=28), nullable=False)
    # volume_f3 = db.Column(db.Float(precision=28), nullable=False)
    weight_g = db.Column(db.Integer)
    # storage_size = db.Column(db.String(32), nullable=False)
    # storage_media_type = db.Column(db.String(32), nullable=False)
    # storage_category = db.Column(db.String(32), nullable=False)

    tax_code_code = db.Column(db.String(40), db.ForeignKey('tax_code.code'), default='A_GEN_STANDARD')

    # item_purchase_price_currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
    # item_purchase_price_net = db.Column(db.Float(precision=28))

    unit_cost_price_currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), default='EUR')
    _unit_cost_price_net = db.Column(db.Integer)

    item_history = db.relationship('ItemHistory', backref='item', lazy=True, cascade='all, delete-orphan')

    transaction_inputs = db.relationship('TransactionInput', backref='item', lazy=True)
    transactions = db.relationship('Transaction', backref='item', lazy=True)

    item_tags = db.relationship(
        "ItemTag",
        secondary=item_tag_item_AT,
        back_populates="items"
    )

    @hybrid_property
    def weight_kg(self):
        return self.weight_g / 1000 if self.weight_g is not None else None

    @weight_kg.setter
    def weight_kg(self, value):
        self.weight_g = int(round(value * 1000)) if value is not None else None


    @hybrid_property
    def unit_cost_price_net(self):
        return self._unit_cost_price_net / 100 if self._unit_cost_price_net is not None else None

    @unit_cost_price_net.setter
    def unit_cost_price_net(self, value):
        self._unit_cost_price_net = int(round(value * 100)) if value is not None else None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<Item: Seller_id: {} – SKU: {} – validity: {}-{}>'.format(self.seller_firm_id, self.sku, self.valid_from, self.valid_to)



    def update(self, data_changes):
        from .service import ItemHistoryService

        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()

        ItemHistoryService.handle_update(self.id, data_changes)

        return self



class ItemHistory(db.Model):  # type: ignore
    """ Item history model """
    __tablename__ = "item_history"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)

    #meta data
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    valid_from = db.Column(db.Date, default=datetime.strptime('01-06-2018', '%d-%m-%Y').date)
    valid_to = db.Column(db.Date, default=datetime.strptime('31-12-2035', '%d-%m-%Y').date)
    comment = db.Column(db.String(256))

    # mirrored attributes (no relationships!)
    created_by = db.Column(db.Integer)
    given_id = db.Column(db.String(40))
    active = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer)
    original_filename = db.Column(db.String(128))
    sku = db.Column(db.String(48))
    seller_firm_id = db.Column(db.Integer)
    brand_name = db.Column(db.String(256))
    name = db.Column(db.String(256))
    ean = db.Column(db.String(64))
    asin = db.Column(db.String(64))
    fnsku = db.Column(db.String(64))
    weight_g = db.Column(db.Integer)
    tax_code_code = db.Column(db.String(40))
    unit_cost_price_currency_code = db.Column(db.String(4))
    _unit_cost_price_net = db.Column(db.Integer)


    @hybrid_property
    def unit_cost_price_net(self):
        return self._unit_cost_price_net / 100 if self._unit_cost_price_net is not None else None

    @unit_cost_price_net.setter
    def unit_cost_price_net(self, value):
        self._unit_cost_price_net = int(round(value * 100)) if value is not None else None

    @hybrid_property
    def weight_kg(self):
        return self.weight_g / 1000 if self.weight_g is not None else None

    @weight_kg.setter
    def weight_kg(self, value):
        self.weight_g = int(round(value * 1000)) if value is not None else None


    def __repr__(self):
        return "<ItemHistory {}-{}: {}>".format(str(self.valid_from), str(self.valid_to), self.unit_cost_price_net)

    def __attr__(self):
        return {
            'created_by': self.created_by,
            'given_id': self.given_id,
            'active': self.active,
            'category_id': self.category_id,
            'original_filename': self.original_filename,
            'brand_name': self.brand_name,
            'name': self.name,
            'ean': self.ean,
            'asin': self.asin,
            'fnsku': self.fnsku,
            'weight_kg': self.weight_kg,
            'tax_code_code': self.tax_code_code,
            'unit_cost_price_currency_code': self.unit_cost_price_currency_code,
            'unit_cost_price_net': self.unit_cost_price_net,
        }
