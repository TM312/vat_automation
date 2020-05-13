from app.extensions import db



class Platform(db.Model):
    """ Platform model , e.g. code: AMZ """
    __tablename__ = "platform"

    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(32), unique=True)
    channels = db.relationship('Channel', backref='platform', lazy=True)

    __mapper_args__ = {'polymorphic_on': code}

    def __repr__(self):
        return '<Platform: {} ({})>'.format(self.name, self.code)



class Marketplace(db.Model):
    """ Marketplace model, e.g. name amazon.it """
    __tablename__ = "marketplace"

    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    transactions = db.relationship(
        'Transaction', backref='marketplace', lazy=True)

    def __init__(self, **kwargs):
        super(Marketplace, self).__init__(**kwargs)
