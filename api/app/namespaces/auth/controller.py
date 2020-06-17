from typing import List

from flask import request
from flask import current_app

from flask_restx import Namespace, Resource

from . import Token
from . import auth_dto
from .service import TokenService
from .interface import TokenInterface

from ..user.interface_parent import UserInterface
from ..user import user_dto
from ..utils.decorators import login_required, accepted_u_types

ns = Namespace("Auth", description="Token Related Operations")  # noqa
ns.add_model(auth_dto.name, auth_dto)


@ns.route("/")
class AdminTokenResource(Resource):
    """Get all tokens"""
    #@login_required
    #@accepted_u_types('admin')
    @ns.marshal_list_with(auth_dto)
    def get(self) -> List[Token]:
        """List Of Registered Tokens"""
        return TokenService.get_all()

@ns.route("/<string:auth_token>")
class AdminTokenIdResource(Resource):
    #@login_required
    #@accepted_u_types('admin')
    @ns.marshal_with(auth_dto)
    def get(self, auth_token: TokenInterface) -> Token:
        """Get One Token"""
        return TokenService.get_by_id(auth_token)


@ns.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    @ns.expect(user_dto, validate=True)
    #@ns.header('Authorization',  description='Auth Token')
    def post(self):
        """ Login User """
        user_data: UserInterface = request.json
        print(user_data, flush=True)
        return TokenService.login_user(user_data)


@ns.route('/logout')
class UserLogout(Resource):
    """
    User Logout Resource
    """
    @login_required
    def post(self):
        # get auth token from request header
        auth_token: TokenInterface = request.headers.get('Authorization')
        return TokenService.logout_user(auth_token)
