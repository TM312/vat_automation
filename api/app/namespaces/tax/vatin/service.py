from typing import List, BinaryIO, Dict
import pandas as pd
from datetime import date, datetime, timedelta
import time
import re
from random import randint


from flask import current_app
from werkzeug.exceptions import HTTPException, FailedDependency, UnprocessableEntity, NotFound

from app.extensions import db

from .helpers import MEMBER_COUNTRY_CODES, VIES_WSDL_URL, VATIN_MAX_LENGTH, VIES_OPTIONS
from . import VATIN
from .interface import VATINInterface

from ...transaction_input import TransactionInput
from ...utils.service import InputService, NotificationService



class VATINService:
    @staticmethod
    def get_all() -> List[VATIN]:
        vatins = VATIN.query.all()
        return vatins

    @staticmethod
    def get_by_id(vatin_id: int) -> VATIN:
        return VATIN.query.filter(VATIN.id == vatin_id).first()

    @staticmethod
    def get_by_public_id(vatin_public_id: str) -> VATIN:
        return VATIN.query.filter_by(public_id = vatin_public_id).first()

    @staticmethod
    def get_by_country_code_seller_firm(country_code: str, seller_firm: 'app.namespaces.business.seller_firm.SellerFirm') -> VATIN:
        return VATIN.query.join(seller_firm.vat_numbers).filter_by(country_code).first()

    @staticmethod
    def get_by_country_code_seller_firm_id(country_code, business_id) -> VATIN:
        return VATIN.query.filter(VATIN.country_code == country_code, VATIN.business_id == business_id).first()

    @staticmethod
    def update(vatin_id: int, data_changes: VATINInterface) -> VATIN:
        vatin = VATINService.get_by_id(vatin_id)
        vatin.update(data_changes)
        db.session.commit()
        return vatin

    @staticmethod
    def update_by_public_id(vatin_public_id: str, data_changes: VATINInterface) -> VATIN:
        vatin = VATINService.get_by_public_id(vatin_public_id)
        if vatin:
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
            raise NotFound('This vat number does not exist.')


    @staticmethod
    def delete_by_public_id(vatin_public_id: str):
        vatin = VATINService.get_by_public_id(vatin_public_id)
        if vatin:
            db.session.delete(vatin)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'VATIN (code: {}) has been successfully deleted.'.format(vatin_public_id)
            }
            return response_object
        else:
            raise NotFound('This vat number does not exist.')



    @staticmethod
    def get_vatin(country_code: str, number: str, date: date) -> VATIN:
        return VATIN.query.filter(VATIN.country_code == country_code, VATIN.number==number, VATIN.valid_from<=date, VATIN.valid_to>=date).first()



    @staticmethod
    def get_vatin_if_number(country_code_temp: str, number_temp: str, date: date) -> VATIN:
        if not isinstance(number_temp, str):
            return None
        else:
            try:
                country_code, number = VATINService.vat_precheck(country_code_temp, number_temp)
                vatin = VATINService.get_vatin(country_code, number, date)
                if not isinstance(vatin, VATIN):
                    vatin_data = VIESService.send_request(country_code, number)

                    vatin_data['country_code'] = country_code,
                    vatin_data['number'] = number,
                    vatin_data['valid_from'] = date if vatin_data.get('valid') else None

                    try:
                        vatin = VATINService.create(vatin_data)
                    except:
                        db.session.rollback()

            except:
                raise

            return vatin


    @staticmethod
    def create(vatin_data: VATINInterface) -> VATIN:
        new_vatin = VATIN(
            country_code = vatin_data.get('country_code'),
            number = vatin_data.get('number'),
            initial_tax_date = vatin_data.get('initial_tax_date'),
            valid_from = vatin_data.get('valid_from'),
            request_date = vatin_data.get('request_date'),
            valid = vatin_data.get('valid'),
            name = vatin_data.get('name'),
            address = vatin_data.get('address'),
            business_id = vatin_data.get('business_id')
            )

        db.session.add(new_vatin)
        db.session.commit()

        return new_vatin

    @staticmethod
    def get_vatin_or_None_and_verify(transaction_input: TransactionInput, country_code_temp: str, number_temp: str, date: date) -> VATIN:
        from ...business.service_parent import BusinessService

        vatin = VATINService.get_vatin_if_number(country_code_temp, number_temp, date)
        # if isinstance(vatin, VATIN):
        #     business = BusinessService.get_by_name_address_or_None(vatin.name, vatin.address)

        return vatin


    @staticmethod
    def process_vat_numbers_files_upload(vat_numbers_files: List[BinaryIO], seller_firm_public_id: str) -> Dict:
        from ...business.seller_firm.service import SellerFirmService

        BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config["BASE_PATH_STATIC_DATA_SELLER_FIRM"]

        file_type='vat_numbers'
        df_encoding = 'utf-8'
        delimiter = ';'
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM
        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)

        for file in vat_numbers_files:
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            VATINService.process_vat_numbers_file(file_path_in, file_type, df_encoding, delimiter, basepath, seller_firm.id)

        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(vat_numbers_files)))
        }

        return response_object


    # celery task !!
    @staticmethod
    def process_vat_numbers_file(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, seller_firm_id: int) -> List[Dict]:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_objects = VATINService.create_vatins(df, file_path_in, seller_firm_id)

        InputService.move_file_to_out(file_path_in, basepath, file_type)

        return response_objects

    @staticmethod
    def create_vatins(df: pd.DataFrame, file_path_in: str, seller_firm_id: int) -> List[Dict]:
        from time import sleep

        error_counter = 0
        total_number_vatins = len(df.index)
        input_type = 'vat number' #only used for response objects

        for i in range(total_number_vatins):
            country_code, number = VATINService.get_vat_from_df(df, i)
            if (country_code is None or number is None):
                continue

            vatin = VATIN.query.filter(VATIN.country_code==country_code, VATIN.number==number, VATIN.valid_to >= date.today()).first()

            if vatin:
                if isinstance(vatin.business_id, int):
                    continue

                else:
                    vatin.business_id = seller_firm_id
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                        raise

            else:
                # VIES DB is unreliable therefore reducing requests per second
                sleep(randint(4, 6))
                print("SLEEP in create_vatins", flush=True)
                vatin_data = VIESService.send_request(country_code, number)

                if seller_firm_id:
                    vatin_data['business_id'] = seller_firm_id

                valid_from = InputService.get_date_or_None(df, i, column='valid_from')

                if not valid_from:
                    valid_from = date.today()

                vatin_data['valid_from'] = valid_from

                try:
                    VATINService.create(vatin_data)

                except:
                    db.session.rollback()
                    error_counter += 1


        response_objects = InputService.create_input_response_objects(file_path_in, input_type, total_number_vatins, error_counter)

        return response_objects

    @staticmethod
    def evaluate_transaction_notification(transaction_id: int, customer_vat_check_required: bool, date: date, number: str) -> None:
        if number and not customer_vat_check_required:
            OLD_TRANSACTION_TOLERANCE_DAYS = current_app.config['OLD_TRANSACTION_TOLERANCE_DAYS']

            reference_value = str(OLD_TRANSACTION_TOLERANCE_DAYS)
            calculated_value = str(date.today() - date).days

            notification_data = {
                   'subject': 'Old Transaction',
                    'original_filename': transaction_input.original_filename,
                    'status': 'info',
                    'reference_value': reference_value,
                    'calculated_value': calculated_value,
                    'message': 'Due to the age of the tax date the customer firm VAT Number ({}) it was assumed to be valid without further checks.'.format(number),
                    'transaction_id': transaction_input.id
                   }
            try:
                NotificationService.create_transaction_notification(notification_data)
            except:
                db.session.rollback()
                raise


    @staticmethod
    def get_vat_from_df(df: pd.DataFrame, i: int) -> List[str]:
        country_code_temp = InputService.get_str(df, i, column='country_code')
        number_temp = InputService.get_str(df, i, column='number')
        country_code, number = VATINService.vat_precheck(country_code_temp, number_temp)
        return country_code, number


    @staticmethod
    def vat_precheck(country_code_temp: str, number_temp_unform: str) -> List[str]:
        if (country_code_temp == 'nan'
            or number_temp_unform == 'nan'
            or not number_temp_unform
        ):
            return None, None

        if not country_code_temp:
            country_code_temp = number_temp_unform[:2].strip()
        else:
            country_code_temp.upper().replace(" ", "")

        number_temp = number_temp_unform.upper().replace(" ", "")

        if not re.match(r"^[a-zA-Z][a-zA-Z]", number_temp):
            VATINService.verify(country_code_temp, number_temp)
            country_code, number = country_code_temp, number_temp

        elif country_code_temp == number_temp[:2].strip():
            VATINService.verify(country_code_temp, number_temp[2:].strip())
            country_code, number = country_code_temp, number_temp[2:].strip()

        else:
            country_code = number_temp[:2].strip()
            number = number_temp[2:].strip()
            VATINService.verify(country_code, number)

        return country_code, number


    @staticmethod
    def process_verification_request(vatin_data: VATINInterface) -> Dict:
        country_code_temp = vatin_data.get('country_code')
        number_temp = vatin_data.get('number')

        try:
            country_code, number = VATINService.vat_precheck(country_code_temp, number_temp)
            if not country_code or not number:
                response_object = {
                    'status': 'error',
                    'verified': False,
                    'country_code': None,
                    'number': None
                }

            else:
                response_object = {
                    'status': 'success',
                    'verified': True,
                    'country_code': country_code,
                    'number': number
                }

        except:
            response_object = {
                'status': 'success',
                'verified': False,
                'country_code': country_code_temp,
                'number': number_temp
            }

        finally:
            return response_object

    @staticmethod
    def process_validation_request(vatin_data: VATINInterface) -> VATIN:
        country_code_temp = vatin_data.get('country_code')
        number_temp = vatin_data.get('number')

        country_code, number = VATINService.vat_precheck(country_code_temp, number_temp)
        if not country_code or not number:
            raise UnprocessableEntity('The submitted country code or number do not conform with the required standard.')

        vatin = VATINService.get_vatin(country_code, number, date.today())

        if vatin:
            return vatin

        else:
            try:
                vatin_data = VIESService.send_request(country_code, number)
                try:
                    vatin = VATINService.create(vatin_data)
                    return vatin

                except:
                    db.session.rollback()
                    raise UnprocessableEntity('Can not create VATIN.')

            except:
                raise FailedDependency('Could not validate country code and number at the VIES database.')



    @staticmethod
    def process_single_submit(seller_firm_public_id: str, vatin_data_raw: VATINInterface) -> VATIN:
        from ...business.seller_firm.service import SellerFirmService

        country_code, number = VATINService.vat_precheck(vatin_data_raw.get('country_code'), vatin_data_raw.get('number'))

        if not country_code or not number:
            raise

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if seller_firm:
            vatin_data = vatin_data_raw
            vatin_data['country_code'] = country_code
            vatin_data['number'] = number
            vatin_data['business_id'] = seller_firm.id

            vatin = VATIN.query.filter_by(country_code=country_code, number=number).first()

            if not vatin:
                vatin = VATINService.process_validation_request(vatin_data_raw)

            data_changes = {k:v for k,v in vatin_data.items() if (v is not None and v != getattr(vatin, k))}
            if data_changes:
                vatin.update(data_changes)
                db.session.commit()
            return vatin

        else:
            raise NotFound('The indicated seller firm does not exist.')




    @staticmethod
    def verify(country_code: str, number: str) -> None:
            VATINService.verify_country_code(country_code)
            VATINService.verify_regex(country_code, number)

    @staticmethod
    def verify_country_code(country_code: str) -> None:
        if not re.match(r"^[a-zA-Z][a-zA-Z]", country_code):
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

        if not country["validator"].match("{}{}".format(country_code, number)):
            msg = "{} does not match the country's VAT ID specifications.".format(
                country_code)
            raise HTTPException(msg)





class VIESService:

    @staticmethod #!! async??
    def send_request(country_code: str, number: str) -> Dict:

        """VIES API response data."""
        try:
            vatin_data = VIESService.send_request_via_urllib(country_code, number)

        except Exception as e:
            current_app.logger.warning('Exception: {} | URLLIB Request failed for VATIN: {}-{}'.format(e, country_code, number))
            try:
                # VIES DB is unreliable therefore reducing requests per second
                from time import sleep
                sleep(randint(4,6))
                vatin_data = VIESService.send_request_via_zeep(country_code, number)

            except:
                vatin_data = {
                    'country_code': country_code,
                    'number': number,
                    'valid': None,
                    'request_date': date.today(),
                    'name': None,
                    'address': None
                }
                current_app.logger.warning('Exception: {} | ZEEP Request failed for VATIN: {}-{}'.format(e, country_code, number))

        finally:
            print('FINALlY vatin_data:', vatin_data, flush=True)
            return vatin_data


    @staticmethod
    def send_request_via_urllib(country_code: str, number: str) -> Dict:
        #adapted from here: https://github.com/ajcerejeira/vat-validator/blob/master/vat_validator/vies.py
        from urllib import request
        import xml.etree.ElementTree as ET

        # Prepare the SOAP request
        envelope = ET.Element(
            "soapenv:Envelope",
            attrib={
                "xmlns:hs": "urn:ec.europa.eu:taxud:vies:services:checkVat:types",
                "xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
            },
        )
        body = ET.SubElement(envelope, "soapenv:Body")
        action = ET.SubElement(body, "hs:checkVat")
        ET.SubElement(action, "hs:countryCode").text = country_code
        ET.SubElement(action, "hs:vatNumber").text = number
        payload = ET.tostring(envelope, encoding="utf-8")

        # Send the SOAP request to VIES Webservice
        url = "http://ec.europa.eu/taxation_customs/vies/services/checkVatService"
        req = request.Request(url, data=payload)
        res = request.urlopen(req)

        # Parse the result
        res_envelope = ET.fromstring(res.read())
        namespace = "urn:ec.europa.eu:taxud:vies:services:checkVat:types"
        request_date = res_envelope.find(".//{{{}}}requestDate".format(namespace))
        valid = res_envelope.find(".//{{{}}}valid".format(namespace))
        name = res_envelope.find(".//{{{}}}name".format(namespace))
        address = res_envelope.find(".//{{{}}}address".format(namespace))

        vatin_data = {
            'country_code': country_code,
            'number': number,
            'valid': valid is not None and valid.text == "true",
            'request_date': datetime.strptime(request_date.text, "%Y-%m-%d%z").date()
                            if request_date is not None and request_date.text is not None
                            else None,
            'name': name.text if (name is not None and name.text != '---') else None,
            'address': address.text if (address is not None and address.text != '---') else None
        }

        return vatin_data

    @staticmethod
    def send_request_via_zeep(country_code: str, number: str) -> Dict:
        from zeep import Client, helpers
        client = Client(VIES_WSDL_URL)
        vat_zeep_object = client.service.checkVat(country_code, number)
        vat = helpers.serialize_object(vat_zeep_object)
        vatin_data = {
            'country_code': country_code,
            'number': number,
            'valid': vat['valid'],
            'request_date': vat['requestDate'] if isinstance(vat.get(['requestDate']), date) else None,
            'name': None if vat['address'] == '---' else vat['address'],
            'address': None if vat['name'] == '---' else vat['name']
        }

        return vatin_data


    @staticmethod
    def sanitize_response_detail(vat: VATIN, parameter: str) -> str:
        return None if vat[parameter] == '---' else parameter
