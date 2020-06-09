from app.extensions import db  # noqa
from ..model_parent import User

class Seller(User):
    __mapper_args__ = {'polymorphic_identity': 'seller'}
