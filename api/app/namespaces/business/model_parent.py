from datetime import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db  # noqa


class Business(db.Model):  # type: ignore
    """ Business parent model """
    __tablename__ = "business"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True,nullable=False, default=uuid.uuid4)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
    name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(256))
    # logo_image_name = db.Column(db.String(120), default=None)
    discriminator = db.Column('b_type', db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}


    def update(self, data_changes):
        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()
        return self
