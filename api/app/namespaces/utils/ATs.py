from app.extensions import db

channel_tax_code_AT = db.Table(
    'channel_tax_code_AT',
    db.Column('channel_code', db.String(8), db.ForeignKey('channel.code'), primary_key=True),
    db.Column('tax_code_code', db.String(40), db.ForeignKey('tax_code.code'), primary_key=True)
    )


eu_country_AT = db.Table(
    'eu_country_AT',
    db.Column('eu_id', db.Integer, db.ForeignKey('eu.id'), primary_key=True),
    db.Column('country_code', db.String(4), db.ForeignKey('country.code'), primary_key=True)
    )

tax_treatment_transaction_type_AT = db.Table(
    'tax_treatment_transaction_type_AT',
    db.Column('tax_treatment_code', db.String(40), db.ForeignKey('tax_treatment.code'), primary_key=True),
    db.Column('transaction_type_code', db.String(16), db.ForeignKey('transaction_type.code'), primary_key=True)
    )


tax_record_user_AT = db.Table(
    'tax_record_user_AT',
    db.Column('tax_record_id', db.Integer, db.ForeignKey('tax_record.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    )

tax_record_transaction_AT = db.Table(
    'tax_record_transaction_AT',
    db.Column('tax_record_id', db.Integer, db.ForeignKey('tax_record.id'), primary_key=True),
    db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id'), primary_key=True)
)

tax_auditor_seller_firm_AT = db.Table(
    'tax_auditor_seller_firm_AT',
    db.Column('tax_auditor_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('seller_firm_id', db.Integer, db.ForeignKey('business.id'), primary_key=True)
)
