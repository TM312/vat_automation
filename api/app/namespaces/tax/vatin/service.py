from typing import List
from datetime import date, timedelta
from zeep import Client
import time

from flask import current_app
from werkzeug.exceptions import HTTPException

from app.extensions import db

from vatin import MEMBER_COUNTRY_CODES, VIES_WSDL_URL, VATIN_MAX_LENGTH, logger
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
    def create_vatin(country_code: str, number: str, valid_from: date, valid_to: date, valid: bool, **kwargs) -> VATIN:
        new_vatin = VATIN(
            country_code=country_code,
            number=number,
            initial_tax_date=kwargs.get('initial_tax_date'),
            valid_from=valid_from,
            valid_to=valid_to
            valid = valid,
            business_id=kwargs.get('business_id')
            )

        db.session.add(new_vatin)
        db.session.commit()


    @staticmethod
    def process_vat_numbers_upload(vat_numbers_files: list):
        file_type='vat_numbers'
        file_path_in_list = InputService.store_static_data_upload(files=vat_numbers_files, file_type=file_type)
        seller_firm_id_list = InputService.get_seller_firm_id_list(files=vat_numbers_files)

        create_function = VATINService.process_vatin_from_df_file_path


        flat_response_objects = InputService.create_static_data_inputs(file_path_in_list, seller_firm_id_list, create_function)

        InputService.move_static_files(file_path_in_list, file_type)

        return flat_response_objects


    @staticmethod
    def process_vatin_from_df_file_path(file_path: str, seller_firm_id: str) -> list:
        df = InputService.read_file_path_into_df(file_path, encoding=None)

        error_counter = 0
        total_number_items = len(df.index)
        input_type = 'vat number' #only used for response objects

        for i in range(total_number_items):
            country_code = InputService.get_str(df, i, column='country_code'),
            number = InputService.get_str(df, i, column='number')

            valid_from = InputService.get_date_or_None(df, i, column='valid_from')
            valid_to = InputService.get_date_or_None(df, i, column='valid_to')

            if not valid_from:
                valid_from = date.today()
            if not valid_to:
                valid_to = valid_from + timedelta(days=VATIN_LIFESPAN)

            seller_firm_id = seller_firm_id_list[i]:
            try:
                VATINService.check_validity(country_code, number, valid, valid_from=valid_from, valid_to=valid_to, business_id=seller_firm_id)

            except:
                db.session.rollback()
                error_counter += 1

        response_objects = InputService.create_input_response_objects(file_path, input_type, total_number_items, error_counter)

        return response_objects





    @staticmethod
    def get_validity_period(date: date, **kwargs):
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

        return valid_from, valid_to




    @staticmethod
    def check_validity(country_code: str, number, **kwargs) -> bool:
        vat = VATINService.vat_precheck(country_code, number)
        if vat:
            if 'initial_tax_date' in kwargs:
                vatin = VATIN.query.filter(VATIN.country_code == country_code, VATIN.number == number, VATIN.initial_tax_date <= kwargs['initial_tax_date'], VATIN.valid_to >= kwargs['initial_tax_date']).first()
            else:
                vatin = VATIN.query.filter(VATIN.country_code == country_code, VATIN.number == number).first()

            if vatin:
                valid = vatin.valid
                if not vatin.initial_tax_date and 'initial_tax_date' in kwargs:
                    vatin.initial_tax_date = kwargs['initial_tax_date']
                    db.session.commit()

            else:
                valid = VATINService.is_valid(country_code=country_code, number=number, **kwargs)
                valid_from, valid_to = VATINService.get_validity_period(date, **kwargs)
                VATINService.create_vatin(country_code, number, valid_from, valid_to, valid, **kwargs)

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


    @staticmethod #!!! async??
    def check_data(country_code, number):
        """VIES API response data."""
        client = Client(VIES_WSDL_URL)
        try:
            return client.service.checkVat(country_code, number)

        except Exception as e:
            logger.exception(e)
            return False
