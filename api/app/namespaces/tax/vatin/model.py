from datetime import datetime, date

from app.extensions import db

from . import VIES_OPTIONS




class VATIN(db.Model):
    """ VATIN model """
    __tablename__ = "vatin"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date)
    initial_tax_date = db.Column(db.Date)

    _country_code = db.Column(db.String(4), nullable=False)
    _number = db.Column(db.String(16), nullable=False)
    valid = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(32))
    address = db.Column(db.String(80))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    transactions = db.relationship('Transaction', backref='vatin', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    # https://www.python-course.eu/python3_properties.php
    @property
    def country_code(self):
        return self._country_code

    @country_code.setter
    def country_code(self, value):
        self._country_code = value.upper()

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value.upper().replace(" ", "")



    def __str__(self):
        unformated_number = "{country_code}{number}".format(
            country_code=self.country_code, number=self.number,
        )

        country = VIES_OPTIONS.get(self.country_code, {})
        if len(country) == 3:
            return country[2](unformated_number)
        return unformated_number

    def __repr__(self):
        return "<VATIN {}>".format(self.__str__())

    def update(self, data_changes):
        for key, val in data_changes.items():
            setattr(self, key, val)
        self.modified_at = datetime.utcnow()
        return self
