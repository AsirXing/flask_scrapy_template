__author__ = 'chenfeiyu'
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    USER_NAME = os.environ.get('USER_NAME') or 'username'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_RECYCLE = 45

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or None
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or None
    MAIL_SUBJECT_PREFIX = '[Flask Scrapy Template]'
    MAIL_SENDER = 'flask_scrapy_template@yourdomain.com'
    MAIL_CARTELL_SUPPORT = os.environ.get('MAIL_CARTELL_SUPPORT') or 'username@yourdomain.com'
    SYSTEM_ADMIN = os.environ.get('SYSTEM_ADMIN')
    MAIL_USE_SSL = False

    SQLALCHEMY_POOL_SIZE = 0

    DATABASE_URL_LOCAL = 'mysql+pymysql://username:password@localhost/flask_scrapy_template'

    @staticmethod
    def init_app(app):
        pass


# mysql+pymysql://username:password@url/database
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or Config.DATABASE_URL_LOCAL


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or Config.DATABASE_URL_LOCAL


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
