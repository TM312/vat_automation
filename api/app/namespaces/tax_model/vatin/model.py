import datetime

from app.extensions import db

from vies import VIES_WSDL_URL, VIES_OPTIONS, logger

from werkzeug.exceptions import HTTPException
from werkzeug.utils import cached_property

from zeep import Client


class VATIN(db.Model):
    """ VATIN model """
    __tablename__ = "vatin"

    id = db.Column(db.Integer, primary_key=True)
    valid_first = db.Column(db.Datetime, default=datetime.datetime.utcnow)
    valid_to = db.Column(db.DateTime)
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                               nullable=False)

    def __init__(self, **kwargs):
        super(ItemInformation, self).__init__(**kwargs)
        self.country_code = country_code
        self.number = number


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

    @cached_property
    def data(self):
        """VIES API response data."""
        client = Client(VIES_WSDL_URL)
        try:
            return client.service.checkVat(self.country_code, self.number)
        except Exception as e:
            logger.exception(e)
            raise

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


    @classmethod
    def from_str(cls, value):
        """Return a VATIN object by given string."""
        return cls(value[:2].strip(), value[2:].strip())
