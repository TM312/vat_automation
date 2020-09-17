from datetime import datetime, timedelta, date
from uuid import uuid4

from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property


from ..utils.ATs import item_tag_item_AT, tag_item_history_AT



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

    tax_code_code = db.Column(db.String(40), db.ForeignKey('tax_code.code'))

    # item_purchase_price_currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
    # item_purchase_price_net = db.Column(db.Float(precision=28))

    unit_cost_price_currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
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


    def update(self, data_changes, **kwargs):
        from ..tag.service import TagService
        from .service import ItemHistoryService

        for key, val in data_changes.items():
            """
            Name or price changes are tracked for each item. A item history object is created whenever one of these attributes is being updated.
            """
            if key == 'unit_cost_price_net' or key == 'name':

                if key == 'unit_cost_price_net':
                    tag = TagService.get_by_code('PRICE_CHANGE')
                    print('Get tag by code "PRICE_CHANGE":', tag, flush=True)
                elif key == 'name':
                    tag = TagService.get_by_code('NAME_CHANGE')
                    ###
                    print('Get tag by code "NAME_CHANGE":', tag, flush=True)

                valid_from = kwargs.get('valid_from') if isinstance(kwargs.get('valid_from'), date) else date.today()

                 # Get the current item history
                item_history = ItemHistoryService.get_by_item_id_date(self.id, valid_from)
                if not isinstance(item_history, ItemHistory):
                    raise

                if ((key == 'unit_cost_price_net' and val == item_history.unit_cost_price_net) or
                    (key == 'name' and val == item_history.name)):
                    continue

                else:

                    if valid_from == item_history.valid_from:
                        if key == 'unit_cost_price_net':
                            item_history.unit_cost_price_net = val
                        elif key == 'name':
                            item_history.name = val

                        if not tag in item_history.tags:
                            item_history.tags.append(tag)

                    else:
                        unit_cost_price_net = (
                            data_changes.get('unit_cost_price_net')
                            if isinstance(data_changes.get('unit_cost_price_net'), (int, complex, float))
                            else self.unit_cost_price_net
                        )
                        name = (
                            data_changes.get('name')
                            if isinstance(data_changes.get('name'), str)
                            else self.name
                            )
                        unit_cost_price_currency_code = (
                            data_changes.get('unit_cost_price_currency_code')
                            if isinstance(data_changes.get('unit_cost_price_currency_code'), str)
                            else self.unit_cost_price_currency_code
                        )

                        if valid_from > item_history.valid_from:
                            item_history.valid_to = valid_from - timedelta(days=1)

                            item_history_data = {
                                'unit_cost_price_net': unit_cost_price_net,
                                'unit_cost_price_currency_code': unit_cost_price_currency_code,
                                'name': name,
                                'valid_from': valid_from,
                                'item_id': self.id
                            }

                        else:
                            item_history_data = {
                                'unit_cost_price_net': unit_cost_price_net,
                                'unit_cost_price_currency_code': unit_cost_price_currency_code,
                                'name': name,
                                'valid_from': valid_from,
                                'valid_to': item_history.valid_from - timedelta(days=1),
                                'item_id': self.id
                            }

                        try:
                            new_item_history = ItemHistoryService.create(item_history_data)
                        except:
                            raise

                        new_item_history.tags.append(tag)
                        self.item_history.append(new_item_history)

            setattr(self, key, val)
        self.modified_at = datetime.utcnow()
        return self


class ItemHistory(db.Model):  # type: ignore
    """ Item history model """
    __tablename__ = "item_history"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    tags = db.relationship(
        "Tag",
        secondary=tag_item_history_AT,
        back_populates="item_histories"
    )

    valid_from = db.Column(db.Date, default=datetime.strptime('01-06-2018', '%d-%m-%Y').date)
    valid_to = db.Column(db.Date, default=datetime.strptime('31-12-2030', '%d-%m-%Y').date)

    unit_cost_price_currency_code = db.Column(db.String(4), nullable=False)
    _unit_cost_price_net = db.Column(db.Integer)
    name = db.Column(db.String(256))
    comment = db.Column(db.String(256))


    @hybrid_property
    def unit_cost_price_net(self):
        return self._unit_cost_price_net / 100 if self._unit_cost_price_net is not None else None

    @unit_cost_price_net.setter
    def unit_cost_price_net(self, value):
        self._unit_cost_price_net = int(round(value * 100)) if value is not None else None


    def __repr__(self):
        return "<ItemPrice {}-{}: {}>".format(str(self.valid_from), str(self.valid_to), self.unit_cost_price_net)
