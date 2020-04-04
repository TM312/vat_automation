from threading import Thread
from datetime import datetime

from flask_mail import Message
from flask import current_app, render_template
from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous import SignatureExpired, BadTimeSignature
from werkzeug.exceptions import Conflict, Gone, BadRequest

from app.extensions import mail
from app.extensions import db
from ..user.service import UserService


from ..utils.decorators.asyncd import asyncd


class EmailService:

    @asyncd  # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support
    def send_async_email(app, msg):
        with app.app_context():
            mail.send(msg)


    def send_email(subject, recipients, template, **kwargs):
        app = current_app._get_current_object()

        msg = Message(
            subject=subject,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=recipients
        )
        msg.html = render_template(template, **kwargs)

        EmailService.send_async_email(app, msg)

    def generate_confirmation_url(user_email):
        confirm_serializer = URLSafeTimedSerializer(secret_key=current_app.config['SECRET_KEY'])
        token=confirm_serializer.dumps(
            obj=user_email,
            salt=current_app.config['EMAIL_CONFIRMATION_SALT']
        )  # Returns a signed string serialized with the internal serializer.


        confirmation_link = '{}/confirm/{}'.format(
            current_app.config['FRONTEND_HOST'],
            token
            )

        return confirmation_link


    def confirm_email(token):
        confirm_serializer = URLSafeTimedSerializer(
            secret_key=current_app.config['SECRET_KEY']
        )
        try:
            salt = current_app.config['EMAIL_CONFIRMATION_SALT']
            max_age = current_app.config['EMAIL_CONFIRMATION_MAX_AGE']

            email = confirm_serializer.loads(
                token,
                salt = salt,
                max_age = max_age
            )

        except SignatureExpired:
            raise Gone('The token is expired.')

        except BadTimeSignature:
            raise BadRequest('Bad Signature.')

        user = UserService.get_by_email(email)

        if user.confirmed:
            raise Conflict('User already confirmed.')
        else:
            user.confirmed = True
            user.confirmed_on = datetime.utcnow()
            db.session.add(user)
            db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'The user email (Public ID: {}) has been confirmed.'.format(user.public_id)
        }
        return response_object
