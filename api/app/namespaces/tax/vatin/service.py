import os
from typing import List, BinaryIO, Dict
import pandas as pd
from datetime import date, datetime, timedelta
import time
import re
from random import randint


from flask import current_app
from werkzeug.exceptions import HTTPException, FailedDependency, UnprocessableEntity, NotFound, ExpectationFailed

from app.extensions import (
    db,
    socket_io)

from .helpers import MEMBER_COUNTRY_CODES, VIES_WSDL_URL, VATIN_MAX_LENGTH, VIES_OPTIONS
from . import VATIN
from .interface import VATINInterface
from .schema import VatinSchemaSocket

from app.namespaces.transaction_input import TransactionInput
from app.namespaces.utils.service import InputService, NotificationService
from app.namespaces.tag.service import TagService

from app.extensions.socketio.emitters import SocketService




class VATINService:
    @staticmethod
    def get_all() -> List[VATIN]:
        return VATIN.query.all()

    @staticmethod
    def get_all_by_business_id(business_id: int) -> List[VATIN]:
        return VATIN.query.filter_by(business_id = business_id).all()

    @staticmethod
    def get_by_id(vatin_id: int) -> VATIN:
        return VATIN.query.filter_by(id = vatin_id).first()

    @staticmethod
    def get_by_public_id(vatin_public_id: str) -> VATIN:
        return VATIN.query.filter_by(public_id = vatin_public_id).first()


    @staticmethod
    def get_by_country_code_seller_firm_id(country_code: str, business_id: int) -> VATIN:
        return VATIN.query.filter(
            VATIN.country_code == country_code,
            VATIN.business_id == business_id
            ).first()

    @staticmethod
    def get_by_country_code_number_date(country_code: str, number: str, date: date) -> VATIN:
        return VATIN.query.filter(
            VATIN.country_code == country_code,
            VATIN.number==number,
            VATIN.valid_from<=date,
            VATIN.valid_to>=date
            ).first()

    @staticmethod
    def get_expiring(limit: int) -> List[VATIN]:
        return VATIN.query.filter(
            VATIN.valid == True,
            VATIN.valid_to <= date.today() + timedelta(days=10)
        ).limit(limit).all()

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
        vatin = VATINService.get_by_id(vatin_id)
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
    def get_vatin_if_number(country_code_temp: str, number_temp: str, date: date) -> VATIN:
        if not isinstance(number_temp, str):
            return None
        else:
            country_code, number = VATINService.vat_precheck(country_code_temp, number_temp)
            vatin = VATINService.get_by_country_code_number_date(country_code, number, date)
            if not isinstance(vatin, VATIN):
                try:
                    vatin_data = VIESService.send_request(country_code, number)
                    print('vatin_data in get_vatin_if_number', flush=True)
                    print('vatin_data: ', vatin_data, flush=True)
                except:
                    vatin_data = {
                        'country_code': country_code,
                        'number': number,
                        'valid': None,
                        'request_date': date.today(),
                        'name': None,
                        'address': None
                    }

                vatin_data['country_code'] = country_code,
                vatin_data['number'] = number,
                vatin_data['valid_from'] = date if vatin_data.get('valid') else None

                try:
                    vatin = VATINService.create(vatin_data)
                except:
                    db.session.rollback()
                    raise

            return vatin


    @staticmethod
    def create(vatin_data: VATINInterface) -> VATIN:
        new_vatin = VATIN(
            country_code = vatin_data.get('country_code'),
            number = vatin_data.get('number'),
            original_filename = vatin_data.get('original_filename'),
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
    def get_vatin_or_None(country_code_temp: str, number_temp: str, date: date) -> VATIN:
        business_vatin = VATINService.get_vatin_if_number(country_code_temp, number_temp, date)
        if isinstance(business_vatin, VATIN):
            from app.namespaces.business.service_parent import BusinessService
            from app.namespaces.business import Business
            business = BusinessService.get_by_name_address_or_None(business_vatin.name, business_vatin.address)

            if isinstance(business, Business):
                data_changes = {'business_id': business.id}
                business_vatin.update(data_changes)
                db.session.commit()

            return business_vatin



    @staticmethod
    def handle_vatin_data_upload(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: Dict) -> Dict:
        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_object = VATINService.create_vatins(df, file_path_in, seller_firm_id)
        tag = TagService.get_by_code('VAT_NUMBER')
        NotificationService.handle_seller_firm_notification_data_upload(seller_firm_id, user_id, tag, seller_firm_notification_data)
        InputService.move_file_to_out(file_path_in, basepath, file_type)

        return response_object


    @staticmethod
    def get_df_vars(df: pd.DataFrame, i: int, current: int, object_type_human_read: str) -> List:
        try:
            country_code, number = VATINService.get_vat_from_df(df, i)
        except:
            # send error status via socket
            message = 'Can not read country code/number of {} in row {} (file: {}).'.format(object_type_human_read, current+1, original_filename)
            raise ExpectationFailed(message)

        try:
            service_start_date = current_app.config.SERVICE_START_DATE
            valid_from = InputService.get_date_or_None(df, i, column='valid_from')
            if isinstance(valid_from, date):
                valid_from = valid_from if valid_from >= service_start_date else service_start_date
            else:
                tolerance = current_app.config.OLD_TRANSACTION_TOLERANCE_DAYS
                valid_from = date.today() - timedelta(days=tolerance)

        except:
            raise UnprocessableEntity('valid_from')

        if not isinstance(country_code, str):
            raise ExpectationFailed('country_code')

        if not isinstance(number, str):
            raise ExpectationFailed('number')

        if not isinstance(valid_from, date):
            raise ExpectationFailed('valid_from')

        return country_code, number, valid_from



    @staticmethod
    def create_vatins(df: pd.DataFrame, file_path_in: str, seller_firm_id: int) -> List[Dict]:
        from time import sleep

        error_counter = 0
        total = total_number_vatins = len(df.index)
        original_filename = os.path.basename(file_path_in)[:127]
        object_type = 'vat_number'
        object_type_human_read = 'vat number'
        duplicate_list = []
        duplicate_counter = 0

        if not seller_firm_id:
            # send error status via socket
            SocketService.emit_status_error_no_seller_firm(object_type)
            return False

        # send status update via socket
        SocketService.emit_status_success(0, total, original_filename, object_type)

        for i in range(total_number_vatins):
            current = i + 1

            try:
                country_code, number, valid_from = VATINService.get_df_vars(df, i, current, object_type_human_read)
            except Exception as e:
                if e.code == 422:
                    SocketService.emit_status_error_column_read(current, object_type, column_name=e.description)
                elif e.code == 417:
                    SocketService.emit_status_error_invalid_value(object_type, e.description)
                return False


            vatin = VATINService.get_by_country_code_number_date(country_code, number, date.today())

            if isinstance(vatin, VATIN) and vatin.valid:
                if isinstance(vatin.business_id, int):
                    if not duplicate_counter > 2:
                        message = 'The vat number "{}-{}" has already been processed earlier.'.format(country_code, number)
                        SocketService.emit_status_info(object_type, message)
                    total -= 1
                    duplicate_list.append('{}-{}'.format(country_code, number))
                    duplicate_counter += 1
                    continue #skipping duplicates

                else:
                    data_changes = {
                        'business_id': seller_firm_id
                    }
                    vatin.update(data_changes)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                        # send error status via socket
                        message = 'An error occured while updating the {} in row {} (file: {}). Please get in contact with one of the admins.'.format(object_type_human_read, current+1, original_filename)
                        SocketService.emit_status_error(object_type, message)
                        return False


            else:
                # VIES DB is unreliable therefore reducing requests per second
                sleep(randint(4, 6))
                try:
                    vatin_data = VIESService.send_request(country_code, number)
                except:
                    vatin_data = {
                        'country_code': country_code,
                        'number': number,
                    }

                    # send error status via socket
                    message = 'Valiation of vat number "{}-{}" temporarily unavailable. Please make sure that it is validated before submitting transaction reports containing the number.'.format(country_code, number)
                    SocketService.emit_status_warning(object_type, message)

                vatin_data['request_date'] = date.today()
                vatin_data['business_id'] = seller_firm_id
                vatin_data['original_filename'] = original_filename
                vatin_data['valid_from'] = valid_from

                if vatin and vatin_data['valid'] != None:
                    vatin.update(vatin_data)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()

                        # send error status via socket
                        message = 'An error occured while updating the {} in row {} (file: {}). Please get in contact with one of the admins.'.format(object_type_human_read, current+1, original_filename)
                        SocketService.emit_status_error(object_type, message)
                        return False

                else:
                    try:
                        vatin = VATINService.create(vatin_data)

                    except:
                        db.session.rollback()
                        error_counter += 1

                        # send error status via socket
                        message = 'Error at vat number "{}-{}" (file: {}). Please recheck.'.format(country_code, number, original_filename)
                        SocketService.emit_status_error(object_type, message)
                        return False

                # send status update via socket
                SocketService.emit_status_success(current, total, original_filename, object_type)


        # following the succesful processing, the vuex store is being reset
        # first cleared
        SocketService.emit_clear_objects(object_type)
        # then refilled
        VATINService.push_all_by_seller_firm_id(seller_firm_id, object_type)

        # send final status via socket
        SocketService.emit_status_final(total, original_filename, object_type, object_type_human_read, duplicate_list=duplicate_list)

        return True


    # List all files in a directory using scandir(): Returns an iterator of all the objects in a directory including file attribute information

    @staticmethod
    def push_all_by_seller_firm_id(seller_firm_id: int, object_type: str) -> None:
        socket_list = []
        vat_numbers = VATINService.get_all_by_business_id(seller_firm_id)
        for vat_number in vat_numbers:
            # push new distance sale to vuex via socket
            vat_number_json = VatinSchemaSocket.get_vatin_sub(vat_number)

            if len(vat_numbers) < 10:
                SocketService.emit_new_object(vat_number_json, object_type)
            else:
                socket_list.append(vat_number_json)

        if len(socket_list) > 0:
            SocketService.emit_new_objects(socket_list, object_type)




    @staticmethod
    def process_validation_request(vatin_data: VATINInterface) -> VATIN:
        country_code_temp = vatin_data.get('country_code')
        number_temp = vatin_data.get('number')

        country_code, number = VATINService.vat_precheck(
            country_code_temp, number_temp)
        if not country_code or not number:
            raise UnprocessableEntity('The submitted country code or number do not conform with the required standard.')

        vatin = VATINService.get_by_country_code_number_date(country_code, number, date.today())

        if vatin and vatin.valid:
            return vatin

        else:
            try:
                vatin_data = VIESService.send_request(country_code, number)
                vatin_data['request_date'] = date.today()

            except:
                vatin_data = {
                    'country_code': country_code,
                    'number': number,
                    'valid': None,
                    'request_date': date.today(),
                    'name': None,
                    'address': None
                }



            if vatin and vatin_data['valid'] != None:
                vatin.update(vatin_data)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
            else:
                try:
                    vatin = VATINService.create(vatin_data)
                    return vatin

                except:
                    db.session.rollback()
                    raise


    @staticmethod
    def compare_calculation_reference_old_transaction(transaction_id: int, transaction_input: TransactionInput, customer_vat_check_required: bool, tax_date: date, number: str) -> None:
        if number and not customer_vat_check_required:
            OLD_TRANSACTION_TOLERANCE_DAYS = current_app.config.OLD_TRANSACTION_TOLERANCE_DAYS

            reference_value = str(OLD_TRANSACTION_TOLERANCE_DAYS)
            calculated_value = str((date.today() - tax_date).days)

            notification_data=NotificationService.create_transaction_notification_data(
                main_subject='Transaction too old – No VAT check',
                original_filename=transaction_input.original_filename,
                status='info',
                reference_value='Transaction age tolerance: {} days.'.format(reference_value),
                calculated_value='Actual transaction age: {} days.'.format(calculated_value),
                transaction_id=transaction_id
                )
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
    def process_single_submit(seller_firm_public_id: str, vatin_data_raw: VATINInterface) -> VATIN:
        from app.namespaces.business.seller_firm.service import SellerFirmService

        country_code, number = VATINService.vat_precheck(vatin_data_raw.get('country_code'), vatin_data_raw.get('number'))

        if not country_code or not number:
            raise

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if seller_firm:
            vatin_data = vatin_data_raw
            vatin_data['country_code'] = country_code
            vatin_data['number'] = number
            vatin_data['business_id'] = seller_firm.id

            vatin = VATINService.get_by_country_code_number_date(country_code, number, date.today())

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
            msg = "{} is not a valid ISO 3166-1 country code.".format(country_code)
            raise HTTPException(msg)

        elif country_code not in MEMBER_COUNTRY_CODES:
            msg = "{} is not a European member state.".format(country_code)
            raise HTTPException(msg)

    @staticmethod
    def verify_regex(country_code: str, number: str) -> None:
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
                current_app.logger.warning('Exception: {} | ZEEP Request failed for VATIN: {}-{}'.format(e, country_code, number))
                raise


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
