from typing import List, BinaryIO, Dict
import pandas as pd
from datetime import date, timedelta
import time
import re

from flask import current_app
from werkzeug.exceptions import HTTPException

from app.extensions import db

from .helpers import MEMBER_COUNTRY_CODES, VIES_WSDL_URL, VATIN_MAX_LENGTH, VIES_OPTIONS
from . import VATIN
from .interface import VATINInterface

from ...transaction_input import TransactionInput
from ...utils.service import InputService



class VATINService:
    @staticmethod
    def get_all() -> List[VATIN]:
        vatins = VATIN.query.all()
        return vatins

    @staticmethod
    def get_by_id(vatin_id: int) -> VATIN:
        return VATIN.query.filter(VATIN.id == vatin_id).first()


    @staticmethod
    def update(vatin_id: int, data_changes: VATINInterface) -> VATIN:
        vatin = VATINService.get_by_id(vatin_id)
        vatin.update(data_changes)
        db.session.commit()
        return vatin

    @staticmethod
    def delete_by_id(vatin_id: int):
        vatin = VATIN.query.filter(VATIN.id == vatin_id).first()
        if vatin:
            db.session.delete(vatin)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'VATIN (code: {}) has been successfully deleted.'.format(vatin_id)
            }
            return response_object
        else:
            raise NotFound('This vatin does not exist.')





    @staticmethod
    def get_vatin(country_code: str, number: str, date: date) -> VATIN:
        vatin: VATIN.query.filter_by(VATIN.country_code == country_code, VATIN.number==number, VATIN.valid_from<=date, VATIN.valid_to>=date).first()
        return vatin



    @staticmethod
    def get_vatin_if_number(country_code_temp: str, number_temp: str, date: date) -> VATIN:
        if not isinstance(number_temp, str):
            return None
        else:
            try:
                country_code, number = VATINService.vat_precheck(country_code_temp, number_temp)
                vatin = VATINService.get_vatin(country_code, number, date)
                if not isinstance(vatin, VATIN):
                    valid_from, valid_to = VATINService.get_validity_period(date)
                    business_id = None
                    vatin = VATINService.create_vatin_by_request(country_code, number, valid_from, valid_to, business_id)

            except:
                raise

            return vatin


    @staticmethod
    def create(vatin_data: dict) -> VATIN:
        new_vatin = VATIN(
            country_code = vatin_data.get('country_code'),
            number = vatin_data.get('number'),
            initial_tax_date = vatin_data.get('initial_tax_date'),
            valid_from = vatin_data.get('valid_from'),
            valid_to = vatin_data.get('valid_to'),
            valid = vatin_data.get('valid'),
            name = vatin_data.get('name'),
            address = vatin_data.get('address'),
            business_id = vatin_data.get('business_id')
            )

        db.session.add(new_vatin)
        db.session.commit()

    @staticmethod
    def get_vatin_or_None_and_verify(transaction_input: TransactionInput, country_code_temp: str, number_temp: str, date: date) -> VATIN:
        from ...business.service_parent import BusinessService


        vatin = VATINService.get_vatin_if_number(country_code_temp, number_temp, date)
        if isinstance(vatin, VATIN):
            business = BusinessService.get_by_name_address_or_None(vatin.name, vatin.address)

        # if isinstance(business, SellerFirm):
            # if not business.id != vatin.business_id: #potentially a notification
            #     notification_data = {
            #         'subject': '{}s Not Matching'.format(main_subject),
            #         'original_filename': original_filename,
            #         'status': 'warning',
            #         'message': 'The '.format(reference_value, calculated_value),
            #         'transaction_input_id': transaction_input_id
            #     }
            #     NotificationService.create_transaction_notification(notification_data)

        return vatin


    @staticmethod
    #kwargs can contain: seller_firm_public_id
    def process_vat_numbers_files_upload(vat_numbers_files: List[BinaryIO], **kwargs) -> Dict:
        BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config["BASE_PATH_STATIC_DATA_SELLER_FIRM"]

        file_type='vat_numbers'
        df_encoding = 'utf-8'
        delimiter = ';'
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM

        for file in vat_numbers_files:
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            VATINService.process_vat_numbers_file(file_path_in, file_type, df_encoding, delimiter, basepath, **kwargs)

        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(vat_numbers_files)))
        }

        return response_object


    # celery task !!
    @staticmethod
    def process_vat_numbers_file(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, **kwargs) -> List[Dict]:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_objects = VATINService.create_vatins(df, file_path_in, **kwargs)

        InputService.move_file_to_out(file_path_in, basepath, file_type)

        return response_objects

    # **kwargs['seller_firm_pulic_id'] may hold a seller firm's public id
    @staticmethod
    def create_vatins(df: pd.DataFrame, file_path_in: str, **kwargs) -> List[Dict]:
        from ...business.seller_firm.service import SellerFirmService

        VATIN_LIFESPAN = current_app.config["VATIN_LIFESPAN"]

        error_counter = 0
        total_number_vatins = len(df.index)
        input_type = 'vat number' #only used for response objects

        for i in range(total_number_vatins):

            country_code, number = VATINService.get_vat_from_df(df, i)

            valid_from = InputService.get_date_or_None(df, i, column='valid_from')
            valid_to = InputService.get_date_or_None(df, i, column='valid_to')

            if not valid_from:
                valid_from = date.today()
            if not valid_to:
                valid_to = valid_from + timedelta(days=VATIN_LIFESPAN)

            vatin = VATIN.query.filter_by(country_code=country_code, number=number).first()

            if vatin:
                if vatin.valid and valid_to > vatin.valid_to:
                    vatin.valid_to = valid_to
                    db.session.commit()
                    continue

            else:
                seller_firm_id = SellerFirmService.get_seller_firm_id(df=df, i=i, **kwargs)
                vatin = VATINService.create_vatin_by_request(country_code, number, valid_from, valid_to, business_id=seller_firm_id)
                if not isinstance(vatin, VATIN):
                    error_counter += 1



        response_objects = InputService.create_input_response_objects(file_path_in, input_type, total_number_vatins, error_counter)

        return response_objects

    @staticmethod
    def get_validity_period(date: date, **kwargs) -> List[date]:
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
    def get_vat_from_df(df: pd.DataFrame, i: int) -> List[str]:
        country_code_temp = InputService.get_str(df, i, column='country_code')
        number_temp = InputService.get_str(df, i, column='vatin')

        print('country_code_temp:', country_code_temp, flush=True)
        print('number_temp:', number_temp, flush=True)
        country_code, number = VATINService.vat_precheck(country_code_temp, number_temp)
        return country_code, number


    @staticmethod
    def create_vatin_by_request(country_code: str, number: str, valid_from: date, valid_to: date, business_id: int):
        vat = VIESService.send_request(country_code, number)

        valid = vat['valid']
        name = vat['name']
        address = vat['address']


        vatin_data = {
            'country_code': country_code,
            'number': number,
            'valid_from': valid_from,
            'valid_to': valid_to,
            'valid': valid,
            'name': name,
            'address': address,
            'business_id': business_id
            }

        try:
            vatin: VATIN = VATINService.create(vatin_data)
            return vatin
        except:
            db.session.rollback()






    @staticmethod
    def vat_precheck(country_code_temp: str, number_temp: str) -> List[str]:
        if not number_temp:
            return None

        elif not re.match(r"^[a-zA-Z]", number_temp):
            print('Case 1', flush=True)
            VATINService.verify(country_code, number_temp)
            country_code, number = country_code_temp, number_temp

        elif country_code_temp == number_temp[:2].strip():
            print('Case 2', flush=True)
            VATINService.verify(country_code_temp, number_temp[2:].strip())
            country_code, number = country_code_temp, number_temp[2:].strip()

        else:
            print('Case 3', flush=True)
            country_code = number_temp[:2].strip()
            number = number_temp[2:].strip()
            VATINService.verify(country_code, number)


        return country_code, number




    @staticmethod
    def verify(country_code: str, number: str) -> None:
        VATINService.verify_country_code(country_code)
        VATINService.verify_regex(country_code, number)

    @staticmethod
    def verify_country_code(country_code: str) -> None:
        if not re.match(r"^[a-zA-Z]", country_code):
            msg = "{} is not a valid ISO_3166-1 country code.".format(country_code)
            raise HTTPException(msg)

        elif country_code not in MEMBER_COUNTRY_CODES:
            msg = "{} is not a European member state.".format(country_code)
            raise HTTPException(msg)

    @staticmethod
    def verify_regex(country_code: str, number: str) -> None:
        print('country_code:', country_code, flush=True)
        print('number:', number, flush=True)
        country = dict(
            map(
                lambda x, y: (x, y),
                ("country", "validator", "formatter"),
                VIES_OPTIONS[country_code],
            )
        )
        print('VIES_OPTIONS[country_code]: ', VIES_OPTIONS[country_code], flush=True)
        print('country:', country, flush=True)
        if not country["validator"].match("{}{}".format(country_code, number)):
            msg = "{} does not match the country's VAT ID specifications.".format(
                country_code)
            raise HTTPException(msg)






class VIESService:

    @staticmethod #!! async??
    def send_request(country_code: str, number: str) -> Dict:
        from zeep import Client, helpers

        """VIES API response data."""
        client = Client(VIES_WSDL_URL)
        try:
            vat_zeep_object = client.service.checkVat(country_code, number)
            vat = helpers.serialize_object(vat_zeep_object)
            print('VIES API! | vat:', vat)
            return vat

        except Exception as e:
            msg="{} is not a valid VATIN.".format(country_code)
            raise HTTPException(msg)


    @staticmethod
    def sanitize_response_detail(vat: VATIN, parameter: str) -> str:
        return None if vat[parameter] == '---' else parameter
