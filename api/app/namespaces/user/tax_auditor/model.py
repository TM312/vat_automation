

from app.extensions import db  # noqa
from ..model_parent import User


tax_auditor_tax_record_output_country_AT = db.Table(
    'tax_auditor_tax_record_output_country_AT',
    db.Column('tax_auditor_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('tax_record_output_country_id', db.Integer, db.ForeignKey('tax_record_output_country.id'), primary_key=True)
    )

tax_auditor_seller_firm_AT = db.Table(
    'tax_auditor_seller_firm_AT',
    db.Column('tax_auditor_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('seller_firm_id', db.Integer, db.ForeignKey('business.id'), primary_key=True)
    )



class TaxAuditor(User):
    __mapper_args__ = {'polymorphic_identity': 'tax_auditor'}

    # tax_records = db.relationship('TaxRecord', backref='creator', order_by="desc(TaxRecord.created_on)", lazy=True)

    # tax_record_countries = db.relationship(
    #     'TaxRecordOutputCountry',
    #     secondary=tax_record_output_country_AT,
    #     backref="tax_auditors",
    #     lazy=True
    #     )

    key_accounts = db.relationship(
        "SellerFirm",
        secondary=tax_auditor_seller_firm_AT,
        backref="key_account_managers",
        lazy=True
        )


    # https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
    # The association table is indicated by the relationship.secondary argument to relationship()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.avatar_hash = self.gravatar_hash()
        self.confirmed_on = None

    def is_following(self, seller_firm_id):
        return self.key_accounts.filter(tax_auditor_seller_firm_AT.c.seller_firm_id == seller_firm_id).count() > 0



    def __repr__(self):
        return '<Tax Auditor: %r>' % self.email
