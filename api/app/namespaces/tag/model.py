
from app.extensions import db
from ..utils.ATs import tag_notification_AT, tag_item_history_AT

class Tag(db.Model):
    """ Tag model, i.e. codes:
        ACCOUNT, DISTANCE_SALE, ITEM, VAT_NUMBER, TRANSACTION,
        NAME_CHANGE, PRICE_CHANGE
    """
    __tablename__ = "tag"

    code = db.Column(db.String(24), primary_key=True)

    notifications = db.relationship(
        "Notification",
        secondary=tag_notification_AT,
        back_populates="tags"
    )

    item_histories = db.relationship(
        'ItemHistory',
        secondary=tag_item_history_AT,
        back_populates="tags"
    )
