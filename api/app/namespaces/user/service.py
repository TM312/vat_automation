import datetime
import uuid
from typing import List

from werkzeug.exceptions import Conflict, NotFound, Unauthorized

from app.extensions import db
from .model import User
from .schema import user_dto



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
    def update(user: User, data_changes) -> User:
        user.update(data_changes)
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

    def create_user(user_data) -> User:
        #check if user already exists in db
        user = User.query.filter_by(email = user_data.get('email')).first()
        if not user:
            #create new user based on User model
            new_user = User(
                email=user_data.get('email'),
                password=user_data.get('password')
            )
            #add user to db
            db.session.add(new_user)
            db.session.commit()

            return new_user
        else:
            raise Conflict('A user with this email adress already exists.')

     # def ping(self):
    #     self.last_seen = datetime.utcnow()
    #     db.session.add(self)

    def generate_token(public_id: str, token_lifespan):  # : TokenInterface) -> Token:
        try:
            auth_token = User.encode_auth_token(public_id, token_lifespan)
            auth_token_decoded = auth_token.decode()
            return auth_token_decoded
        except:
            raise Unauthorized('Some error occurred during authorization.')
