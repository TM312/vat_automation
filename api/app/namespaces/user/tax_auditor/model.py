

from app.extensions import db  # noqa
from .. import User


class TaxAuditor(User):
    __mapper_args__ = {'polymorphic_identity': 'tax_auditor'}
