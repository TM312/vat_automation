from app.extensions import db


class Vat(db.Model):  # type: ignore
    """ Vat model """
    __tablename__ = "vat"

    id = db.Column(db.Integer, primary_key=True)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date)

    country_code = db.Column(db.String(4), db.ForeignKey('country.code'))
    tax_code_code = db.Column(db.String(8), db.ForeignKey('tax_code.code'))
    tax_rate_type_code = db.Column(db.ForeignKey('tax_rate_type.code'), nullable = False)

    rate = db.Column(db.Numeric(scale=4))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

            def __repr__(self):
                return '<Vat: valid: {}-{} – country_code: {} - tax_code: {} – tax_rate_type_code: {} – rate {}>'.format(self.valid_from, self.valid_to, self.country_code, self.tax_code_code, self.tax_rate_type_code, self.rate)



class TaxRateType(db.Model):  # type: ignore
    """ TaxRateTypeCountry model, e.g. codes: R, R2, Z, S """
    __tablename__ = "tax_rate_type"

    code = db.Column(db.String(8), primary_key=True)
    description = db.Column(db.String(256))
    tax_rates = db.relationship('Vat', backref='tax_rate_type', lazy=True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<TaxRateType: {}'.format(self.code)
