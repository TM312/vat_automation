from typing import List

from flask import request, g
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource


from app.extensions import mail
from .schema import user_dto
from .service import UserService
from .model import User
from .interface import UserInterface
from ..auth.interface import TokenInterface
from ..utils.decorators.auth import login_required, accepted_roles, confirmation_required
from ..email.service import EmailService




ns = Namespace("User", description="User Related Operations")  # noqa
ns.add_model(user_dto.name, user_dto)


@ns.route("/")
class AdminUserListResource(Resource):
    """Get all Users"""
    @login_required
    @accepted_roles('admin')
    #@confirmation_required
    @ns.marshal_list_with(user_dto, envelope='data')
    def get(self) -> List[User]:
        """List Of Registered Users"""
        return UserService.get_all()


@ns.route("/<string:public_id>")
@ns.param("public_id", "Public user ID")
class AdminUserIdResource(Resource):
    @login_required
    @accepted_roles('admin')
    @ns.marshal_with(user_dto)
    def get(self, public_id: str) -> User:
        """Get One User"""
        return UserService.get_by_id(public_id)

    @login_required
    @accepted_roles('admin')
    def delete(self, public_id: str) -> Response:
        """Delete A Single User"""
        return UserService.delete_by_id(public_id)

    @login_required
    @accepted_roles('admin')
    @ns.expect(user_dto, validate=True)
    @ns.marshal_with(user_dto)
    def put(self, public_id: str) -> User:
        """Update A User's Details"""
        data_changes: UserInterface = request.json  # JSON body of a request
        user = UserService.get_by_id(public_id)
        return UserService.update(user, data_changes)


@ns.route("/self")
class UserResource(Resource):
    # @ns.param("public_id", "Public user ID")
    @login_required
    @ns.marshal_with(user_dto, envelope='data')
    def get(self) -> User:
        """ Current User User """
        return g.user

    @ns.expect(user_dto, validate=True)
    def post(self):
        """Create A Single User"""
        user_data: UserInterface = request.json
        new_user = UserService.create_user(user_data)

        """ Send Confirmation Email to user email """
        confirmation_link = EmailService.generate_confirmation_url(new_user.email)
        print(confirmation_link)
        EmailService.send_email(
            subject='Registration',
            recipients = [new_user.email],
            template='email_confirmation.html',
            confirmation_link=confirmation_link,
        )

        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201

    @login_required
    def delete(self) -> Response:
        """Delete self"""
        return UserService.delete_by_id(g.user.public_id)

    @login_required
    @ns.expect(user_dto, validate=True)
    @ns.marshal_with(user_dto)
    def put(self) -> User:
        """Update self"""
        data_changes: UserInterface = request.json  # JSON body of a request
        user = g.user
        return UserService.update(user, data_changes)
