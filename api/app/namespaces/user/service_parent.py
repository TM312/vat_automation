import datetime
import uuid
from typing import List

from werkzeug.exceptions import Conflict, NotFound, Unauthorized

from app.extensions import db
from .model import User
from .schema import user_dto

from ..email.service import EmailService
from ..auth.service import TokenService



class UserService:
    @staticmethod
    def get_all() -> List[User]:
        users = User.query.all()
        return users

    @staticmethod
    def get_by_id(public_id: str) -> User:
        user = User.query.filter(User.public_id == public_id).first()
        if user:
            return user
        else:
            raise NotFound('This user does not exist.')

    @staticmethod
    def get_by_email(email: str) -> User:
        user = User.query.filter(User.email == email).first()
        if user:
            return user
        else:
            raise NotFound('This user does not exist.')


    @staticmethod
    def ping(user: User) -> User:
        user.last_seen()
        db.session.commit()
        return user


    @staticmethod
    def delete_by_id(public_id: str):
        #check if user exists in db
        user = User.query.filter(User.public_id == public_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'User (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This user does not exist.')
