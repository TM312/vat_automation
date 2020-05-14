import os
import shutil
from typing import List
import pandas as pd
from datetime import datetime

from flask import g, current_app, send_from_directory

from werkzeug.utils import secure_filename
from werkzeug.exceptions import UnsupportedMediaType, RequestEntityTooLarge

from ..business import SellerFirm



MAX_FILE_SIZE_INPUT = current_app.config['MAX_FILE_SIZE_INPUT']
BASE_PATH_TEMPLATES = current_app.config['BASE_PATH_TEMPLATES']

class TemplateService:

    def download_file(filename: str):
        return send_from_directory(directory=BASE_PATH_TEMPLATES, filename=filename, as_attachment=True)




class InputService:
    @staticmethod
    def get_date_or_None(df, i:int, column:str) -> date or None:
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
    def get_str(df, i:int, column:str) -> str:
        try:
            string = str(df.iloc[i][column])
        except:
            raise UnsupportedMediaType('Can not read str format.')
        return string


    @staticmethod
    def get_str_or_None(df, i:int, column:str) -> str or None:
        if pd.isnull(df.iloc[i][column]):
            return None
        else:
            try:
                string = str(df.iloc[i][column])
            except:
                raise UnsupportedMediaType('Can not read date format.')

        return string


    @staticmethod
    def get_float(df, i:int, column:str) -> float:
        if pd.isnull(df.iloc[i][column]):
            return 0.0
        else:
            try:
                flt = float(df.iloc[i][column])
            except:
                raise UnsupportedMediaType('Can not read float format.')

        return flt


    @staticmethod
    def get_bool(df, i:int, column:str, value_true) -> bool:
        try:
            boolean = bool(df.iloc[i][column] == value_true)
        except:
            raise UnsupportedMediaType('Can not read bool format.')

        return boolean


    @staticmethod
    def create_input_response_objects(file_path, input_type: str, total_number_inputs: int, error_counter: int, **kwargs) -> List[dict]:
        response_objects = []
        success_status = 'successfully'
        notification = ''

        if 'redundancy_counter' in kwargs and kwargs['redundancy_counter'] > 0:

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
    def get_seller_firm_id(df, i, **kwargs) -> list:
        if not 'seller_firm_id' in kwargs:
            seller_firm_public_id = InputService.get_str_or_None(df, i, column='seller_firm_id')
        else:
            seller_firm_public_id = kwargs['seller_firm_id']

        seller_firm = SellerFirm.query.filter_by(public_id=seller_firm_public_id).first()

        if seller_firm:
            seller_firm_id = seller_firm.id
            return seller_firm_id_list


    @staticmethod
    def store_static_data_upload(file: list, file_type: str) -> list:
        try:
            file_path_in = InputService.store_file(file=file, allowed_extensions=STATIC_DATA_ALLOWED_EXTENSIONS, basepath=BASE_PATH_STATIC_DATA_SELLER_FIRM, file_type=file_type)
        except:
            raise

        return file_path_in



    @staticmethod
    def allowed_file(filename: str, allowed_extensions: list) -> bool:
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower(
            ) in allowed_extensions


    @staticmethod
    def allowed_filesize(file_path: str) -> bool:
        file_size = os.stat(file_path).st_size
        if not file_size <= MAX_FILE_SIZE_INPUT:
            os.remove(file_path)


    @staticmethod
    def store_file(file, allowed_extensions: list, basepath: str, file_type: str):
        if allowed_file(filename=file.filename, allowed_extensions=allowed_extensions):
            filename = secure_filename(file.filename)
            stored_filename = "{}.{}".format(filename, filename.rsplit('.', 1)[1].lower())


            basepath_in = os.path.join(basepath, file_type, 'in')
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
    def read_file_path_into_df(file_path: str, df_encoding, delimiter):
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            try:
                if file_name.lower().endswith('.csv'):
                    df = pd.read_csv(file_path, encoding=df_encoding, delimiter=delimiter)
                else:
                    raise UnsupportedMediaType(
                        'File extension invalid (file: {}).'.format(file_name))
                return df
            except:
                raise UnsupportedMediaType(
                    'Cannot read file {}.'.format(file_name))

        else:
            raise  # !!! (not a file)





#     @staticmethod
#     def assess_amazon_csv_info(tax_auditor, amazon_seller_id, activity_period):

#         # check if seller firm from file exists in db
#         seller_firm = SellerFirm.query.filter(SellerFirm.amazon_seller_id == amazon_seller_id).first()

#         if seller_firm:

#             if tax_auditor.employer_id == seller_firm.accounting_firm_id:
#                     # i.e. a record is created for the own employer
#                 final_dirpath = os.path.join(
#                     BASE_PATH_MEDIA,
#                     str(seller_firm.public_id),
#                     'tax_record',
#                     activity_period
#                 )

#                     final_stored_name = "{}_tax_record_input_{}_amazon.csv".format(
#                         activity_period, seller_firm.accounting_firm_client_id)

#                 return [final_dirpath, final_stored_name, seller_firm]

#             else:
#                 response_object = {
#                     'status': 'error',
#                     'message': 'A seller firm with amazon unique identifier {} exists but has not established a client relationship with your company. Please establish this relationship first.'.format(amazon_seller_id)
#                 }

#                 return response_object

#         else:
#             response_object = {
#                 'status': 'error',
#                 'message': 'A seller firm with the amazon unique identifier {} has not been registered yet.'.format(amazon_seller_id)
#             }

#             return response_object


# @staticmethod
#     def name_info_retrieve(temp_file_path, filename):
#         try:
#             df = pd.read_csv(filepath_or_buffer=temp_file_path, sep=',')
#             if (df.columns[0] == 'UNIQUE_ACCOUNT_IDENTIFIER' and
#                     df.columns[1] == 'ACTIVITY_PERIOD'):
#                 activity_period = df.iloc[0][1]
#                 amazon_seller_id = df.iloc[0][0]
#                 platform = 'amazon'

#                 return [activity_period, amazon_seller_id, platform]
#             else:
#                 response_object = {
#                     'status': 'error',
#                     'message': 'Tax record file {} is not formatted properly. Please recheck.'.format(filename)
#                 }
#                 return response_object
#                 #raise UnsupportedMediaType()

#         except:
#             response_object = {
#                 'status': 'error',
#                 'message': 'Error at file {}: Can not read csv. Make sure it is formatted properly.'.format(filename)
#             }
#             return response_object
#             #raise UnsupportedMediaType()





# def upload_file(file):
#         if file.filename == '':
#                     response_object = {
#                         'status': 'error',
#                         'message': 'File {} is empty.'.format(filename)
#                     }
#                     response_objects.append(response_object)
#                     continue

#                 if TaxAuditorService.allowed_file(file.filename):

#                     temp_file_path, filename = TaxAuditorService.store_to_temp_path(
#                         tax_auditor, file)


#                     # once all checks are passed the file is renamed and moved into the final dir
#                     return_object = TaxAuditorService.name_info_retrieve(
#                         temp_file_path, filename)

#                     # check if List is returned from function (if not the return object is the response object for failed processing.)
#                     if isinstance(return_object, list):
#                         # assign explicit var names to the function output
#                         activity_period, amazon_seller_id, platform = return_object

#                         ##
#                         ## IF PLATFORM == 'amazon' --> check in file additional parameters.
#                         ##

#                         return_object = TaxAuditorService.assess_amazon_csv_info(
#                             tax_auditor, amazon_seller_id)

#                         if isinstance(return_object, list):
#                             final_dirpath, final_stored_name, seller_firm = return_object

#                             os.makedirs(final_dirpath, exist_ok=True)
#                             final_file_path = os.path.join(
#                                 final_dirpath, final_stored_name)
#                             shutil.move(temp_file_path, final_file_path)

#                             # #creating a database entry for the tax record
#                             # new_tax_record = TaxRecordService.create(
#                             #     user=tax_auditor,
#                             #     seller_firm=seller_firm,
#                             #     platform=platform
#                             #     final_dirpath=final_dirpath,
#                             #     activity_period=activity_period
#                             # )

#                             # #creating a database entry for the uploaded tax record input file
#                             # TaxRecordService.create_input(
#                             #     platform=platform,
#                             #     original_input_name=filename,
#                             #     formatted_input_name=final_stored_name,
#                             #     tax_record=new_tax_record
#                             # )

#                             # updating the user status, i.e. last_seen
#                             UserService.ping(tax_auditor, method_name=inspect.stack()[0][3],
#                                             service_context=TaxRecordService.__name__)

#                             response_object = {
#                                 'status': 'success',
#                                 'message': 'File {} successfully uploaded.'.format(filename)
#                             }

#                         else:
#                             response_object = return_object
#                     else:
#                         response_object = return_object

#                     response_objects.append(response_object)

#                 else:
#                     response_object = {
#                         'status': 'error',
#                         'message': 'The type of file {} is not allowed. Please provide a valid csv file.'.format(filename)
#                     }
#                     response_objects.append(response_object)
#                     #raise UnsupportedMediaType()

!!!!!
