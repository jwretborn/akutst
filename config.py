from os import path, environ

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '4\x04O\x8c\xf7koqz\xa0xez\xc4\xa7?.4\xceu\xc4\x8c0\x1b'
    SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WEBPACK_MANIFEST_PATH = path.join(path.abspath(path.dirname(__file__)), "manifest.json")
    WEBPACK_ASSETS_URL = ''

    SECURITY_URL_PREFIX = "/admin"
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = environ["SECURITY_PASSWORD_SALT"]
    SECURITY_EMAIL_SENDER = "no-reply@akutst.se"
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL	= True

    MAIL_SERVER = environ['SMTP_HOST']
    MAIL_PORT = environ['SMTP_PORT']
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ['SMTP_USER']
    MAIL_PASSWORD = environ['SMTP_PASSWORD']
    MAIL_DEFAULT_SENDER = "no-reply@akutst.se"

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
