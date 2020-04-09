import datetime
import uuid
from typing import List

from werkzeug.exceptions import Conflict, NotFound, Unauthorized

from app.extensions import db
from .model import Accounting
from .schema import accounting_dto

from ..email.service import EmailService



class AccountingService:
    @staticmethod
    def get_all() -> List[Accounting]:
        accountings = Accounting.query.all()
        return accountings

    @staticmethod
    def get_by_id(public_id: str) -> Accounting:
        accounting = Accounting.query.filter(Accounting.public_id == public_id).first()
        if accounting:
            return accounting
        else:
            raise NotFound('This accounting does not exist.')

    @staticmethod
    def update(public_id: str, data_changes) -> Accounting:
        accounting = AccountingService.get_by_id(public_id)
        accounting.update(data_changes)
        db.session.commit()
        return accounting

    @staticmethod
    def delete_by_id(public_id: str):
        #check if accounting exists in db
        accounting = Accounting.query.filter(Accounting.public_id == public_id).first()
        if accounting:
            db.session.delete(accounting)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Accounting (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This accounting does not exist.')

    @staticmethod
    def create_accounting_business(accounting_data) -> Accounting:
        accounting = Accounting.query.filter_by(
            company_name=accounting_data.get('company_name')).first()

        if not accounting:
            #create new accounting based on Accounting model
            new_accounting = Accounting(
                company_name=accounting_data.get('company_name')
                logo_image_name=accounting_data.get('logo_image_name')
            )
            #add accounting to db
            db.session.add(new_accounting)
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
    def get_all_clients(public_id: str) -> List[Accounting]
        clients = Accounting.query.filter(
            Accounting.public_id == public_id).clients.all()
        return clients






    # @staticmethod
    # def create_client(client_data)

    #     # checks for existing client
    #     client = Accounting.query.filter_by(
    #             tax_auditor_seller_id=accounting_data.get('tax_auditor_seller_id'),
    #             tax_auditor_company=tax_auditor.company_name
    #             ).first()

    #             if not client:
    #                 #create new accounting based on Accounting model
    #                 new_unclaimed_seller = Accounting(
    #                     claimed = False,
    #                     role = 'seller',
    #                     tax_auditor_seller_id=accounting_data.get(
    #                         'tax_auditor_seller_id'),
    #                     tax_auditor_company=tax_auditor.company_name,
    #                     company_name = accounting_data.get(
    #                         'company_name'),
    #                 )
    #                 #add accounting to db
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
