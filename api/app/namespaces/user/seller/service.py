from uuid import UUID
from typing import List

from werkzeug.exceptions import Conflict, NotFound, Unauthorized

from app.extensions import db
from .model import Seller
from .interface import SellerInterface


from ...email.service import EmailService


class SellerService:
    @staticmethod
    def create(seller_data: SellerInterface) -> Seller:
        seller = Seller.query.filter_by(email=seller_data.get('email')).first()
        if not seller:
            #create new seller based on Seller model
            new_seller = Seller(
                email=seller_data.get('email'),
                password=seller_data.get('password'),
                role='employee'
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
                'message': 'A seller with the this email address already exists. Try logging in instead.'
            }
            return response_object



    @staticmethod
    def update(seller: Seller, data_changes) -> Seller:
        seller.update(data_changes)
        seller.update_last_seen()
        db.session.commit()
        return seller


    @staticmethod
    def delete_by_id(public_id: UUID):
        #check if seller exists in db
        seller = Seller.query.filter(Seller.public_id == public_id).first()
        if seller:
            db.session.delete(seller)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Seller (Public ID: {}) has been successfully deleted.'.format(str(public_id))
            }
            return response_object
        else:
            raise NotFound('This seller does not exist.')
