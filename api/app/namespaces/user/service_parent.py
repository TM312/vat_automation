import datetime
from uuid import UUID
from typing import List

from werkzeug.exceptions import Conflict, NotFound

from app.extensions import db
from . import User, Action


class UserService:
    @staticmethod
    def get_all() -> List[User]:
        users = User.query.all()
        return users

    @staticmethod
    def get_by_public_id(public_id: UUID) -> User:
        user = User.query.filter(User.public_id == public_id).first()
        if user:
            return user
        else:
            raise NotFound('This user does not exist.')


    @staticmethod
    def get_by_id(id: int) -> User:
        user = User.query.filter(User.id == id).first()
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
    def ping(user: User, method_name: str, service_context: str) -> User:
        user.update_last_seen()

        new_action = Action(
            method_name=method_name,
            service_context=service_context,
            user_id=user.id)

        #add action to db and commit user changes
        db.session.add(new_action)
        db.session.commit()
        return user


    @staticmethod
    def delete_by_public_id(public_id: UUID):
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
