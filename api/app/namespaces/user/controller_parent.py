from typing import List
from uuid import UUID
from flask import request, g, current_app

from flask.wrappers import Response
from flask_restx import Namespace, Resource

from . import User, Action
from . import user_dto, user_dto_admin, user_sub_dto, action_dto
from .service_parent import UserService

from ..utils.decorators import login_required, accepted_u_types, confirmation_required


ns = Namespace("User", description="User Related Operations")  # noqa
ns.add_model(user_sub_dto.name, user_sub_dto)
ns.add_model(user_dto.name, user_dto)
ns.add_model(user_dto_admin.name, user_dto_admin)
ns.add_model(action_dto.name, action_dto)

# https://flask-restx.readthedocs.io/en/latest/api.html#flask_restx.Model
# https://github.com/python-restx/flask-restx/blob/014eb9591e61cd3adbbd29a38b76df6a688f067b/flask_restx/namespace.py


@ns.route("/")
class AdminUserListResource(Resource):
    """Get all Users"""
    @ns.marshal_list_with(user_dto_admin, envelope='data')
    def get(self) -> List[User]:
        """List Of Registered Users"""
        return UserService.get_all()


@ns.route("/actions")
class AdminUserActionsResource(Resource):
    """Get all User Actions"""
    #@login_required
    #@accepted_u_types('admin')
    @ns.marshal_list_with(action_dto, envelope='data')
    def get(self) -> List[Action]:
        """List of user actions"""
        return UserService.get_all_actions()


@ns.route("/<string:public_id>")
@ns.param("public_id", "Public user ID")
class AdminUserIdResource(Resource):
    #@login_required
    #@accepted_u_types('admin')
    @ns.marshal_with(user_dto_admin, envelope='data')
    def get(self, public_id: str) -> User:
        """Get One User"""
        return UserService.get_by_public_id(UUID(public_id))

    #@login_required
    #@accepted_u_types('admin')
    def delete(self, public_id: str) -> Response:
        """Delete A Single User"""
        return UserService.delete_by_public_id(UUID(public_id))


@ns.route("/self")
class UserSelfResource(Resource):
    @login_required
    #@accepted_u_types('admin')
    @ns.marshal_with(user_dto)
    def get(self, envelope='data') -> User:
        """Get One User"""
        return UserService.get_by_id(g.user.id)
