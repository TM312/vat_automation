

from app.extensions import db  # noqa
from ..model_parent import User


class TaxAuditor(User):
    __mapper_args__ = {'polymorphic_identity': 'tax_auditor'}
