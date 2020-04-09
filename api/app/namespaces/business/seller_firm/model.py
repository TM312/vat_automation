from app.extensions import db  # noqa
from ..model_parent import Business

class Seller_Firm(Business):
    __mapper_args__ = {'polymorphic_identity': 'seller_firm'}

    claimed = db.Column(db.Boolean, default=False)

    employees = db.relationship(
        'Seller', backref='employer', lazy=True)

    # IDs for supported platforms
    amazon_seller_id = db.Column(db.String(40), default=None)

    # Columns related to Accounting/Tax Service
    accounting_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    accounting_firm_seller_id = db.Column(db.String(120), default=None)

    tax_records = db.relationship('TaxRecord', backref='owner', lazy=True)


    def __init__(self, **kwargs):
        super(Seller_Firm, self).__init__(**kwargs)

    def __repr__(self):
        return '<Seller_Firm: %r>' % self.company_name
