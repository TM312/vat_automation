from app.extensions import db
####################################################################################

class TaxRate(db.Model):  # type: ignore
    """ TaxRate model """
    __tablename__ = "tax_rate"

    country_code = db.Column(db.String(4), db.ForeignKey('country.code'), primary_key=True)
    tax_code_code = db.Column(db.String(8), db.ForeignKey('tax_code.code'), primary_key=True)

    tax_rate_type_name = db.Column(db.ForeignKey('tax_rate_type.name'), nullable = False)

    valid_from = db.Column(db.DateTime, nullable=False)
    valid_to = db.Column(db.DateTime)
    rate = db.Column(db.Numeric(precision=8, scale=4))

    tax_code = db.relationship("TaxCode", back_populates="countries")
    country = db.relationship("Country", back_populates="tax_codes")

    # def __init__(self, **kwargs):
    #     super(TaxRate, self).__init__(**kwargs)

    def __repr__(self):
        return '<TaxRate: valid: {}-{} – country_code: {} - tax_rate_type_name: {} – rate {}>'.format(self.valid_from, self.valid_to, self.country_code, self.tax_rate_type_name, self.rate)


class TaxCode(db.Model):  # type: ignore
    """ Item tax_code, e.g. A_GEN_STANDARD """
    __tablename__ = "tax_code"

    code = db.Column(db.String(8), primary_key=True)
    description = db.Column(db.String(128), nullable=False)
    countries = db.relationship('TaxRate', back_populates='tax_code')
    channels = db.relationship(
        "Channel",
        secondary=channel_tax_code_AT,
        back_populates="tax_codes"
    )

    def __init__(self, **kwargs):
        super(TaxCode, self).__init__(**kwargs)

    def __repr__(self):
        return '<TaxCode:{} valid from:{}>'.format(self.code, self.description)

########################################################################
!!!!!  TAX RATE TYPES NEED TO BE ADAPTED EITHER : R_DE incl. Rate or R excl. rate !!!!!

############################################################
class TaxRateType(db.Model):  # type: ignore
    """ TaxRateTypeCountry model, e.g. names: R_DE, R2_DE, Z_GB, S_DE """
    __tablename__ = "tax_rate_type"

    name = db.Column(db.String(8), primary_key=True)
    public_name = db.Column(db.String(256), nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_to = db.Column(db.DateTime)

    rate = db.Column(db.Numeric(precision=8, scale=4))
    tax_rates = db.relationship('TaxRate', backref='tax_rate_type', lazy=True)

    description = db.Column(db.String(256), default=None)



    def __init__(self, **kwargs):
        super(TaxRateType, self).__init__(**kwargs)

    def __repr__(self):
        return '<TaxRateType: {}'.format(self.code)
