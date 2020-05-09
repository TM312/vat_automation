from typing import List
import jwt
from datetime import datetime, timedelta
import inspect

from flask import current_app
from werkzeug.exceptions import InternalServerError, NotFound, Unauthorized

from app.extensions import db
from .model import Token
from .interface import TokenInterface

from ..user.model_parent import User
from ..user.service_parent import UserService

COMPANY_NAME = current_app.config["COMPANY_NAME"]
SECRET_KEY = current_app.config["SECRET_KEY"]


class TokenService:
    @staticmethod
    def get_all() -> List[Token]:
        tokens = Token.query.all()
        return tokens

    @staticmethod
    def get_by_id(auth_token: TokenInterface) -> Token:
        token = Token.query.filter(Token.token == auth_token).first()
        if token:
            return token, 200
        else:
            raise NotFound('Token does not exist.')


    @staticmethod
    def login_user(user_data, token_lifespan):
        # fetch the user data
        user = User.query.filter_by(email=user_data.get('email')).first()
        if user and user.check_password(user_data.get('password')):
            auth_token = TokenService.encode_auth_token(
                public_id=str(user.public_id), token_lifespan=token_lifespan)
            if auth_token:
                UserService.ping(user, method_name=inspect.stack()[0][3],
                                 service_context=TokenService.__name__)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'token' : auth_token.decode()
                }
                return response_object
        else:
            raise Unauthorized('Invalid Email or Password.')

    @staticmethod
    def current_user(auth_token):
            payload = TokenService.decode_auth_token(auth_token)
            if not isinstance(payload, str):
                user = User.query.filter(User.public_id == payload['sub']).first()
                if user:
                    return user
                else:
                    raise NotFound('This user does not exist.')
            raise Unauthorized(payload)  # ('Provide a valid auth token.')

    @staticmethod
    def logout_user(user, auth_token):
        # update a user's last_seen attribute & creates a new action object
        # the inspect module needs to be imported whenever ping is called
        UserService.ping(user, method_name=inspect.stack()[0][3],
                         service_context=TokenService.__name__)

        # actual logout
        payload = TokenService.decode_auth_token(auth_token)
        if isinstance(payload, dict):
            # mark the token as blacklisted
            blacklisted_token = Token(
                token = auth_token,
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
    def encode_auth_token(public_id: str, token_lifespan: int):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'iss': COMPANY_NAME.lower(),
                'exp': datetime.utcnow() + timedelta(minutes=token_lifespan),
                'iat': datetime.utcnow(),
                'sub': public_id
            }
            auth_token = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
            return auth_token

        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            key = SECRET_KEY
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
    def check_blacklisted(auth_token):
        # check whether auth token has been blacklisted
        res = Token.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
