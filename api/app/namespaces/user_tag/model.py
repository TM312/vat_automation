
from datetime import datetime
from app.extensions import db
from ..utils.ATs import user_tag_item_AT



class UserTag(db.Model):
    """ UserTag model """
    __tablename__ = 'user_tag'

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(16))

    items = db.relationship(
        'Item',
        secondary=user_tag_item_AT,
        back_populates='user_tags'
    )
