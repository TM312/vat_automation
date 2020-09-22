
from app.extensions import db
from app.namespaces.utils.ATs import tag_notification_AT

class Tag(db.Model):
    """ Tag model, i.e. codes:
        ACCOUNT, DISTANCE_SALE, ITEM, VAT_NUMBER, TRANSACTION,
    """

    __tablename__ = "tag"

    code = db.Column(db.String(24), primary_key=True)

    notifications = db.relationship(
        "Notification",
        secondary=tag_notification_AT,
        back_populates="tags"
    )
