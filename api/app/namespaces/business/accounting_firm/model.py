from app.extensions import db  # noqa
from .. import Business
from ..seller_firm import SellerFirm
from ...user import User
from sqlalchemy.ext.declarative import declared_attr
# from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property
from sqlalchemy import select, func

class AccountingFirm(Business):
    __mapper_args__ = {'polymorphic_identity': 'accounting_firm'}

    # https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/inheritance.html
    @declared_attr
    def employees(cls):
        "Employees column, if not present already."
        # Pass foreign_keys= as a Python executable string for lazy evaluation (https://stackoverflow.com/questions/54703652/sqlalchemy-multiple-relationships-between-tables)
        #also: https://stackoverflow.com/questions/22355890/sqlalchemy-multiple-foreign-keys-in-one-mapped-class-to-the-same-primary-key
        return Business.__table__.c.get('employees', db.relationship('TaxAuditor', backref='employer', primaryjoin='TaxAuditor.employer_id==Business.id'))


    clients = db.relationship('SellerFirm', backref=db.backref('accounting_firm', remote_side=[Business.id]))

    # @hybrid_property
    # def len_employees(self):
    #     return (len(self.employees)

    # len_employees = column_property(
    #     select([func.count(User.id)])
    #     .where(User.employer_id == id)
    #     .correlate_except(User)
    # )

    # len_clients = column_property(
    #     select([func.count(SellerFirm.id)])
    #     .where(SellerFirm.accounting_firm_id == id)
    #     .correlate_except(SellerFirm)
    # )

    def __repr__(self):
        return '<Accounting Firm: %r>' % self.name
