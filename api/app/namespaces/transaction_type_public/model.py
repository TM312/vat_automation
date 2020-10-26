from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


class TransactionTypePublic(db.Model):  # type: ignore
    """ Transaction Type Public model, i.e. platform specific transaction type codes, e.g.: AMZ -> Commingling Buy  """
    __tablename__ = "transaction_type_public"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid4)

    code = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(128))

    platform_code = db.Column(db.String(8), db.ForeignKey('platform.code'), nullable=False)
    transaction_type_code = db.Column(db.String(8), db.ForeignKey('transaction_type.code'), nullable=False)


    def __repr__(self):
        return '<TransactionTypePublic: {}>'.format(self.code)
