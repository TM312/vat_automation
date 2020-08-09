import os
from datetime import datetime
from typing import List, Type

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 14
    COMPANY_NAME = 'Tax-Automation.com'
    TOKEN_LIFESPAN_LOGIN = 420  # in minutes
    TOKEN_LIFESPAN_REGISTRATION = 360  # in minutes
    # domain is put here for production
    FRONTEND_HOST = os.getenv('SERVER_ADDRESS')

    # mail server settings
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    EMAIL_CONFIRMATION_SALT = os.getenv('EMAIL_CONFIRMATION_SALT')
    EMAIL_CONFIRMATION_MAX_AGE = 3600  # 3600 #in seconds

    # Static Data Paths
    BASE_PATH_SEEDS = '/home/data/seeds'
    BASE_PATH_LOGS = '/home/data/logs'
    BASE_PATH_TEMPLATES = '/home/data/templates'
    BASE_PATH_DATA_SELLER_FIRM = '/home/data/seller_firm_data'
    BASE_PATH_STATIC_DATA_SELLER_FIRM = '/home/data/seller_firm_data/static'
    BASE_PATH_TRANSACTION_DATA_SELLER_FIRM = '/home/data/seller_firm_data/transaction'
    BASE_PATH_TAX_RECORD_DATA_SELLER_FIRM = '/home/data/seller_firm_data/tax_record'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # Media
    # PROFILE_IMAGE_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    MAX_FILE_SIZE_INPUT = 50 * 1024 * 1024  # 50 --> 50MB
    DATA_ALLOWED_EXTENSIONS = ['csv', 'txt']
    STATIC_DATA_ALLOWED_EXTENSIONS = ['csv']
    TRANSACTION_DATA_ALLOWED_EXTENSIONS = ['txt', 'csv']

    STANDARD_SERVICE_TAX_RATE_TYPE = 'S'
    TAX_DEFAULT_VALIDITY = datetime.strptime('31-12-2030', '%d-%m-%Y').date()
    VATIN_LIFESPAN = 32 # in days
    OLD_TRANSACTION_TOLERANCE_DAYS = 100
    SERVICE_START_DATE = datetime.strptime('01-06-2018', '%d-%m-%Y').date()

    SUPPORTED_CURRENCIES = ['GBP', 'CZK', 'PLN'] #besides 'EUR'

    TRANSACTIONS_PER_QUERY = 25

    # administrator list
    ADMINS = ['thomas.moellers@unisg.ch']

# environments


class Development(Config):
    DEBUG = True
    DEVELOPMENT = True
    # structure: dialect+driver://username:password@host:port/database
    #           [DB_TYPE]+[DB_CONNECTOR]: // [USERNAME]: [PASSWORD]@[HOST]: [PORT]/[DB_NAME]
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI_DEV')
    SECRET_KEY = os.getenv('SECRET_KEY_DEV')
    BCRYPT_LOG_ROUNDS = 4


class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI_TEST')
    SECRET_KEY = os.getenv('SECRET_KEY_TEST')
    BCRYPT_LOG_ROUNDS = 4
    CSRF_ENABLED = False  # only for testing config!


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
