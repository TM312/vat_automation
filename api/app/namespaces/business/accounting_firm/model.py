from app.extensions import db  # noqa
from ..model_parent import Business

class Accounting_Firm(Business):
    __mapper_args__ = {'polymorphic_identity': 'accounting_firm'}
    employees = db.relationship(
        'TaxAuditor', backref='employer', lazy=True)

    clients = db.relationship(
        'Seller_Firm', backref='accounting_firm', lazy=True)


    def __init__(self, **kwargs):
        super(Accounting_Firm, self).__init__(**kwargs)

    def __repr__(self):
        return '<Accounting Firm: %r>' % self.company_name
