import datetime
import uuid
from typing import List

from werkzeug.exceptions import Conflict, NotFound, Unauthorized

from app.extensions import db
from .model import SellerFirm
from .schema import seller_firm_dto

from ..email.service import EmailService



class SellerFirmService:
    @staticmethod
    def get_all() -> List[SellerFirm]:
        seller_firms = SellerFirm.query.all()
        return seller_firms

    @staticmethod
    def get_by_id(public_id: str) -> SellerFirm:
        seller_firm = SellerFirm.query.filter(
            SellerFirm.public_id == public_id).first()
        if seller_firm:
            return seller_firm


    @staticmethod
    def update(public_id: str, data_changes) -> SellerFirm:
        seller_firm = SellerFirmService.get_by_id(public_id)
        seller_firm.update(data_changes)
        db.session.commit()
        return accounting

    @staticmethod
    def delete_by_id(public_id: str):
        #check if accounting business exists in db
        seller_firm = SellerFirm.query.filter(
            SellerFirm.public_id == public_id).first()
        if seller_firm:
            db.session.delete(seller_firm)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Accounting firm (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This accounting firm does not exist.')

    @staticmethod
    def create_seller_firm(seller_firm_data) -> SellerFirm:
        seller_firm = SellerFirm.query.filter_by(
            company_name=seller_firm_data.get('company_name')).first()

        if not seller_firm:
            #create new accounting based on SellerFirm model
            new_seller_firm = SellerFirm(
                company_name=seller_firm_data.get('company_name')
                logo_image_name=seller_firm_data.get('logo_image_name')
            )
            #add accounting business to db
            db.session.add(new_seller_firm)
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
    def create_unclaimed_seller_firm(tax_auditor, seller_firm_data) -> SellerFirm:
        amazon_seller_id = seller_firm_data.get('amazon_seller_id')
        company_name = seller_firm_data.get('company_name')

        if amazon_seller_id and company_name:
            seller_firm_asi = SellerFirm.query.filter_by(amazon_seller_id=amazon_seller_id).first()
            seller_firm_cn = SellerFirm.query.filter_by(company_name=company_name).first()

            if seller_firm_asi and seller_firm_cn:
                if seller_firm_asi != seller_firm_cn:
                    seller_firm = seller_firm_asi
                    if seller_firm.accounting_firm_id != tax_auditor.employer_id:
                        response_object = {
                            'status': 'error',
                            'message': 'The details provided point to two different companies that have already been registered. Please establish a client connection with the company instead.'
                        }
                        return response_object

                    else:
                        response_object = {
                                'status': 'error',
                                'message': 'The details provided point to a company that has already been registered. Please establish a client connection with the company instead.'
                            }
                        return response_object

            elif seller_firm_asi and not seller_firm_cn:
                response_object = {
                    'status': 'error',
                    'message': 'The amazon unique identifier provided points to a company that has already been registered and the company name does not match. Please recheck the provided details.'
                    }
                return response_object

            elif seller_firm_cn and not seller_firm_asi:
                response_object = {
                    'status': 'error',
                    'message': 'The company name provided points to a company that has already been registered and the amazon unique identifier does not match. Please recheck the provided details.'
                }
                return response_object

            elif not seller_firm_cn and not seller_firm_asi:
                accounting_firm_seller_id = seller_firm_data.get('accounting_firm_seller_id')

                # create new unclaimed seller firm
                new_unclaimed_seller_firm = SellerFirm(
                    claimed=False,
                    amazon_seller_id=amazon_seller_id,
                    accounting_firm_id=tax_auditor.employer_id,
                    accounting_firm_seller_id=accounting_firm_seller_id
                )

                #add seller to db
                db.session.add(new_unclaimed_seller_firm)
                db.session.commit()

                # this implementation implies that the seller with an unclaimed account is not in control if or if not the tax_auditor sets her as her client
                # the pattern for claimed accounts requires authorization by the seller.
                return seller_firm

        else:
            response_object = {
                'status': 'error',
                'message': 'Please provide a valid amazon unique identifier and a valid company name.'
            }
            return response_object
