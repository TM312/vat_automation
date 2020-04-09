from app.extensions import db  # noqa


# User objects can be associated in a tax_auditor-seller many-to-many relationship, i.e. one seller can have multiple tax_auditors and one tax_auditor can serve multiple sellers.
# Since the associated objects belong to the same entity, i.e. user, it is called self-referential relationship.
clients = db.Table('User',
    db.Column('tax_auditor_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('client_id', db.Integer, db.ForeignKey('user.id'))
)
