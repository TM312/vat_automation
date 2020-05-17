from ..model_parent import User

class Admin(User):
    __mapper_args__ = {'polymorphic_identity': 'admin'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.avatar_hash = self.gravatar_hash()
        self.confirmed_on = None
