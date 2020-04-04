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


# from app.extensions import db
# from .model import TaxData
# from .schema import tax_data_dto


class TaxDataService:
    # @staticmethod
    # def get_all() -> List[TaxData]:
    #     tax_data = TaxData.query.all()
    #     return tax_datas

    # @staticmethod
    # def get_by_id(public_id: str) -> TaxData:
    #     tax_data = TaxData.query.filter(TaxData.public_id == public_id).first()
    #     if tax_data:
    #         return tax_data
    #     else:
    #         raise NotFound('This tax data record does not exist.')

    # @staticmethod
    # def delete_by_id(public_id: str):
    #     #check if tax_data exists in db
    #     tax_data = TaxData.query.filter(TaxData.public_id == public_id).first()
    #     if tax_data:
    #         db.session.delete(tax_data)
    #         db.session.commit()

    #         response_object = {
    #             'status': 'success',
    #             'message': 'TaxData (Public ID: {}) has been successfully deleted.'.format(public_id)
    #         }
    #         return response_object
    #     else:
    #         raise NotFound('This tax_data does not exist.')

    @staticmethod
    # NEVER TRUST USER INPUT
    def upload_input(user, uploaded_files):
        if uploaded_files == []:
            raise NotFound('No files submitted.')
        i = 0
        for file in uploaded_files:
            i += 1
            print('check ' + str(i))
            print(file.filename)
            if file.filename == '':
                raise NotFound('Empty file uploaded.')

            if file and TaxDataService.allowed_file(file.filename):
                filename = secure_filename(file.filename)

                # the file is saved to a temporary path. The dir is named 'temp'
                temp_dirpath = os.path.join(
                    current_app.config['BASE_PATH_MEDIA'],
                    user,
                    # str(user.public_id),
                    'tax_data',
                    'temp'
                )

                temp_stored_name = "{}_tax_data_input_{}.csv".format(
                    (datetime.now().strftime('%Y%m')),
                    'temp'
                )

                # if not existent (exist_ok=True) the path to the temporary dir is being created
                os.makedirs(temp_dirpath, exist_ok=True)

                temp_file_path = os.path.join(temp_dirpath, temp_stored_name)

                file.save(temp_file_path)

                # the file size is compared to the allowed file size from config
                # if file size > allowed file size the file is being deleted.
                file_size = os.stat(temp_file_path).st_size
                if file_size > current_app.config['TAX_DATA_MAX_FILE_SIZE']:
                    os.remove(temp_file_path)
                    raise RequestEntityTooLarge(
                        'Uploaded file exceeds file limit.')

                else:
                    # once all checks are passed the file is renamed and moved into the final dir
                    name_info_list = TaxDataService.name_info_retrieve(
                        temp_file_path)

                    final_stored_name = "{}_tax_data_input_{}.csv".format(
                        name_info_list[0], name_info_list[1])

                    final_dirpath = os.path.join(
                        current_app.config['BASE_PATH_MEDIA'],
                        user,
                        # str(user.public_id),
                        'tax_data',
                        name_info_list[0]
                    )

                    os.makedirs(final_dirpath, exist_ok=True)
                    final_file_path = os.path.join(
                        final_dirpath, final_stored_name)
                    shutil.move(temp_file_path, final_file_path)
                    # a database entry for the file is being created
                    # TaxService.create_tax_record(#)

            else:
                raise UnsupportedMediaType(
                    'This is not an allowed type. Please provide a valid csv file.')

        response_object = {
            'status': 'success',
            'message': 'Tax data saved.'
        }
        return response_object

    @staticmethod
    def download_file(user, filename):
        try:
            dirpath = os.path.join(
                current_app.config['BASE_PATH_MEDIA'],
                user,  # str(user.public_id)
                'tax_data')
            #filename = '202004_tax_data_input_55462838340018328.csv'
            return send_from_directory(dirpath, filename=filename, as_attachment=True)
        except FileNotFoundError:
            raise NotFound('The requested file does not exist.')

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower(
            ) in current_app.config['TAX_DATA_ALLOWED_EXTENSIONS']

    @staticmethod
    def name_info_retrieve(temp_file_path):
        try:
            df = pd.read_csv(filepath_or_buffer=temp_file_path, sep=',')
            if (df.columns[0] == 'UNIQUE_ACCOUNT_IDENTIFIER' and
                    df.columns[1] == 'ACTIVITY_PERIOD'):
                activity_period = df.iloc[0][1]
                unique_account_identifier = df.iloc[0][0]
                return [activity_period, unique_account_identifier]
            else:
                raise UnsupportedMediaType(
                    'The file is not formatted properly. Please recheck.')

        except:
            raise UnsupportedMediaType(
                'Can not read csv. Make sure it is formatted properly.')

    # @staticmethod
    # def create_tax_record(user_data) -> TaxData:
    #     # create new user based on User model
    #     new_tax_data = TaxData(
    #         email=user_data.get('email'),
    #         password=user_data.get('password')
    #     )
    #     # add user to db
    #     db.session.add(new_user)
    #     db.session.commit()

    #     return new_user
    # else:
    #     raise Conflict('A user with this email adress already exists.')
