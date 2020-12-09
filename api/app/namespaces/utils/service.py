import os
import shutil
from typing import List, BinaryIO, Dict, Union
import pandas as pd
from datetime import datetime, date, timedelta

from flask import g, current_app, send_from_directory
from . import TransactionNotification, SellerFirmNotification
from .interface import SellerFirmNotificationInterface

from werkzeug.utils import secure_filename
from werkzeug.exceptions import UnsupportedMediaType, RequestEntityTooLarge, UnprocessableEntity, InternalServerError
from app.extensions import db

from app.namespaces.business import Business

class TemplateService:

    # Actions related to handling templates

    def download_file(filename: str):
        BASE_PATH_TEMPLATES = current_app.config.BASE_PATH_TEMPLATES
        try:
            return send_from_directory(BASE_PATH_TEMPLATES, filename, as_attachment=True, mimetype="text/csv", attachment_filename=filename)
        except Exception as e:
            print(e, flush=True)

    @staticmethod
    def get_valid_from(df: pd.DataFrame, i: int, obj, klass):
        service_start_date = current_app.config.SERVICE_START_DATE
        valid_from = InputService.get_date_or_None(df, i, column='valid_from')
        if isinstance(valid_from, date):
            valid_from = valid_from if valid_from >= service_start_date else service_start_date
        else:
            if isinstance(obj, klass):
                valid_from = date.today()
            else:
                valid_from = service_start_date
        return valid_from


class HelperService:
    # Actions for variable manipulations

    @staticmethod
    def get_date_from_str(date_string:str, date_format: str) -> date:
        try:
            date = datetime.strptime(date_string, date_format)
        except:
            raise UnprocessableEntity('Unreadable date format.')
        return date

    @staticmethod
    def stringify(string_raw: str) -> str:
        import re
        pattern = re.compile(r'-{2,}')
        #https://stackoverflow.com/questions/23996118/replace-special-characters-in-a-string-python
        string = string_raw.lower().translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}).replace(" ", "-").strip("-")
        return re.sub(pattern, "-", string)

    @staticmethod
    def stringify_snake_case(string_raw: str) -> str:
        import re
        pattern = re.compile(r'-{2,}')
        #https://stackoverflow.com/questions/23996118/replace-special-characters-in-a-string-python
        string = string_raw.lower().translate(
            {ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=-+"}).replace(" ", "_").strip("-")
        return re.sub(pattern, "_", string)


    @staticmethod
    def get_earliest_date(*dates: List[date]) -> date:
        return min([datum for datum in dates if datum is not None])


class HistoryService:
    # Actions related to history objects


    @staticmethod
    def handle_update(obj_id: int, HistoryClass, ObjHistoryService, data_changes: Dict):
        """
            When updating 3 cases can exist:

            CASE EARLIER: The update's valid_from attribute is EARLIER than any other history object.
                1. New history obj is created
                2. Oldest history obj retrieved
                3. Missing data change attributes complemented by those from oldest history obj
                4. New history obj valid_to == oldest history pbj valid_from - timedelta(days=1)

            CASE EQUAL: The update's valid_from attribute is EQUAL to another history object.
                1. Data changes are implemented for the retrieved history object

            CASE LATER (main case): The update's valid_from attribute is LATER than the currently valid history object.
                1. New history obj is created
                2. Current history obj retrieved
                3. Missing data change attributes complemented by those from history obj
                4. Current history obj valid_to == new history obj valid_from - timedelta(days=1)

        """

        #retrieve valid_from to decide for case
        valid_from = data_changes['valid_from']
        history_obj = ObjHistoryService.get_by_relationship_date(obj_id, valid_from)

        # CASE EARLIER
        if not isinstance(history_obj, HistoryClass):
            #1.
            new_history_obj = ObjHistoryService.create_empty(obj_id)
            #2.
            history_obj = ObjHistoryService.get_oldest(obj_id)
            #3. and #4.
            all_attr = {**history_obj.attr_as_dict(), **data_changes}
            all_attr['valid_to'] = history_obj.valid_from - timedelta(days=1)
            new_history_obj.update(all_attr)

        else:
            # CASE EQUAL
            if valid_from == history_obj.valid_from:
                history_obj.update(data_changes)


            # CASE LATER
            else:
                history_obj = ObjHistoryService.get_current(obj_id)
                #1.
                new_history_obj = ObjHistoryService.create_empty(obj_id)
                #(2.) -> already exists
                # #3.
                all_attr = {**history_obj.attr_as_dict(), **data_changes}
                all_attr['valid_from'] = valid_from
                new_history_obj.update(all_attr)

                # #4.
                history_obj.valid_to = valid_from - timedelta(days=1)




class NotificationService:

    @staticmethod
    def get_seller_firm_shared(seller_firm_id: int, user_id: int, time: datetime, subject: str) -> SellerFirmNotification:
        timespan_in_min = current_app.config.TIMESPAN_SIMILARITY
        seller_firm_notification = SellerFirmNotification.query.filter(
            SellerFirmNotification.seller_firm_id == seller_firm_id,
            SellerFirmNotification.created_by == user_id,
            SellerFirmNotification.created_on.between(time - timedelta(minutes=timespan_in_min), time),
            SellerFirmNotification.subject == subject
        ).first()

        return seller_firm_notification

    @staticmethod
    def get_all_key_account_notifications() -> List[SellerFirmNotification]:
        notifications_per_query = current_app.config.NOTIFICATIONS_PER_QUERY

        from app.namespaces.user.tax_auditor import TaxAuditor
        from app.namespaces.business.seller_firm import SellerFirm

        seller_firm_notifications = SellerFirmNotification.query.join(
            SellerFirm.notifications
            ).join(
                SellerFirm.tax_auditors, aliased=True
        ).filter_by(id=g.user.id).order_by(SellerFirmNotification.created_on.desc()).limit(notifications_per_query).all()

        return seller_firm_notifications



    @staticmethod
    def create_seller_firm_notification(seller_firm_notification_data: SellerFirmNotificationInterface) -> SellerFirmNotification:

        new_notification = SellerFirmNotification(
            subject=seller_firm_notification_data.get('subject'),
            status=seller_firm_notification_data.get('status'),
            message=seller_firm_notification_data.get('message'),
            seller_firm_id=seller_firm_notification_data.get('seller_firm_id'),
            created_by=seller_firm_notification_data.get('created_by')
        )

        db.session.add(new_notification)
        db.session.commit()

        return new_notification



    @staticmethod
    def create_transaction_notification_data(main_subject: str, original_filename: str, status: str, reference_value: str, calculated_value: str, transaction_id: int) -> Dict:

        notification_data = {
            'subject': '{}s Not Matching'.format(main_subject),
            'original_filename': original_filename,
            'status': status,
            'reference_value': str(reference_value),
            'calculated_value': str(calculated_value),
            'transaction_id': transaction_id
        }
        return notification_data

    @staticmethod
    def create_transaction_notification(notification_data):
        new_notification = TransactionNotification(
            subject=notification_data.get('subject'),
            original_filename = notification_data.get('original_filename'),
            status = notification_data.get('status'),
            reference_value = notification_data.get('reference_value'),
            calculated_value = notification_data.get('calculated_value'),
            message = notification_data.get('message'),
            transaction_id = notification_data.get('transaction_id')
        )

        db.session.add(new_notification)
        db.session.commit()


        return new_notification


    @staticmethod
    def handle_seller_firm_notification_data_upload(seller_firm_id: int, user_id: int, tag: str, seller_firm_notification_data: SellerFirmNotificationInterface) -> None:
        # if multiple files containing data for the same seller are uploaded, the same notification is used and extended in terms of tags
        seller_firm_notification = NotificationService.get_seller_firm_shared(seller_firm_id, user_id, datetime.utcnow(), subject='Data Upload')
        if not isinstance(seller_firm_notification, SellerFirmNotification):
            seller_firm_notification = NotificationService.create_seller_firm_notification(seller_firm_notification_data)

        if not tag in seller_firm_notification.tags:
            seller_firm_notification.tags.append(tag)

            #if the same data has been uploaded within 5 minutes it is not being considered as modified.
            if (datetime.utcnow() - seller_firm_notification.created_on) >= timedelta(minutes=5):
                seller_firm_notification.modify()

            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise







class InputService:

    # Actions for handling files or data frames



    @staticmethod
    def get_date_or_None(df: pd.DataFrame, i:int, column:str) -> date:
        if pd.isnull(df.iloc[i][column]):
            return None
        else:
            try:
                date = datetime.strptime(df.iloc[i][column], '%d-%m-%Y').date()
            except:
                try:
                    date = datetime.strptime(df.iloc[i][column], '%d.%m.%Y').date()
                except:
                    try:
                        date = datetime.strptime(df.iloc[i][column], '%d.%m.%y').date()
                    except:
                        raise UnsupportedMediaType('Can not read date format.')
        return date


    @staticmethod
    def get_str(df: pd.DataFrame, i: int, column: str) -> str:
        try:
            string = str(df.iloc[i][column])
        except:
            raise UnsupportedMediaType('Can not read str format.')
        return string

    @staticmethod
    def get_single_str_compact(df: pd.DataFrame, i: int, column: str) -> str:
        try:
            string_unform = str(df.iloc[i][column])
            string = InputService.clean_str(string_unform)
        except:
            raise UnsupportedMediaType('Can not read str format.')
        return string


    @staticmethod
    def get_str_or_None(df: pd.DataFrame, i:int, column:str) -> str:
        if pd.isnull(df.iloc[i][column]):
            return None
        else:
            try:
                string = str(df.iloc[i][column])
            except:
                raise UnsupportedMediaType('Can not read date format.')

        return string

    @staticmethod
    def clean_str(string: str) -> str:
        string_trimmed = string.replace(',', '')
        string_trimmed = string_trimmed.replace(' ', '')
        string_trimmed = string_trimmed.replace("'", "")
        return string_trimmed

    @staticmethod
    def get_float_or_None(df: pd.DataFrame, i:int, column:str) -> float:
        if pd.isnull(df.iloc[i][column]):
            return None
        else:
            try:
                flt = float(df.iloc[i][column])
            except:
                try:
                    string = df.iloc[i][column]
                    string_trimmed = InputService.clean_str(string)
                    flt = float(string_trimmed)

                except:
                    raise UnsupportedMediaType('Can not read float format.')

        return flt


    @staticmethod
    def get_bool(df: pd.DataFrame, i: int, column: str, value_true) -> bool:
        try:
            df_value = df.iloc[i][column]
            if isinstance(df_value, str) and isinstance(value_true, str):
                boolean = bool(df_value.upper() == value_true.upper())

            boolean = bool(df_value == value_true)
        except:
            raise UnsupportedMediaType('Can not read bool format.')

        return boolean


    @staticmethod
    def create_input_response_objects(file_path, input_type: str, total_number_inputs: int, error_counter: int, **kwargs):
        response_objects = []
        success_status = 'successfully'
        notification = ''

        if isinstance(kwargs.get('redundancy_counter'), int) and kwargs.get('redundancy_counter') > 0:

            response_object_info = {
                'status': 'info',
                'message': '{} {}s had been uploaded earlier already and were skipped.'.format(str(kwargs.get('redundancy_counter')), input_type)
            }
            response_objects.append(response_object_info)

        if error_counter > 0:
            notification = ' However, please recheck the submitted file for invalid data.'

            response_object_error = {
                'status': 'warning',
                'message': 'For {} {}s, the necessary {} details could not be read.'.format(str(error_counter), input_type, input_type)
            }
            response_objects.append(response_object_error)

        # problem if file is already deleted
        filename = os.path.basename(file_path)

        ending = 's' if total_number_inputs != 1 else ''

        response_object = {
            'status': 'success',
            'message': 'The {} file "{}" ({} {}{} in total) has been {} uploaded.{}'.format(input_type, filename, str(total_number_inputs), input_type, ending, success_status, notification)
        }

        response_objects.append(response_object)

        return response_objects


    @staticmethod
    def determine_file_type(df: pd.DataFrame) -> str:
        column_name_list = df.columns.tolist()

        if ('channel_code' in column_name_list and 'channel_code' in column_name_list):
            return 'account_list'

        elif ('arrival_country_code' in column_name_list
            and 'active' in column_name_list
            and 'ship_from_rule' in column_name_list
            ):
            return 'distance_sale_list'

        elif ('SKU' in column_name_list
            and 'name' in column_name_list
            and 'tax_code' in column_name_list
            and 'unit_cost_price_currency_code' in column_name_list):
            return 'item_list'

        elif ('country_code' in column_name_list and 'number' in column_name_list):
            return 'vat_numbers'

        elif ('UNIQUE_ACCOUNT_IDENTIFIER' in column_name_list
              and 'SALES_CHANNEL' in column_name_list
              and 'TRANSACTION_EVENT_ID' in column_name_list
              and 'ACTIVITY_TRANSACTION_ID' in column_name_list
              and 'SELLER_SKU' in column_name_list ):
              return 'transactions_amazon'

        elif ('seller_firm_name' in column_name_list
            and	'address' in column_name_list
            and	'establishment_country_code' in column_name_list):
            return 'seller_firm'

        else:
            os.remove(file_path_in)
            raise UnprocessableEntity('Unable to identify the file type')




    @staticmethod
    def infer_delimiter(file_path_in: str) -> str:
        reader = pd.read_csv(file_path_in, sep=None, iterator=True, engine='python')
        inferred_sep = reader._engine.data.dialect.delimiter
        return inferred_sep





    @staticmethod
    def allowed_file(filename: str, allowed_extensions: List[str]) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


    @staticmethod
    def allowed_filesize(file_path: str) -> bool:
        MAX_FILE_SIZE_INPUT = current_app.config.MAX_FILE_SIZE_INPUT

        file_size = os.stat(file_path).st_size


        if not file_size <= MAX_FILE_SIZE_INPUT:
            os.remove(file_path)

        return file_size <= MAX_FILE_SIZE_INPUT

    @staticmethod
    def get_secure_filename(file: BinaryIO) -> str:
        return secure_filename(file.filename)


    @staticmethod
    def store_file(file: BinaryIO, allowed_extensions: List[str], basepath: str, business_id: int, file_type: str) -> str:
        if InputService.allowed_file(filename=file.filename, allowed_extensions=allowed_extensions):
            stored_filename = InputService.get_secure_filename(file)

            basepath_in = os.path.join(basepath, str(business_id), file_type, 'in')

            os.makedirs(basepath_in, exist_ok=True)

            file_path_in = os.path.join(basepath_in, stored_filename)

            try:
                file.save(file_path_in)
            except:
                raise UnprocessableEntity('Can not store file. Please contact one of the admins.')

            if InputService.allowed_filesize(file_path=file_path_in):
                return file_path_in

            else:
                raise RequestEntityTooLarge('The uploaded file "{}" exceeds the file limit.'.format(stored_filename))

        else:
            raise UnsupportedMediaType('The file type "{}" is not allowed. Please recheck if the file extension matches one of the following: {}'.format(filename, allowed_extensions))


    @staticmethod
    def move_data_to_file_type(file_path_tbd: str, file_type: str, business_id: int):

        basepath = current_app.config.BASE_PATH_BUSINESS_DATA
        basepath_file_type = os.path.join(basepath, str(business_id), file_type, 'in')
        os.makedirs(basepath_file_type, exist_ok=True)

        file_name = os.path.basename(file_path_tbd)
        file_path_file_type = os.path.join(basepath_file_type, file_name)
        try:
            shutil.move(file_path_tbd, file_path_file_type)
            return file_path_file_type
        except:
            raise


    @staticmethod
    def move_file_to_out(file_path_in: str, basepath: str, file_type: str, business_id: int):
        basepath_in = os.path.join(basepath, str(business_id), file_type, 'in')
        basepath_out = os.path.join(basepath, str(business_id), file_type, 'out')
        os.makedirs(basepath_out, exist_ok=True)

        file_name = os.path.basename(file_path_in)
        file_path_out = os.path.join(basepath_out, file_name)
        try:
            shutil.move(file_path_in, file_path_out)
        except:
            raise


    @staticmethod
    def read_file_path_into_df(file_path: str, df_encoding: str, delimiter: str) -> pd.DataFrame:
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            try:
                if file_name.lower().endswith('.csv') or file_name.lower().endswith('.txt'):
                    df_raw = pd.read_csv(file_path, encoding=df_encoding, delimiter=delimiter)
                    df = InputService.clean_df(df_raw)

                else:
                    raise UnsupportedMediaType('File extension invalid (file: {}).'.format(file_name))
                return df
            except:
                raise UnsupportedMediaType('Cannot read file {}.'.format(file_name))

        else:
            raise InternalServerError('Not a path: {}'.format(file_path))  # !!! (not a file)


    @staticmethod
    def clean_df(df_raw: pd.DataFrame) -> pd.DataFrame:

        df = df_raw.dropna(how='all')
        #formatting to handle bad input
        df.columns = df.columns.str.strip('')
        df.columns = df.columns.str.replace('(,$)|(^,)', '', regex=True) #removes , from both ends of column

        return df
