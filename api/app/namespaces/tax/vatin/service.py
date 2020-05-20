from typing import List
from datetime import date, timedelta
from zeep import Client
import time

from flask import current_app
from werkzeug.exceptions import HTTPException

from app.extensions import db

from . import MEMBER_COUNTRY_CODES, VIES_WSDL_URL, VATIN_MAX_LENGTH, logger
from .model import VATIN

from ...business.seller_firm.service import SellerFirmService




class VATINService:

    @staticmethod
    def create_vatin(vatin_data: dict) -> VATIN:
        new_vatin = VATIN(
            country_code = vatin_data.get('country_code'),
            number = vatin_data.get('number'),
            initial_tax_date = vatin_data.get('initial_tax_date'),
            valid_from = vatin_data.get('valid_from'),
            valid_to = vatin_data.get('valid_to'),
            valid = vatin_data.get('valid '),
            business_id = vatin_data.get('business_id')
            )

        db.session.add(new_vatin)
        db.session.commit()


    @staticmethod
    #kwargs can contain: seller_firm_public_id
    def process_vat_numbers_files_upload(vat_numbers_files: list, **kwargs):
        BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config["BASE_PATH_STATIC_DATA_SELLER_FIRM"]

        file_type='vat_numbers'
        df_encoding = 'utf-8'
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM

        for file in vat_numbers_files:
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            VATINService.process_vat_numbers_file(file_path_in, file_type, df_encoding, basepath, **kwargs)

        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(vat_numbers_files)))
        }

        return response_object


    # celery task !!
    @staticmethod
    def process_vat_numbers_file(file_path_in: str, file_type: str, df_encoding, basepath: str, **kwargs) -> list:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding)
        response_objects = VATINService.create_vatins(df, file_path_in, **kwargs)

        InputService.move_file_to_out(file_path_in, file_type)

        return response_objects




    @staticmethod
    def create_vatins(df, file_path_in: str, **kwargs) -> list:
        VATIN_LIFESPAN = current_app.config["VATIN_LIFESPAN"]


        error_counter = 0
        total_number_vatins = len(df.index)
        input_type = 'vat number' #only used for response objects

        for i in range(total_number_vatins):
            seller_firm_id = SellerFirmService.get_seller_firm_id(df, i, **kwargs)

            country_code = InputService.get_str(df, i, column='country_code'),
            number = InputService.get_str(df, i, column='number')

            valid_from = InputService.get_date_or_None(df, i, column='valid_from')
            valid_to = InputService.get_date_or_None(df, i, column='valid_to')

            if not valid_from:
                valid_from = date.today()
            if not valid_to:
                valid_to = valid_from + timedelta(days=VATIN_LIFESPAN)

            seller_firm_id = seller_firm_id_list[i]
            try:
                VATINService.check_validity(country_code, number, valid, valid_from=valid_from, valid_to=valid_to, business_id=seller_firm_id)

            except:
                db.session.rollback()
                error_counter += 1

        response_objects = InputService.create_input_response_objects(file_path, input_type, total_number_vatins, error_counter)

        return response_objects





    @staticmethod
    def get_validity_period(date: date, **kwargs):
        VATIN_LIFESPAN = current_app.config["VATIN_LIFESPAN"]

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
            if isinstance(kwargs.get('initial_tax_date'), date):
                vatin = VATIN.query.filter(VATIN.country_code == country_code, VATIN.number == number, VATIN.initial_tax_date <= kwargs['initial_tax_date'], VATIN.valid_to >= kwargs['initial_tax_date']).first()
            else:
                vatin = VATIN.query.filter(VATIN.country_code == country_code, VATIN.number == number).first()

            if vatin:
                valid = vatin.valid
                if not vatin.initial_tax_date and isinstance(kwargs.get('initial_tax_date'), date):
                    vatin.initial_tax_date = kwargs['initial_tax_date']
                    db.session.commit()

            else:
                valid = VATINService.is_valid(country_code=country_code, number=number, **kwargs)
                valid_from, valid_to = VATINService.get_validity_period(date, **kwargs)

                vatin_data = {
                    'country_code' : country_code,
                    'number' : number,
                    'initial_tax_date' : kwargs.get('initial_tax_date'),
                    'valid_from' : valid_from,
                    'valid_to' : valid_to,
                    'valid' : valid,
                    'business_id' : kwargs.get('business_id')
                }
                try:
                    VATINService.create_vatin(vatin_data)
                except:
                    raise

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


    @staticmethod #!! async??
    def check_data(country_code, number):
        """VIES API response data."""
        client = Client(VIES_WSDL_URL)
        try:
            return client.service.checkVat(country_code, number)

        except Exception as e:
            logger.exception(e)
            return False
