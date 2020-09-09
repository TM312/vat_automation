from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property
from sqlalchemy import select, func

from ..transaction import Transaction
from ..utils.ATs import seller_firm_accounting_firm_AT

from app.extensions import db  # noqa

from ..tax.vatin import VATIN
from ..user import User

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

    accounting_firms = db.relationship(
        'Business',
        secondary=seller_firm_accounting_firm_AT,
        primaryjoin="seller_firm_accounting_firm_AT.c.seller_firm_id == Business.id",
        secondaryjoin="seller_firm_accounting_firm_AT.c.accounting_firm_id == Business.id",
        backref='clients'
    )
    b_type = db.Column(db.String(50))
    __mapper_args__ = {'polymorphic_on': b_type}



    def update(self, data_changes):
        for k, v in data_changes.items():
            setattr(self, k, v)
        self.modified_at = datetime.utcnow()
        self.times_modified += 1
        return self
