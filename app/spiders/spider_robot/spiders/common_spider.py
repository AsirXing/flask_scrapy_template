__author__ = 'chenfeiyu'
import scrapy, logging
from ....common.exceptions import RequestTimeoutError, NotFoundError, DBError, ProcessingError
from ....common.constants import Constants
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ErrorItem
from app import db
from config import Config
from ....common.email import Email
from ....models.spider_configure import SpiderConfigure


class CommonSpider(scrapy.Spider):
    handle_httpstatus_list = [403]

    url = ''
    name = ''

    def __init__(self):
        scrapy.Spider.__init__(self)

    def convert_original_to_standard(self, final_item):
        pass

    def turn_off_spider_and_send_email(self):
        try:
            if SpiderConfigure.close_spider(self.name):
                Email.send_email(Config.MAIL_CARTELL_SUPPORT,
                                     'System automatically turn off spider',
                                     'mail/spider_off',
                                     spider=self.name,
                                     site_url=self.url)
        except Exception, e:
            logging.exception(e)
            raise ProcessingError('Sending alert email failed')

    def send_no_response_email(self):
        spider_configure = SpiderConfigure.get(self.name)
        try:
            if not spider_configure.email_alert:
                SpiderConfigure.disable_email_alert(self.name)
                Email.send_email(Config.MAIL_CARTELL_SUPPORT,
                             'No response from spider',
                             'mail/spider_no_response',
                             spider=self.name,
                             site_url=self.url)
        except Exception, e:
            logging.exception(e)
            raise ProcessingError('Sending alert email failed')

    def get_error_item(self, error_type, message, status_code):
        error = ErrorItem()
        error[Constants.XML_ERROR_TYPE] = error_type
        error[Constants.XML_ERROR_MESSAGE] = message
        error[Constants.XML_ERROR_STATUS_CODE] = status_code
        return dict(error)

    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        logging.error('errback_httpbin: ' + repr(failure))

        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.send_no_response_email()
            raise NotFoundError('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.send_no_response_email()
            raise NotFoundError('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError):
            request = failure.request
            raise RequestTimeoutError('TimeoutError on %s', request.url)

        else:
            response = failure.value.response
            logging.error('error on ' + response.url)
            logging.error(repr(response))