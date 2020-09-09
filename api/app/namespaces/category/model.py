from datetime import datetime
from uuid import uuid4

from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID


class Category(db.Model):  # type: ignore
    """ Category model """
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)

    name = db.Column(db.String(40))
    level = db.Column(db.Integer, default=0)

    # https://docs.sqlalchemy.org/en/13/orm/self_referential.html?highlight=self%20referential
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    children = db.relationship("Category", backref=db.backref('parent', remote_side=[id]))

    c_type = db.Column(db.String(16))
    __mapper_args__ = {'polymorphic_on': c_type}



    def __repr__(self):
        return '<Category {}: name: {} | level: {} | business_id: {}>'.format(self.id, self.name, self.level)

    def update(self, data_changes):
        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()
        return self


class ItemCategory(Category):  # type: ignore

    __mapper_args__ = {'polymorphic_identity': 'item'}

    items = db.relationship('Item', backref='category', lazy=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
