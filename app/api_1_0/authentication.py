__author__ = 'chenfeiyu'
from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from . import api
from .errors import unauthorized, forbidden
from ..common.utils import Utils
from ..common.constants import Constants
from config import Config

auth = HTTPBasicAuth()


# This is a callback method of HTTPBasicAuth
@auth.verify_password
def verify_password(username, password):
    if Utils.is_empty(username) or Utils.is_empty(password):
        return False

    if username == Config.USER_NAME and password == Config.SECRET_KEY:
        g.current_user = Config.USER_NAME
        return True
    else:
        return False


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials', Constants.XML_ROOT_FLASK_SCRAPY)


# This will affect the whole blue print
@api.before_request
@auth.login_required
def before_request():
    if g.current_user != Config.USER_NAME:
        return forbidden('Unconfirmed account', Constants.XML_ROOT_FLASK_SCRAPY)