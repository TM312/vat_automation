from app.extensions import db  # noqa
from .. import Business
from sqlalchemy.ext.declarative import declared_attr

class AccountingFirm(Business):
    __mapper_args__ = {'polymorphic_identity': 'accounting_firm'}

    # https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/inheritance.html
    @declared_attr
    def employees(cls):
        "Employees column, if not present already."
        return Business.__table__.c.get('employees', db.relationship(
            'TaxAuditor', backref='employer', lazy=True))

    # @declared_attr
    # def tax_records(cls):
    #     "tax_records column, if not present already."
    #     return Business.__table__.c.get('tax_records', db.relationship('TaxRecord', backref='accounting_firm', order_by="desc(TaxRecord.created_on)", lazy=True))

    clients =db.relationship('SellerFirm', backref='accounting_firm', lazy=True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<Accounting Firm: %r>' % self.name
