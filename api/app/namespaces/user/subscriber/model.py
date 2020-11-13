from app.extensions import db  # noqa
from app.namespaces.user import User


class Subscriber(User):
    __mapper_args__ = {'polymorphic_identity': 'subscriber'}

    u_type_indicated = db.Column(db.String(16), default="seller")
