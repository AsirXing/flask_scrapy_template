__author__ = 'chenfeiyu'
from .constants import Constants

class CommonError(ValueError):
    def __init__(self, message, root_tag=Constants.XML_ROOT_FLASK_SCRAPY):
        ValueError.__init__(self, message)
        self.root_tag = root_tag

class ValidationError(CommonError):
    pass


class ProcessingError(CommonError):
    pass


class RequestTimeoutError(CommonError):
    pass


class NotFoundError(CommonError):
    pass

class HttpError(CommonError):
    pass

class DBError(CommonError):
    pass

class ForbiddenError(CommonError):
    pass

