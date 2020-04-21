from typing import List

from werkzeug.exceptions import Conflict, NotFound, Unauthorized

from app.extensions import db
from .model import AccountingFirm
from .schema import accounting_firm_dto

from ...user.tax_auditor.model import TaxAuditor


class AccountingFirmService:
    @staticmethod
    def get_own(tax_auditor: TaxAuditor) -> AccountingFirm:
        #check if accounting_firm exists by querying the Business table for the tax_auditors employer id
        accounting_firm = AccountingFirm.query.filter(
            AccountingFirm.id == tax_auditor.employer.id).first()
        if accounting_firm:
            return accounting_firm
        else:
            raise NotFound('This accounting firm does not exist.')

    @staticmethod
    def update_own(tax_auditor: TaxAuditor, data_changes) -> AccountingFirm:
        #check if accounting_firm exists by querying the Business table for the tax_auditors employer id
        accounting_firm = AccountingFirm.query.filter(
            AccountingFirm.id == tax_auditor.employer.id).first()
        if accounting_firm:
            accounting_firm.update(data_changes)
            db.session.commit()
            return accounting_firm
        else:
            raise NotFound('This accounting firm does not exist.')


    @staticmethod
    def delete_own(tax_auditor: TaxAuditor):
        #check if accounting_firm exists by querying the Business table for the tax_auditors employer id
        accounting_firm = AccountingFirm.query.filter(
            AccountingFirm.id == tax_auditor.employer.id).first()
        if accounting_firm:
            db.session.delete(accounting_firm)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Accounting firm (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This accounting firm does not exist.')

    @staticmethod
    def create_accounting_firm(accounting_firm_data) -> AccountingFirm:
        accounting_firm = AccountingFirm.query.filter_by(
            company_name=accounting_firm_data.get('company_name')).first()

        if not accounting_firm:
            #create new accounting based on AccountingFirm model
            new_accounting_firm = AccountingFirm(
                company_name=accounting_firm_data.get('company_name')
                logo_image_name=accounting_firm_data.get('logo_image_name')
            )
            #add accounting business to db
            db.session.add(new_accounting_firm)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object

        else:
            response_object = {
                'status': 'error',
                'message': 'An accounting business with this name has already been registered.'
            }
            return response_object



    @staticmethod
    def get_own_clients(tax_auditor: TaxAuditor):
        #check if accounting_firm exists by querying the Business table for the tax_auditors employer id
        accounting_firm=AccountingFirm.query.filter(
            AccountingFirm.id == tax_auditor.employer.id).first()
        if accounting_firm:
            return accounting_firm.clients.all()



    # @staticmethod
    # def create_client(client_data)

    #     # checks for existing client
    #     client = AccountingFirm.query.filter_by(
    #             tax_auditor_seller_id=accounting_firm_data.get('tax_auditor_seller_id'),
    #             tax_auditor_company=tax_auditor.company_name
    #             ).first()

    #             if not client:
    #                 #create new accounting business based on AccountingFirm model
    #                 new_unclaimed_seller = AccountingFirm(
    #                     claimed = False,
    #                     role = 'seller',
    #                     tax_auditor_seller_id=accounting_firm_data.get(
    #                         'tax_auditor_seller_id'),
    #                     tax_auditor_company=tax_auditor.company_name,
    #                     company_name = accounting_firm_data.get(
    #                         'company_name'),
    #                 )
    #                 #add accounting business to db
    #                 db.session.add(new_unclaimed_seller)
    #                 db.session.commit()

    #                 # this implementation implies that the seller with an unclaimed account is not in control if the tax_auditor sets her as her client
    #                 # the pattern for claimed accounts requires authorization by the seller.
    #                 response_object = {
    #                     'status': 'success',
    #                     'message': 'A new client has successfully been added.'.format(public_id)
    #                 }
    #                 return response_object

    #             else:
    #                 response_object = {
    #                     'status': 'error',
    #                     'message': 'A client with the auditing id: {} already exists. Please check the list of clients where you can follow/unfollow each one.'.format(public_id)
    #                 }
    #                 return response_object
