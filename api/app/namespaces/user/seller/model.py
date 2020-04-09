from app.extensions import db  # noqa
from ..model_parent import User

class Seller(User):
    __mapper_args__ = {'polymorphic_identity': 'seller'}

    def __init__(self, **kwargs):
        super(Seller, self).__init__(**kwargs)
        self.avatar_hash = self.gravatar_hash()
        self.confirmed_on = None

    def __repr__(self):
        return '<Seller: %r>' % self.email
