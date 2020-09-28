from app.extensions import db


class TaxRateType(db.Model):  # type: ignore
    """ TaxRateType model, e.g. codes: R, R2, Z, S """
    __tablename__ = "tax_rate_type"

    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(256))
    vats = db.relationship('Vat', backref='tax_rate_type', lazy=True)

    transactions_item_tax_rate_type = db.relationship('Transaction', backref="transaction_item_tax_rate_type", foreign_keys="Transaction.item_tax_rate_type_code")
    transactions_shipment_tax_rate_type = db.relationship('Transaction', backref="transaction_shipment_tax_rate_type", foreign_keys="Transaction.shipment_tax_rate_type_code")
    transactions_gift_wrap_tax_rate_type = db.relationship('Transaction', backref="transaction_gift_wrap_tax_rate_type", foreign_keys="Transaction.gift_wrap_tax_rate_type_code")



    def __repr__(self):
        return '<TaxRateType: {}'.format(self.code)
