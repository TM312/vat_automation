from current_app.config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, COMPANY_NAME

import logging
from logging.handlers import SMTPHandler

credentials = (MAIL_USERNAME, MAIL_PASSWORD)
mail_handler = SMTPHandler(
	mailhost=(MAIL_SERVER, MAIL_PORT),
	fromaddr='no-reply@' + MAIL_SERVER,
	toaddrs=ADMINS,
	subject=COMPANY_NAME + ' failure',
	credentials=credentials
)
mail_handler.setLevel(logging.ERROR)

if not app.debug:
	app.logger.addHandler(mail_handler)
