from typing import List, Union, Dict
import jwt
from datetime import datetime, timedelta
import inspect

from flask import current_app, g
from werkzeug.exceptions import InternalServerError, NotFound, Unauthorized

from app.extensions import db
from . import Token
from .interface import TokenInterface

from ..user import User
from ..user.service_parent import UserService
from ..user.interface_parent import UserInterface


class TokenService:
    @staticmethod
    def get_all() -> List[Token]:
        auth_tokens = Token.query.all()
        return auth_tokens

    @staticmethod
    def get_by_id(auth_token: TokenInterface) -> Token:
        auth_token = Token.query.filter(Token.auth_token == auth_token).first()
        if auth_token:
            return auth_token, 200
        else:
            raise NotFound('Token does not exist.')


    @staticmethod
    def login_user(user_data: UserInterface) -> Dict:
        # fetch the user data
        user = UserService.get_by_email(user_data.get('email'))
        if user and user.check_password(user_data.get('password')):
            token_lifespan = current_app.config["TOKEN_LIFESPAN_REGISTRATION"]
            auth_token = TokenService.encode_auth_token(public_id=str(user.public_id), token_lifespan=token_lifespan)
            if auth_token:
                # UserService.ping(user, method_name=inspect.stack()[0][3], service_context=TokenService.__name__)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'token' : auth_token.decode()
                }
                return response_object
        else:
            raise Unauthorized('Invalid Email or Password.')

    @staticmethod
    def current_user(auth_token: TokenInterface) -> User:
        payload = TokenService.decode_auth_token(auth_token)
        if not isinstance(payload, str):
            user = UserService.get_by_public_id(payload['sub'])
            if user:
                return user
            else:
                raise NotFound('This user does not exist.')
        raise Unauthorized(payload)  # ('Provide a valid auth token.')

    @staticmethod
    def logout_user(auth_token: TokenInterface) -> Dict:
        # update a user's last_seen attribute & creates a new action object
        # the inspect module needs to be imported whenever ping is called

        user = g.user

        # UserService.ping(user, method_name=inspect.stack()[0][3], service_context=TokenService.__name__)

        # actual logout
        payload = TokenService.decode_auth_token(auth_token)
        if isinstance(payload, dict):
            # mark the token as blacklisted
            blacklisted_token = Token(
                auth_token = auth_token,
                iat = datetime.fromtimestamp(payload['iat'] / 1e3),
                sub = payload['sub']
            )
            db.session.add(blacklisted_token)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            return response_object

        else:
            raise Unauthorized(payload)

    @staticmethod
    def encode_auth_token(public_id: str, token_lifespan: int) -> str:
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'iss': current_app.config["COMPANY_NAME"].lower(),
                'exp': datetime.utcnow() + timedelta(minutes=token_lifespan),
                'iat': datetime.utcnow(),
                'sub': public_id
            }
            auth_token = jwt.encode(
                payload,
                current_app.config["SECRET_KEY"],
                algorithm='HS256'
            )
            return auth_token

        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: TokenInterface) -> Dict:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            key = current_app.config["SECRET_KEY"]
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = TokenService.check_blacklisted(auth_token)
            if is_blacklisted_token:
                return 'Token is blacklisted. Please log in again.'
            else:
                return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def check_blacklisted(auth_token: TokenInterface) -> bool:
        # check whether auth token has been blacklisted
        return db.session.query(Token.query.filter_by(auth_token=str(auth_token)).exists()).scalar()
