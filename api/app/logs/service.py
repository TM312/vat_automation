from flask import current_app
import os
from datetime import date

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from ..config import basedir






class LogService:

    @staticmethod
    def setup_logging(app):
        MAIL_USERNAME = current_app.config.MAIL_USERNAME
        MAIL_PASSWORD = current_app.config.MAIL_PASSWORD
        MAIL_SERVER = current_app.config.MAIL_SERVER
        MAIL_PORT = current_app.config.MAIL_PORT
        COMPANY_NAME = current_app.config.COMPANY_NAME
        ADMINS = current_app.config.ADMINS
        MAIL_USE_TLS = current_app.config.MAIL_USE_TLS
        BASE_PATH_LOGS = current_app.config.BASE_PATH_LOGS

        today_as_str = date.today().strftime('%Y%m%d')
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
        secure = None
        if MAIL_USE_TLS:
            secure = ()

        mail_handler = SMTPHandler(
            mailhost=(MAIL_SERVER, MAIL_PORT),
            fromaddr='no-reply@' + MAIL_SERVER,
            toaddrs=ADMINS,
            subject=COMPANY_NAME + ' failure',
            credentials=credentials
        )
        mail_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.INFO)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Server startup')

        if not os.path.exists('logs'):
            os.mkdir('logs')
            file_handler = RotatingFileHandler('{}/{}_errors.log'.format(BASE_PATH_LOGS, today_as_str), maxBytes=10240, backupCount=10)

            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))


        if not app.debug:
            app.logger.addHandler(mail_handler)
            app.logger.addHandler(file_handler)
