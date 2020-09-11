from datetime import datetime
from uuid import uuid4

from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from ..utils.ATs import user_tag_item_AT



class Item(db.Model):  # type: ignore
    """ Item model """
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
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

    tax_code_code = db.Column(db.String(40), db.ForeignKey('tax_code.code'))

    # item_purchase_price_currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
    # item_purchase_price_net = db.Column(db.Float(precision=28))

    unit_cost_price_currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
    _unit_cost_price_net = db.Column(db.Integer)

    unit_cost_price_history = db.relationship('ItemPriceNet', backref='item', lazy=True)

    transaction_inputs = db.relationship('TransactionInput', backref='item', lazy=True)
    transactions = db.relationship('Transaction', backref='item', lazy=True)

    user_tags = db.relationship(
        "UserTag",
        secondary=user_tag_item_AT,
        back_populates="items"
    )

    @hybrid_property
    def weight_kg(self):
        return self.weight_g / 1000 if self.weight_g is not None else None

    @weight_kg.setter
    def weight_kg(self, value):
        self.weight_g = int(value * 1000) if value is not None else None


    @hybrid_property
    def unit_cost_price_net(self):
        return self._unit_cost_price_net / 100 if self._unit_cost_price_net is not None else None

    @unit_cost_price_net.setter
    def unit_cost_price_net(self, value):
        self._unit_cost_price_net = int(value * 100) if value is not None else None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
         # create new item price
        new_item_price = ItemPriceNet(unit_cost_price_net = kwargs.get('unit_cost_price_net'), item_id = self.id)

    def __repr__(self):
        return '<Item: Seller_id: {} – SKU: {} – validity: {}-{}>'.format(self.seller_firm_id, self.sku, self.valid_from, self.valid_to)


    def update(self, data_changes):
        for key, val in data_changes.items():
            if key == 'unit_cost_price_net':
                # Get the current item price
                current_item_price = ItemPriceNet.query.filter_by(
                    item_id = self.id
                    ).order_by(
                        ItemPriceNet.valid_from.desc()
                        ).first()
                # end validity today
                current_item_price.valid_to = date.today()
                #create new item price
                new_item_price = ItemPriceNet(unit_cost_price_net = val, valid_from=date.today(), item_id = self.id)

                setattr(self, key, val)
                self.unit_cost_price_history.append(new_item_price)
        self.modified_at = datetime.utcnow()
        return self


class ItemPriceNet(db.Model):  # type: ignore
    """ Item model """
    __tablename__ = "item_price_net"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    valid_from = db.Column(db.Date, default=datetime.strptime('01-06-2018', '%d-%m-%Y').date)
    valid_to = db.Column(db.Date, default=datetime.strptime('31-12-2030', '%d-%m-%Y').date)
    comment = db.Column(db.String(128))
    _unit_cost_price_net = db.Column(db.Integer)


    @hybrid_property
    def unit_cost_price_net(self):
        return self._unit_cost_price_net / 100 if self._unit_cost_price_net is not None else None

    @unit_cost_price_net.setter
    def unit_cost_price_net(self, value):
        self._unit_cost_price_net = int(value * 100) if value is not None else None


    def __repr__(self):
        return "<ItemPrice {}-{}: {}>".format(str(self.valid_from), str(self.valid_to), self.unit_cost_price_net)
