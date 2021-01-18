from uuid import UUID
from typing import List

from flask import current_app

from werkzeug.exceptions import Conflict, NotFound, Unauthorized, BadRequest, InternalServerError

from app.extensions import db
from .model import Seller
from .interface import SellerInterface


from app.namespaces.email.service import EmailService


class SellerService:

    @staticmethod
    def get_by_id(seller_id: int) -> Seller:
        return Seller.query.filter_by(id=seller_id).first()

    @staticmethod
    def get_by_public_id(seller_public_id: str) -> Seller:
        return Seller.query.filter_by(public_id=seller_public_id).first()

    @staticmethod
    def get_by_email(seller_email: str) -> Seller:
        return Seller.query.filter_by(email=seller_email).first()



    @staticmethod
    def create(seller_data: SellerInterface) -> Seller:
        new_seller = Seller(
            name=seller_data.get('name'),
            email=str(seller_data.get('email')),
            password=str(seller_data.get('password')),
            role=str(seller_data.get('role')),
            employer_id = seller_data.get('employer_id')
        )
        #add seller to db
        db.session.add(new_seller)
        try:
            db.session.commit()
        except Exception as e:
            raise InternalServerError(e)

        return new_seller





    @staticmethod
    def update(seller: Seller, data_changes) -> Seller:
        seller.update(data_changes)
        seller.update_last_seen()
        db.session.commit()
        return seller


    @staticmethod
    def delete_by_public_id(seller_public_id: str):
        #check if seller exists in db
        seller = SellerService.get_by_public_id(seller_public_id)
        if seller:
            db.session.delete(seller)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Seller (Public ID: {}) has been successfully deleted.'.format(str(seller_public_id))
            }
            return response_object
        else:
            raise NotFound('This seller does not exist.')

    @staticmethod
    def register_seller(seller_data: SellerInterface) -> Seller:
        print('enter register_seller', flush=True)
        email = str(seller_data.get('email'))
        password = str(seller_data.get('password'))
        name = str(seller_data.get('name'))

        if not isinstance(seller_data.get('email'), str) or not isinstance(seller_data.get('password'), str) or not isinstance(seller_data.get('name'), str):
            raise BadRequest('The provided data is invalid.')

        if isinstance(seller_data.get('employer_public_id'), str):
            from app.namespaces.business.seller_firm.service import SellerFirmService
            employer_id = SellerFirmService.get_seller_firm_id(seller_firm_public_id = seller_data.get('employer_public_id', str))

            if isinstance(employer_id, int):
                seller_data['employer_id'] = employer_id

        seller = SellerService.get_by_email(email)
        if not isinstance(seller, Seller):
            try:
                new_seller = SellerService.create(seller_data)
            except Exception as e:
                current_app.logger.warning(e)
                raise e

            if isinstance(new_seller, Seller):

                # """ Send Confirmation Email to seller email """
                # confirmation_link = EmailService.generate_confirmation_url(new_seller.email)
                # print(confirmation_link)
                # EmailService.send_email(
                #     subject='Registration',
                #     recipients = [new_seller.email],
                #     template='email_confirmation.html',
                #     confirmation_link=confirmation_link,
                # )
                return new_seller
            else:
                current_app.logger.info('Seller can not be found in database.')
                raise InternalServerError('Oops, something went wrong.')

        else:
            raise Conflict('A seller with the this email address already exists. Try logging in instead.')
