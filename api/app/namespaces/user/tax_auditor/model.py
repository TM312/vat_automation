

from app.extensions import db  # noqa
from .. import User
from ...utils.ATs import tax_auditor_seller_firm_AT


class TaxAuditor(User):
    __mapper_args__ = {'polymorphic_identity': 'tax_auditor'}
    key_accounts = db.relationship('SellerFirm', secondary=tax_auditor_seller_firm_AT, back_populates='tax_auditors',  cascade="all, delete")
