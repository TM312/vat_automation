import pandas as pd

from app.extensions import db
from flask import current_app
from .model import TaxAuditor

from ..service_parent import UserService

from ...media.tax_record.model import TaxRecord
from ...media.tax_record.service import TaxRecordService
from ...business.seller_firm.service import SellerFirmService


BASE_PATH_MEDIA = current_app.config["BASE_PATH_MEDIA"]
TAX_DATA_MAX_REQUEST_SIZE = current_app.config["TAX_DATA_MAX_REQUEST_SIZE"]
TAX_DATA_ALLOWED_EXTENSIONS = current_app.config["TAX_DATA_ALLOWED_EXTENSIONS"]


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
