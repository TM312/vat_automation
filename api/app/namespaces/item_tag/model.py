
from datetime import datetime
from app.extensions import db
from ..utils.ATs import item_tag_item_AT



class ItemTag(db.Model):
    """ ItemTag model """
    __tablename__ = 'item_tag'

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(16))

    items = db.relationship(
        'Item',
        secondary=item_tag_item_AT,
        back_populates='item_tags'
    )
