from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID


from app.extensions import db  # noqa


class Business(db.Model):  # type: ignore
    """ Business parent model """
    __tablename__ = 'business'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_business_created_by_user'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
    times_modified = db.Column(db.Integer, default=0)
    name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(256))
    # logo_image_name = db.Column(db.String(120), default=None)
    vat_numbers = db.relationship('VATIN', backref='business', lazy=True)
    b_type = db.Column(db.String(50))
    __mapper_args__ = {'polymorphic_on': b_type}



    def update(self, data_changes):
        for k, v in data_changes.items():
            setattr(self, k, v)
        self.modified_at = datetime.utcnow()
        self.times_modified += 1
        return self
