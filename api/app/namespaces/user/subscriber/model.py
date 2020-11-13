

from app.extensions import db  # noqa
from .. import User


class Subscriber(User):
    __mapper_args__ = {'polymorphic_identity': 'subscriber'}
