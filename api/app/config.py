import os
from typing import List, Type

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4
    COMPANY_NAME = 'NTAMAZON'
    TOKEN_LIFESPAN_LOGIN = 420 #in minutes
    TOKEN_LIFESPAN_REGISTRATION = 360  # in minutes
    FRONTEND_HOST = os.getenv('SERVER_ADDRESS')  #domain is put here for production

    # mail server settings
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    EMAIL_CONFIRMATION_SALT = os.getenv('EMAIL_CONFIRMATION_SALT')
    EMAIL_CONFIRMATION_MAX_AGE = 10#3600 #in seconds

    # administrator list
    ADMINS = ['thomas.moellers@unisg.ch']

#environments
class Development(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI_DEV') #structure: dialect+driver://username:password@host:port/database
    SECRET_KEY = os.getenv('SECRET_KEY_DEV')


class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI_TEST')
    SECRET_KEY = os.getenv('SECRET_KEY_TEST')
    BCRYPT_LOG_ROUNDS = 4
    CSRF_ENABLED = False # only for testing!!!


class Staging(Config):
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI_STAGE')
    SECRET_KEY = os.getenv('SECRET_KEY_STAGE')


class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI_PROD')
    SECRET_KEY = os.getenv('SECRET_KEY_PROD')


app_config = dict(
    dev=Development,
    stage=Staging,
    test=Testing,
    prod=Production
)
