import pandas as pd

from app.extensions import db

from .model import TaxAuditor

from ..service_parent import UserService

from ...media.tax_record.model import TaxRecord
from ...media.tax_record.service import TaxRecordService
from ...business.seller_firm.service import SellerFirmService

class TaxAuditorService:
    # seller tax_auditor register self path
    # check if tax_auditor already exists in db
    def create_self(tax_auditor_data) -> TaxAuditor:
        tax_auditor = TaxAuditor.query.filter_by(email=tax_auditor_data.get('email')).first()
        if not tax_auditor:
            # the tax_auditor provides an 'id' which is the internal public_id attribute of the accounting_firm object
            employer_public_id = tax_auditor_data.get('employer_id')
            accounting_firm = AccountingFirm.query.filter_by(public_id=employer_public_id).first()
            if not accounting_firm:
                response_object = {
                    'status': 'error',
                    'message': 'The provided id ({}) does not match with any accounting firm in the database. Please recheck the provided id.'.format(public_id)
                }
                return response_object

            #create new tax_auditor based on TaxAuditor model
            new_tax_auditor = TaxAuditor(
                email=tax_auditor_data.get('email'),
                password=tax_auditor_data.get('password')
                employer_id=accounting_firm.id,
                role='employee'
            )

            #add tax_auditor to db
            db.session.add(new_tax_auditor)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }

            # """ Send Confirmation Email to tax_auditor email """
            # confirmation_link = EmailService.generate_confirmation_url(new_tax_auditor.email)
            # print(confirmation_link)
            # EmailService.send_email(
            #     subject='Registration',
            #     recipients = [new_tax_auditor.email],
            #     template='email_confirmation.html',
            #     confirmation_link=confirmation_link,
            # )

            return response_object
        else:
            response_object = {
                'status': 'error',
                'message': 'A tax_auditor with the this email address already exists. Try logging in instead.'.format(public_id)
            }
            return response_object


    @staticmethod
    def follow(tax_auditor: TaxAuditor, seller_firm_public_id: str):

        # check if seller_firm exists
        seller_firm = SellerFirmService.get_by_id(public_id=seller_firm_public_id)
        if seller_firm:
            # check authorization
            if tax_auditor.employer_id == seller_firm.accounting_firm_id:
                #check if value in association table already 1
                if not tax_auditor.is_following(seller_firm.id):
                    tax_auditor.key_accounts.append(seller_firm)
                    db.session.commit()

                    UserService.ping(tax_auditor, method_name=inspect.stack()[0][3],
                                     service_context=TaxAuditorService.__name__)

                    return tax_auditor

                else:
                    response_object = {
                        'status': 'error',
                        'message': 'You are already following {}'.format(seller_firm.name)
                    }

            else:
                response_object = {
                    'status': 'error',
                    'message': 'You are not authorized to follow {}'.format(seller_firm.name)
                }

        else:
            response_object = {
                'status': 'error',
                'message': 'The requested seller firm id does not exist.'
            }

        return response_object


    @staticmethod
    def unfollow(tax_auditor, seller_firm_public_id: str):
        seller_firm = SellerFirmService.get_by_id(public_id=seller_firm_public_id)
        if seller_firm:
            if tax_auditor.is_following(seller_firm.id):
                tax_auditor.key_accounts.remove(seller_firm)
                db.session.commit()

                UserService.ping(tax_auditor, method_name=inspect.stack()[0][3],
                                 service_context=TaxAuditorService.__name__)

            return tax_auditor

        else:
            response_object = {
                'status': 'error',
                'message': 'The requested seller firm id does not exist.'
            }
        return response_object



    @staticmethod
    def update(tax_auditor: TaxAuditor, data_changes) -> TaxAuditor:
        tax_auditor.update(data_changes)
        tax_auditor.update_last_seen()
        db.session.commit()
        return tax_auditor

    @staticmethod
    def delete_by_id(public_id: str):
        #check if tax_auditor exists in db
        tax_auditor = TaxAuditor.query.filter(TaxAuditor.public_id == public_id).first()
        if tax_auditor:
            db.session.delete(tax_auditor)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Tax auditor (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This tax auditor does not exist.')


@staticmethod
   # NEVER TRUST USER INPUT
   def upload_input(tax_auditor, uploaded_files):
        # create a message list (used for notifications in the frontend)
        response_objects = []

        if uploaded_files == []:
            raise NotFound('No files submitted.')

        else:
            for file in uploaded_files:
                if file.filename == '':
                    response_object = {
                        'status': 'error',
                        'message': 'File {} is empty.'.format(filename)
                    }
                    response_objects.append(response_object)
                    continue

                if  TaxAuditorService.allowed_file(file.filename):

                    temp_file_path, filename = TaxAuditorService.store_to_temp_path(
                        tax_auditor, file)


                    # once all checks are passed the file is renamed and moved into the final dir
                    return_object = TaxAuditorService.name_info_retrieve(
                        temp_file_path, filename)

                    # check if List is returned from function (if not the return object is the response object for failed processing.)
                    if isinstance(return_object, list):
                        # assign explicit var names to the function output
                        activity_period, amazon_seller_id, platform = return_object

                        ##
                        ## IF PLATFORM == 'amazon' --> check in file additional parameters.
                        ##

                        return_object = TaxAuditorService.assess_amazon_csv_info(
                            tax_auditor, amazon_seller_id)

                        if isinstance(return_object, list):
                            final_dirpath, final_stored_name, seller_firm = return_object

                            os.makedirs(final_dirpath, exist_ok=True)
                            final_file_path = os.path.join(
                                final_dirpath, final_stored_name)
                            shutil.move(temp_file_path, final_file_path)

                            #creating a database entry for the tax record
                            new_tax_record = TaxRecordService.create(
                                user=tax_auditor,
                                seller_firm=seller_firm,
                                platform=platform
                                final_dirpath=final_dirpath,
                                activity_period=activity_period
                            )

                            #creating a database entry for the uploaded tax record input file
                            TaxRecordService.create_input(
                                platform=platform,
                                original_input_name=filename,
                                formatted_input_name=final_stored_name,
                                tax_record=new_tax_record
                            )

                            # updating the user status, i.e. last_seen
                            UserService.ping(tax_auditor, method_name=inspect.stack()[0][3],
                                            service_context=TaxRecordService.__name__)

                            response_object = {
                                'status': 'success',
                                'message': 'Tax record for file {} successfully created.'.format(filename)
                            }

                        else:
                            response_object = return_object
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
    def store_to_temp_path(tax_auditor, file):

        # safety measure provided by Flask
        filename = secure_filename(file.filename)

        # the file is saved to a temporary path relating to the uploader's company. The dir is named 'temp'
        temp_dirpath = os.path.join(
            current_app.config['BASE_PATH_MEDIA'],
            str(tax_auditor.employer.public_id),
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

        return [temp_file_path, filename]



    @staticmethod
    def assess_amazon_csv_info(tax_auditor, amazon_seller_id, activity_period):

        # check if seller firm from file exists in db
        seller_firm = SellerFirm.query.filter(SellerFirm.amazon_seller_id == amazon_seller_id).first()

        if seller_firm:

            if tax_auditor.employer_id == seller_firm.accounting_firm_id:
                    # i.e. a record is created for the own employer
                final_dirpath = os.path.join(
                    current_app.config['BASE_PATH_MEDIA'],
                    str(seller_firm.public_id),
                    'tax_record',
                    activity_period
                )

                    final_stored_name = "{}_tax_record_input_{}_amazon.csv".format(
                        activity_period, seller_firm.accounting_firm_seller_id)

                return [final_dirpath, final_stored_name, seller_firm]

            else:
                response_object = {
                    'status': 'error',
                    'message': 'A seller firm with amazon unique identifier {} exists but has not established a client relationship with your company. Please establish this relationship first.'.format(amazon_seller_id)
                }

                return response_object

        else:
            response_object = {
                'status': 'error',
                'message': 'A seller firm with the amazon unique identifier {} has not been registered yet.'.format(amazon_seller_id)
            }

            return response_object


    @staticmethod
    def download_file(tax_auditor: TaxAuditor, tax_record_id: int, filename: str):

        # check if seller firm from file exists in db
        tax_record = Tax_Record.query.filter(Tax_Record.id == tax_record_id).first()

        if tax_record:
            #check if tax_auditor authorized to access file.
            if tax_record.accounting_firm_id == tax_auditor.employer_id:
                TaxRecordService.download_file(tax_record, filename)

            else:
                response_object = {
                    'status': 'error',
                    'message': 'You are not autorized to access the requested file. The accounting firm associated with the record differs from your employer. Please request the file directly from the owner of the record.'
                }

        else:
            response_object = {
                'status': 'error',
                'message': 'The requested file does not exist.'
            }

        return response_object



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
                amazon_seller_id = df.iloc[0][0]
                platform = 'amazon'

                return [activity_period, amazon_seller_id, platform]
            else:
                response_object = {
                    'status': 'error',
                    'message': 'Tax record file {} is not formatted properly. Please recheck.'.format(filename)
                }
                return response_object
                #raise UnsupportedMediaType()

        except:
            response_object = {
                'status': 'error',
                'message': 'Error at file {}: Can not read csv. Make sure it is formatted properly.'.format(filename)
            }
            return response_object
            #raise UnsupportedMediaType()
