import os
import shutil
import pandas as pd
from pathlib import Path
from typing import List
from datetime import datetime

from flask import current_app, g
from flask import send_from_directory

from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound, RequestEntityTooLarge, UnsupportedMediaType


from app.extensions import db
from .model import TaxRecord
# from .schema import tax_record_dto


class TaxRecordService:
    # @staticmethod
    # def get_all() -> List[TaxRecord]:
    #     tax_record = TaxRecord.query.all()
    #     return tax_records

    # @staticmethod
    # def get_by_id(public_id: str) -> TaxRecord:
    #     tax_record = TaxRecord.query.filter(TaxRecord.public_id == public_id).first()
    #     if tax_record:
    #         return tax_record
    #     else:
    #         raise NotFound('This tax data record does not exist.')

    # @staticmethod
    # def delete_by_id(public_id: str):
    #     #check if tax_record exists in db
    #     tax_record = TaxRecord.query.filter(TaxRecord.public_id == public_id).first()
    #     if tax_record:
    #         db.session.delete(tax_record)
    #         db.session.commit()

    #         response_object = {
    #             'status': 'success',
    #             'message': 'TaxRecord (Public ID: {}) has been successfully deleted.'.format(public_id)
    #         }
    #         return response_object
    #     else:
    #         raise NotFound('This tax_record does not exist.')

    @staticmethod
    # NEVER TRUST USER INPUT
    def upload_input(user, uploaded_files):
        # create a message list (used for notifications in the frontend)
        response_objects = []

        if uploaded_files == []:
            raise NotFound('No files submitted.')

        else:
            for file in uploaded_files:
                if file.filename == '':
                    response_object = {
                        'status': 'success',
                        'message': 'File {} is empty.'.format(filename)
                    }
                    response_objects.append(response_object)
                    continue
                    #raise NotFound('Empty file uploaded.')

                if file and TaxRecordService.allowed_file(file.filename):

                    # safety measure provided by Flask
                    filename = secure_filename(file.filename)

                    # the file is saved to a temporary path. The dir is named 'temp'
                    temp_dirpath = os.path.join(
                        current_app.config['BASE_PATH_MEDIA'],
                        # user,
                        str(user.public_id),
                        'tax_record',
                        'temp'
                    )

                    temp_stored_name = "{}_tax_record_input_{}.csv".format(
                        (datetime.now().strftime('%Y%m')),
                        'temp'
                    )

                    # if not existent (exist_ok=True) the path to the temporary dir is being created
                    os.makedirs(temp_dirpath, exist_ok=True)

                    temp_file_path = os.path.join(
                        temp_dirpath, temp_stored_name)

                    file.save(temp_file_path)

                    # the file size is compared to the allowed file size from config
                    # if file size > allowed file size the file is being deleted.
                    file_size = os.stat(temp_file_path).st_size
                    if file_size > current_app.config['TAX_DATA_MAX_REQUEST_SIZE']:
                        os.remove(temp_file_path)
                        raise RequestEntityTooLarge(
                            'Uploaded files exceed the file limit. Please reduce the number of files to be processed at once.')

                    else:
                        # once all checks are passed the file is renamed and moved into the final dir
                        return_object = TaxRecordService.name_info_retrieve(
                            temp_file_path, filename)

                        # check if List is returned from function (if not the return object is the response object for failed processing.)
                        if isinstance(return_object, list):
                            name_info_list = return_object
                            print('is List:' + filename)
                            # assign explicit var names to the function output
                            activity_period = name_info_list[0]
                            unique_account_identifier = name_info_list[1]

                            final_stored_name = "{}_tax_record_input_{}.csv".format(
                                activity_period, unique_account_identifier)

                            final_dirpath = os.path.join(
                                current_app.config['BASE_PATH_MEDIA'],
                                # user,
                                str(user.public_id),
                                'tax_record',
                                name_info_list[0]
                            )

                            os.makedirs(final_dirpath, exist_ok=True)
                            final_file_path = os.path.join(
                                final_dirpath, final_stored_name)
                            shutil.move(temp_file_path, final_file_path)

                            # a database entry for the file is being created
                            TaxRecordService.create_tax_record(
                                user=user,
                                final_dirpath=final_dirpath,
                                activity_period=activity_period,
                                unique_account_identifier=unique_account_identifier,
                                final_stored_name=final_stored_name,
                                filename=filename
                            )

                            response_object = {
                                'status': 'success',
                                'message': 'Tax record for file {} successfully created.'.format(filename)
                            }
                        else:
                            response_object = return_object

                        response_objects.append(response_object)

                else:
                    response_object = {
                        'status': 'error',
                        'message': 'The type of file {} is not allowed. Please provide a valid csv file.'.format(filename)
                    }
                    response_objects.append(response_object)

                    #raise UnsupportedMediaType()

            return response_objects


    @staticmethod
    def get_own(user):
        tax_records = TaxRecord.query.filter_by(owner_id=user.id).all().order_by(
            TaxRecord.created_on.desc())
        return tax_records


    @staticmethod
    def download_file(user, activity_period, filename):
        try:
            dirpath = os.path.join(
                current_app.config['BASE_PATH_MEDIA'],
                # user,
                str(user.public_id),
                'tax_record')
            #filename = '202004_tax_record_input_55462838340018328.csv'
            return send_from_directory(dirpath, filename=filename, as_attachment=True)
        except FileNotFoundError:
            raise NotFound('The requested file does not exist.')

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower(
            ) in current_app.config['TAX_DATA_ALLOWED_EXTENSIONS']

    @staticmethod
    def name_info_retrieve(temp_file_path, filename):
        try:
            df = pd.read_csv(filepath_or_buffer=temp_file_path, sep=',')
            if (df.columns[0] == 'UNIQUE_ACCOUNT_IDENTIFIER' and
                    df.columns[1] == 'ACTIVITY_PERIOD'):
                activity_period = df.iloc[0][1]
                unique_account_identifier = df.iloc[0][0]
                return [activity_period, unique_account_identifier]
            else:
                response_object = {
                    'status': 'error',
                    'message': 'Tax record file {} is not formatted properly. Please recheck.'.format(filename)
                }
                print("response object 'not formatted properly' for file :" + filename)
                return response_object
                #raise UnsupportedMediaType()

        except:
            response_object = {
                'status': 'error',
                'message': 'Error at file {}: Can not read csv. Make sure it is formatted properly.'.format(filename)
            }
            return response_object
            #raise UnsupportedMediaType()

    @staticmethod
    def followed_tax_records(tax_auditor):
        return TaxRecord.query.join(
            clients, (clients.c.client_id == TaxRecord.owner_id)).filter(
                clients.c.tax_auditor_id == tax_auditor.id).order_by(
                    TaxRecord.created_on.desc())


    @staticmethod
    def create_tax_record(
            user,
            final_dirpath,
            activity_period,
            unique_account_identifier,
            final_stored_name,
            filename) -> TaxRecord:

        # check if user already exists in db
        tax_record = TaxRecord.query.filter_by(
            unique_account_identifier=unique_account_identifier,
            activity_period=activity_period,
            platform='Amazon'
        ).first()

        if not tax_record:
            # create new user based on TaxRecord model
            new_tax_record = TaxRecord(
                activity_period=activity_period,
                unique_account_identifier=unique_account_identifier,
                owner_id=user.id,
                storage_dir=final_dirpath,
                original_input_name=filename,
                formatted_input_name=final_stored_name
            )
            # add new_tax_record to db
            db.session.add(new_tax_record)
            db.session.commit()

            return new_tax_record
        else:
            pass
            # TaxRecordService.update_tax_record()
