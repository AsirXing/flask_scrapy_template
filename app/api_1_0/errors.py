__author__ = 'chenfeiyu'

from flask import jsonify, Response
import logging
from app.common.exceptions import ValidationError, HttpError, ProcessingError, RequestTimeoutError, NotFoundError, DBError, ForbiddenError
from ..common.utils import Utils
from ..common.constants import Constants
from . import api
from .. import db


def generate_error(errorType, message, statusCode, root_tag):
    error_xml = Utils.dict_to_xml({'Error':{'Type':errorType, 'Message':message, 'StatusCode': statusCode}}, root_tag)
    return Response(error_xml, mimetype=Constants.MINETYPE_TEXT_XML)

def bad_request(message, root_tag):
    return generate_error(Constants.ERROR_TYPE_BAD_REQUEST, message, Constants.HTTP_CODE_403, root_tag)


def unauthorized(message, root_tag):
    return generate_error(Constants.ERROR_TYPE_UNAUTHORIZED, message, Constants.HTTP_CODE_401, root_tag)


def forbidden(message, root_tag):
    return generate_error(Constants.ERROR_TYPE_FORBIDDEN, message, Constants.HTTP_CODE_403, root_tag)


def not_found(message, root_tag):
    return generate_error(Constants.ERROR_TYPE_NOT_FOUND, message, Constants.HTTP_CODE_404, root_tag)


def timeout(message, root_tag):
    return generate_error(Constants.ERROR_TYPE_TIMEOUT, message, Constants.HTTP_CODE_408, root_tag)

def internal_error(message, root_tag):
    return generate_error(Constants.ERROR_TYPE_PROCESSING, message, Constants.HTTP_CODE_500, root_tag)

def http(message, root_tag):
    return generate_error(Constants.ERROR_TYPE_HTTP, message, Constants.HTTP_CODE_404, root_tag)


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0], e.root_tag)


@api.errorhandler(ProcessingError)
def processing_error(e):
    return internal_error(e.args[0], e.root_tag)


@api.errorhandler(RequestTimeoutError)
def timeout_error(e):
    return timeout(e.args[0], e.root_tag)


@api.errorhandler(NotFoundError)
def not_found_error(e):
    return not_found(e.args[0], e.root_tag)


@api.errorhandler(HttpError)
def http_error(e):
    return http(e.args[0], e.root_tag)


@api.errorhandler(DBError)
def db_error(e):
    logging.exception(e)
    return internal_error(str(e), e.root_tag)


@api.errorhandler(ForbiddenError)
def forbidden_error(e):
    return forbidden(e.args[0], e.root_tag)