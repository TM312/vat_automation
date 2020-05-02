import datetime import date, timedelta

from app.extensions import db

from vies import VIES_WSDL_URL, VIES_OPTIONS, logger




class VATIN(db.Model):
    """ VATIN model """
    __tablename__ = "vatin"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.Date, default=date.today())
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date, default=date.today() + timedelta(days=current_app.config['VATIN_LIFESPAN']))
    initial_tax_date = db.Column(db.Date, nullable=False)
    _country_code = db.Column(db.String(4), nullable=False)
    _number = db.Column(db.String(4), nullable=False)
    valid = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        super(VATIN, self).__init__(**kwargs)
        self.country_code = country_code
        self.number = number
        self.valid = valid


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
