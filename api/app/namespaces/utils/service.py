import os
import shutil
from typing import List, BinaryIO, Dict
import pandas as pd
from datetime import datetime, date

from flask import g, current_app, send_from_directory
from . import TransactionNotification

from werkzeug.utils import secure_filename
from werkzeug.exceptions import UnsupportedMediaType, RequestEntityTooLarge, UnprocessableEntity
from app.extensions import db



class TemplateService:

    def download_file(filename: str):
        BASE_PATH_TEMPLATES = current_app.config['BASE_PATH_TEMPLATES']

        return send_from_directory(directory=BASE_PATH_TEMPLATES, filename=filename, as_attachment=True)


class HelperService:
    @staticmethod
    def get_date_from_str(date_string:str, date_format: str) -> date:
        try:
            date = datetime.strptime(date_string, date_format)
        except:
            raise UnprocessableEntity('Unreadable date format.')
        return date



class NotificationService:

    @staticmethod
    def get_by_transaction_input_id_status(transaction_input_id: int, status: str) -> List[TransactionNotification]:
        return TransactionNotification.query.filter_by(transaction_input_id=transaction_input_id).all()


    @staticmethod
    def create_notification_data(main_subject: str, original_filename: str, status: str, reference_value: str, calculated_value: str, transaction_input_id: int) -> Dict:
        notification_data = {
            'subject': '{}s Not Matching'.format(main_subject),
            'original_filename': original_filename,
            'status': status,
            'message': 'The reference value from the original transaction report ({}) differs from the calculated value ({}). The original reference value has been used for subsequent processing.'.format(reference_value, calculated_value),
            'transaction_input_id': transaction_input_id
        }
        return notification_data

    @staticmethod
    def create_transaction_notification(notification_data):
        new_notification = TransactionNotification(
            subject=notification_data.get('subject'),
            original_filename = notification_data.get('original_filename'),
            status = notification_data.get('status'),
            message = notification_data.get('message'),
            transaction_input_id = notification_data.get('transaction_input_id')
        )

        db.session.add(new_notification)
        db.session.commit()





class InputService:
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
                        print('get_date_or_None', date, flush=True)
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
    def get_str_or_None(df: pd.DataFrame, i:int, column:str) -> str:
        if pd.isnull(df.iloc[i][column]):
            return None
        else:
            try:
                string = str(df.iloc[i][column])
            except:
                print('get_str_or_None', flush=True)
                raise UnsupportedMediaType('Can not read date format.')

        return string


    @staticmethod
    def get_float(df: pd.DataFrame, i:int, column:str) -> float:
        if pd.isnull(df.iloc[i][column]):
            return 0.0
        else:
            try:
                flt = float(df.iloc[i][column])
            except:
                print('get_float', flt, flush=True)
                raise UnsupportedMediaType('Can not read float format.')

        return flt


    @staticmethod
    def get_bool(df: pd.DataFrame, i: int, column: str, value_true) -> bool:
        try:
            boolean = bool(df.iloc[i][column] == value_true)
        except:
            print('get_bool', boolean, flush=True)
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
                'message': '{} {}s had been uploaded earlier already and were skipped.'.format(str(redundancy_counter), input_type)
            }
            response_objects.append(response_object_info)

        if error_counter > 0:
            notification = ' However, please recheck the submitted file for invalid data.'

            response_object_error = {
                'status': 'warning',
                'message': 'For {} {}s, the necessary {} details could not be read.'.format(str(error_counter), input_type, input_type)
            }
            response_objects.append(response_object_error)

        filename = os.path.basename(file_path)

        ending = 's' if total_number_inputs != 1 else ''

        response_object = {
            'status': 'success',
            'message': 'The {} file "{}" ({} {}{} in total) has been {} uploaded.{}'.format(input_type, filename, str(total_number_inputs), input_type, ending, success_status, notification)
        }

        response_objects.append(response_object)

        return response_objects



    # # NEVER TRUST USER INPUT
    # @staticmethod
    # def store_files(uploaded_files):
    #     # create a message list (used for notifications in the frontend)
    #     response_objects = []

    #     if uploaded_files == []:
    #         raise NotFound('No files submitted.')

    #     else:
    #         for file in uploaded_files:
    #             file_path = InputService.store_file(file, allowed_extensions)
    #             file_paths.append(file_path)

    #         return file_paths




    @staticmethod
    def store_static_data_upload(file: BinaryIO, file_type: str) -> str:
        STATIC_DATA_ALLOWED_EXTENSIONS = current_app.config['STATIC_DATA_ALLOWED_EXTENSIONS']
        BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config['BASE_PATH_STATIC_DATA_SELLER_FIRM']

        print('STATIC_DATA_ALLOWED_EXTENSIONS:', STATIC_DATA_ALLOWED_EXTENSIONS, flush=True)

        try:
            file_path_in = InputService.store_file(file=file, allowed_extensions=STATIC_DATA_ALLOWED_EXTENSIONS, basepath=BASE_PATH_STATIC_DATA_SELLER_FIRM, file_type=file_type)
        except:
            raise

        return file_path_in



    @staticmethod
    def allowed_file(filename: str, allowed_extensions: List[str]) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


    @staticmethod
    def allowed_filesize(file_path: str) -> bool:
        MAX_FILE_SIZE_INPUT = current_app.config['MAX_FILE_SIZE_INPUT']

        file_size = os.stat(file_path).st_size


        if not file_size <= MAX_FILE_SIZE_INPUT:
            os.remove(file_path)

        return file_size <= MAX_FILE_SIZE_INPUT


    @staticmethod
    def store_file(file: BinaryIO, allowed_extensions: List[str], basepath: str, **kwargs) -> str:
        if InputService.allowed_file(filename=file.filename, allowed_extensions=allowed_extensions):
            stored_filename = secure_filename(file.filename)

            if 'file_type' in kwargs and ('in_out' not in kwargs or kwargs.get('in_out') == True):
                basepath_in = os.path.join(basepath, kwargs['file_type'], 'in')

            elif 'file_type' in kwargs and 'in_out' in kwargs and kwargs.get('in_out') == False:
                basepath_in = os.path.join(basepath, kwargs['file_type'])

            elif 'file_type' not in kwargs and ('in_out' not in kwargs or kwargs.get('in_out') == True):
                basepath_in = os.path.join(basepath, 'in')

            elif 'file_type' not in kwargs and 'in_out' in kwargs and kwargs.get('in_out') == False:
                basepath_in = os.path.join(basepath)


            os.makedirs(basepath_in, exist_ok=True)

            file_path_in = os.path.join(basepath_in, stored_filename)
            file.save(file_path_in)

            if InputService.allowed_filesize(file_path=file_path_in):
                return file_path_in

            else:
                raise RequestEntityTooLarge('Uploaded files exceed the file limit. Please reduce the number of files to be processed at once.')

        else:
            raise UnsupportedMediaType('The file {} is not allowed. Please recheck if the file extension matches {}'.format(filename, allowed_extensions))


    @staticmethod
    def move_file_to_out(file_path_in: str, basepath: str, file_type: str):
        basepath_in = os.path.join(basepath, file_type, 'in')
        basepath_out = os.path.join(basepath, file_type, 'out')
        os.makedirs(basepath_out, exist_ok=True)

        file_name = os.path.basename(file_path_in)
        file_path_out = os.path.join(basepath, file_type, 'out', file_name)
        try:
            shutil.move(file_path_in, file_path_out)
        except:
            raise


    @staticmethod
    def read_file_path_into_df(file_path: str, df_encoding: str, delimiter: str) -> pd.DataFrame:
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            print('file_name: ', file_name, flush=True)
            try:
                if file_name.lower().endswith('.csv'):
                    df = pd.read_csv(file_path, encoding=df_encoding, delimiter=delimiter)
                    print('df.head()', flush=True)
                    print(df.head(), flush=True)
                else:
                    print('Case "Read File Path: File extension invalid"', flush=True)
                    raise UnsupportedMediaType(
                        'File extension invalid (file: {}).'.format(file_name))
                return df
            except:
                print('Case "Read File Path: Cannot read file"', flush=True)

                raise UnsupportedMediaType(
                    'Cannot read file {}.'.format(file_name))

        else:
            raise  # !!! (not a file)
