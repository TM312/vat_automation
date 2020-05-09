from datetime import date, timedelta
from zeep import Client
import time

from flask import current_app
from werkzeug.exceptions import HTTPException

from app.extensions import db

from vatin import MEMBER_COUNTRY_CODES, VATIN_MAX_LENGTH, logger
from .model import VATIN



VATIN_LIFESPAN = current_app.config["VATIN_LIFESPAN"]


class VATINService:


# # TEST
# value1 = ['DE', 'DE190200766']
# value2 = ['DE', '190200766']
# value3 = 'DE190200766'
# value4 = ['DE', 'IT190200766']
# values = [value1, value2, value3, value4]
# for value in values:
#     print(value)
#     vat = vat_precheck(value)
#     print("vat country code: {}".format(vat.country_code))
#     print("vat number: {}".format(vat.number))
#     print("")

    @staticmethod
    def create_vatin(country_code: str, number: str, date, valid: bool, **kwargs: date) -> VATIN:

        if 'valid_from' in kwargs and 'valid_to' in kwargs:
            valid_from = kwargs['valid_from']
            valid_to = kwargs['valid_to']

        elif 'valid_from' in kwargs and 'valid_to' not in kwargs:
            valid_from = kwargs['valid_from']
            valid_to_base = max(valid_from, date)
            valid_to = valid_to_base + timedelta(days=VATIN_LIFESPAN)

        elif 'valid_from' not in kwargs and 'valid_to' in kwargs:
            valid_from = min(valid_to, date)
            valid_to = kwargs['valid_to']

        elif 'valid_from' not in kwargs and 'valid_to' not in kwargs:
            valid_from = date
            valid_to = date.today() + timedelta(days=VATIN_LIFESPAN)


        new_vatin = VATIN(
            country_code=country_code,
            number=number,
            initial_tax_date=date,
            valid_from=valid_from,
            valid_to=valid_to
            valid = valid,
            )

        db.session.add(new_vatin)
        db.session.commit()


    @staticmethod
    def check_validity(country_code, number, date) -> bool:
        vat = VATINService.vat_precheck(country_code, number)
        if vat:
            vatin = VATIN.query.filter(VATIN.country_code == country_code, VATIN.number == number, VATIN.initial_tax_date <= date, VATIN.valid_to >= date).first()
            if vatin:
                valid = vatin.valid
            else:
                valid = VATINService.is_valid(country_code, number, date=date)
                VATINService.create_vatin(country_code, number, date=date, valid=valid)

            return valid
        else:
            return False

    @staticmethod
    def vat_precheck(country_code, number):

        if not number:
            return None

        elif not re.match(r"^[a-zA-Z]", number):
            vat = [country_code, number]

        elif country_code == number[:2].strip():
            vat = [country_code, number]

        else:
            # print("country codes dont match. Proceeding with country code from VAT Number.")
            country_code = number[:2].strip()
            number = number[2:].strip()
            vat = [country_code, number] #at this point country_code and number may still be invalid, which will be checked hereafter.

        return vat


    @staticmethod
    def is_valid(country_code, number, date) -> bool:
        if vatin:
            return vatin.valid
        else:
            try:
                VATINService.verify(country_code, number)
                VATINService.validate(country_code, number)

            except HTTPException:
                return False
            else:
                return True

    @staticmethod
    def verify(country_code, number):
        VATINService.verify_country_code(country_code)
        VATINService.verify_regex(country_code, number)

    @staticmethod
    def verify_country_code(country_code):
        if not re.match(r"^[a-zA-Z]", country_code):
            msg = "{} is not a valid ISO_3166-1 country code.".format(country_code)
            raise HTTPException(msg)

        elif country_code not in MEMBER_COUNTRY_CODES:
            msg = "{} is not a European member state.".format(country_code)
            raise HTTPException(msg)

    @staticmethod
    def verify_regex(country_code, number):
        country = dict(
            map(
                lambda x, y: (x, y),
                ("country", "validator", "formatter"),
                VIES_OPTIONS[country_code],
            )
        )
        if not country["validator"].match("{}{}".format(country_code, number)):
            msg = "{} does not match the country's VAT ID specifications.".format(
                country_code)
            raise HTTPException(msg)


    @staticmethod
    def validate(country_code, number):
        valid = VATINService.check_data(country_code, number)
        if not valid:
            msg = "{} is not a valid VATIN.".format(country_code)
            raise HTTPException(msg)


    @staticmethod
    def check_data(country_code, number):
        """VIES API response data."""
        client = Client(VIES_WSDL_URL)
        try:
            return client.service.checkVat(country_code, number)
            time.sleep(0.2)
        except Exception as e:
            logger.exception(e)
            return False
