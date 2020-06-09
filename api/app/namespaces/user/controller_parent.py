from typing import List
from uuid import UUID
from flask import request, g, current_app

from flask.wrappers import Response

from flask_restx import Namespace, Resource

from .schema_parent import user_dto, user_dto_admin, action_dto
from .service_parent import UserService
from .model_parent import User, Action

from ..utils import login_required, accepted_u_types, confirmation_required


ns = Namespace("User", description="User Related Operations")  # noqa
ns.add_model(user_dto.name, user_dto)
ns.add_model(user_dto_admin.name, user_dto_admin)
ns.add_model(action_dto.name, action_dto)

# https://flask-restx.readthedocs.io/en/latest/api.html#flask_restx.Model
# https://github.com/python-restx/flask-restx/blob/014eb9591e61cd3adbbd29a38b76df6a688f067b/flask_restx/namespace.py


@ns.route("/")
class AdminUserListResource(Resource):
    """Get all Users"""
    @login_required
    @accepted_u_types('admin')
    #@confirmation_required
    @ns.marshal_list_with(user_dto_admin, envelope='data')
    def get(self) -> List[User]:
        """List Of Registered Users"""
        return UserService.get_all()


@ns.route("/actions")
class AdminUserActionsResource(Resource):
    """Get all User Actions"""
    @login_required
    @accepted_u_types('admin')
    @ns.marshal_list_with(action_dto, envelope='data')
    def get(self) -> List[Action]:
        """List of user actions"""
        return UserService.get_all_actions()


@ns.route("/<string:public_id>")
@ns.param("public_id", "Public user ID")
class AdminUserIdResource(Resource):
    @login_required
    @accepted_u_types('admin')
    @ns.marshal_with(user_dto_admin)
    def get(self, public_id: str) -> User:
        """Get One User"""
        return UserService.get_by_public_id(UUID(public_id))

    @login_required
    @accepted_u_types('admin')
    def delete(self, public_id: str) -> Response:
        """Delete A Single User"""
        return UserService.delete_by_public_id(UUID(public_id))


# @ns.route("/<string:public_id>/actions")
# @ns.param("public_id", "Public user ID")
# class AdminUserIdActionsResource(Resource):
#     """Get user's actions"""
#     @login_required
#     @accepted_u_types('admin')
#     @ns.marshal_with(action_dto, envelope='data')
#     def get(self, public_id: UUID) -> Action:
#         """Get One User"""
#         return UserService.get_actions_by_user_public_id(public_id)
