from app.extensions import db
from ..channel.model import Channel



class Platform(db.Model):
    """ Platform model , e.g. code: AMZ """
    __tablename__ = "platform"

    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(32), unique=True)
    channels = db.relationship('Channel', backref='platform', lazy=True)
    distance_sales = db.relationship('DistanceSale', backref='platform', lazy=True)

    __mapper_args__ = {'polymorphic_on': code}

    def __repr__(self):
        return '<Platform: {} (code : {})>'.format(self.name, self.code)
