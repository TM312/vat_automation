import datetime
import uuid
from typing import List

from werkzeug.exceptions import Conflict, NotFound, Unauthorized

from app.extensions import db
from .model import Seller
from .schema import seller_dto

from ..email.service import EmailService
from ..auth.service import TokenService


class SellerService:
    @staticmethod
    def get_all() -> List[Seller]:
        sellers = Seller.query.all()
        return sellers

    @staticmethod
    def get_by_id(public_id: str) -> Seller:
        seller = Seller.query.filter(Seller.public_id == public_id).first()
        if seller:
            return seller
        else:
            raise NotFound('This seller does not exist.')

    @staticmethod
    def get_by_email(email: str) -> Seller:
        seller = Seller.query.filter(Seller.email == email).first()
        if seller:
            return seller
        else:
            raise NotFound('This seller does not exist.')

    @staticmethod
    def update(seller: Seller, data_changes) -> Seller:
        seller.update(data_changes)
        seller.last_seen()
        db.session.commit()
        return seller


    @staticmethod
    def delete_by_id(public_id: str):
        #check if seller exists in db
        seller = Seller.query.filter(Seller.public_id == public_id).first()
        if seller:
            db.session.delete(seller)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Seller (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This seller does not exist.')

    @staticmethod
    def create_seller(seller_data) -> Seller:
        # tax_auditor registers unclaimed seller path

        # if a tax_auditor attempts to register an unclaimed seller account
        #   - seller_data contains:
        #       - seller.public_id as "tax_auditor_public_id" (provided by nuxt directly) (not relying on g.seller because unregisterd sellers may register)
        #       - seller.tax_auditor_seller_id
        #   - seller_data does not contain: 'email', 'password'

        tax_auditor_public_id = seller_data.get('tax_auditor_public_id', None)
        if tax_auditor_public_id:
            # loads tax_auditor seller object if in db
            tax_auditor = Seller.query.filter_by(public_id=tax_auditor_public_id).first()

            if not tax_auditor:
                response_object = {
                    'status': 'error',
                    'message': 'There appears to be a problem with your account. Please try again. If the problem persists, please get in contact with one of the administrators. (Public ID: {}) '.format(public_id)
                }
                return response_object

            else:
                # a client (already) exists, if a seller exists that
                # -  has a tax_auditor_id that is the same as the one provided through the (nuxt) form (by the tax_auditor)
                # - AND has a tax_auditor_company value which is equal to the tax_auditor's company name.

                # checks for existing client
                client = Seller.query.filter_by(
                        tax_auditor_seller_id=seller_data.get('tax_auditor_seller_id'),
                        tax_auditor_company=tax_auditor.company_name
                        ).first()

                if not client:
                    #create new seller based on Seller model
                    new_unclaimed_seller = Seller(
                        claimed = False,
                        role = 'seller',
                        tax_auditor_seller_id=seller_data.get(
                            'tax_auditor_seller_id'),
                        tax_auditor_company=tax_auditor.company_name,
                        company_name = seller_data.get(
                            'company_name'),
                    )
                    #add seller to db
                    db.session.add(new_unclaimed_seller)
                    db.session.commit()

                    # this implementation implies that the seller with an unclaimed account is not in control if the tax_auditor sets her as her client
                    # the pattern for claimed accounts requires authorization by the seller.
                    response_object = {
                        'status': 'success',
                        'message': 'A new client has successfully been added.'.format(public_id)
                    }
                    return response_object

                else:
                    response_object = {
                        'status': 'error',
                        'message': 'A client with the auditing id: {} already exists. Please check the list of clients where you can follow/unfollow each one.'.format(public_id)
                    }
                    return response_object


        # seller seller register self path
        # check if seller already exists in db
        else:
            seller = Seller.query.filter_by(email = seller_data.get('email')).first()
            if not seller:
                #create new seller based on Seller model
                new_seller = Seller(
                    email = seller_data.get('email'),
                    password = seller_data.get('password')
                    claimed = True,
                    role ='seller'
                )
                #add seller to db
                db.session.add(new_seller)
                db.session.commit()

                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.'
                }

                # """ Send Confirmation Email to seller email """
                # confirmation_link = EmailService.generate_confirmation_url(new_seller.email)
                # print(confirmation_link)
                # EmailService.send_email(
                #     subject='Registration',
                #     recipients = [new_seller.email],
                #     template='email_confirmation.html',
                #     confirmation_link=confirmation_link,
                # )

                return response_object
            else:
                response_object = {
                    'status': 'error',
                    'message': 'A seller with the this email address already exists. Try logging in instead.'.format(public_id)
                }
                return response_object




 @staticmethod
    def follow(seller: Seller, client_public_id: str) -> Seller:
        client = SellerService.get_by_id(client_public_id)
        if client.tax_auditor_company == seller.company_name:
            seller.follow(client)
            db.session.commit()
            return seller
        else:
            response_object = {
                'status': 'error',
                'message': 'You are not authorized to follow this seller.'
            }
            return response_object

    @staticmethod
    def unfollow(seller: Seller, client_public_id: str) -> Seller:
        client = SellerService.get_by_id(client_public_id)
        seller.unfollow(client)
        db.session.commit()
        return seller
