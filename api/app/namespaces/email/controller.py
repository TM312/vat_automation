from flask import request, g, current_app

from flask_restx import Namespace, Resource

from .service import EmailService
from .interface import EmailInterface

from app.namespaces.utils.decorators import login_required

ns = Namespace("email", description="Email Related Operations")  # noqa
#ns.add_model(email.name, email)


@ns.route("/request_confirm")
class UserEmailConfirmationResource(Resource):
    @login_required
    def get(self):
        """ Request email confirmation for current user """
        user = g.user
        confirmation_link = EmailService.generate_confirmation_url(user.email)
        EmailService.send_email(
            subject='Registration',
            recipients=[user.email],
            template='email_confirmation.html',
            confirmation_link=confirmation_link,
        )


@ns.route('/confirm')
class EmailConfirmationResource(Resource):
    """POST Request for email confirmation token state"""
    def post(self):
        token : EmailInterface = request.json['token']  # JSON body of a request
        return EmailService.confirm_email(token)
