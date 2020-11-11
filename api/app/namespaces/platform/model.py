from app.extensions import db
from app.namespaces.channel.model import Channel



class Platform(db.Model):
    """ Platform model , e.g. code: AMZ """
    __tablename__ = "platform"

    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(32), unique=True)

    channels = db.relationship('Channel', backref='platform', lazy=True)
    transaction_types_public = db.relationship('TransactionTypePublic', backref='platform', lazy=True)



    def __repr__(self):
        return '<Platform: {} - {}>'.format(self.code, self.name)

    def update(self, data_changes):
        for key, val in data_changes.items():
            if key.lower() != 'code':
                setattr(self, key, val)
        return self
