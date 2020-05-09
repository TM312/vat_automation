from typing import List

from flask import request
from flask import current_app, g

from flask_restx import Namespace, Resource

from .schema import auth_dto
from ..user.schema_parent import user_dto

from .service import TokenService

from .model import Token
from ..user.model_parent import User

from .interface import TokenInterface
from ..user.interface_parent import UserInterface

from ..utils.decorators.auth import login_required, accepted_u_types

TOKEN_LIFESPAN_REGISTRATION = current_app.config["TOKEN_LIFESPAN_REGISTRATION"]

ns = Namespace("Auth", description="Token Related Operations")  # noqa
ns.add_model(auth_dto.name, auth_dto)


@ns.route("/")
class AdminTokenResource(Resource):
    """Get all tokens"""
    @login_required
    @accepted_u_types('admin')
    @ns.marshal_list_with(auth_dto)
    def get(self) -> List[Token]:
        """List Of Registered Tokens"""
        return TokenService.get_all()

@ns.route("/<string:token>")
class AdminTokenIdResource(Resource):
    @login_required
    @accepted_u_types('admin')
    @ns.marshal_with(auth_dto)
    def get(self, token: str) -> Token:
        """Get One Token"""
        return TokenService.get_by_id(token)


@ns.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    @ns.expect(user_dto, validate=True)
    #@ns.header('Authorization',  description='Auth Token')
    def post(self):
        """ Login User """
        # get the post data
        user_data: UserInterface = request.json
        token_lifespan: TokenInterface = TOKEN_LIFESPAN_REGISTRATION
        return TokenService.login_user(user_data, token_lifespan)


@ns.route('/logout')
class UserLogout(Resource):
    """
    User Logout Resource
    """
    @login_required
    def post(self):
        user = g.user
        # get auth token from request header
        auth_token: TokenInterface = request.headers.get('Authorization')
        return TokenService.logout_user(user, auth_token)
