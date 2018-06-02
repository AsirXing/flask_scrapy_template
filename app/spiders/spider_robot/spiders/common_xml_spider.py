__author__ = 'chenfeiyu'
import logging
from scrapy.spiders import XMLFeedSpider
from ....common.constants import Constants
from ..items import ErrorItem

class CommonXMLSpider(XMLFeedSpider):
    vin = ''
    name = ''
    url = ''
    make = ''
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value

    def __init__(self, vin, *args, **kwargs):
        logging.info("Spider " + self.name + " is calling")
        XMLFeedSpider.__init__(self).__init__(*args, **kwargs)
        self.vin = vin

    def convert_original_to_standard(self, final_item):
        pass

    def get_error_item(self, error_type, message, status_code):
        error = ErrorItem()
        error[Constants.XML_ERROR_TYPE] = error_type
        error[Constants.XML_ERROR_MESSAGE] = message
        error[Constants.XML_ERROR_STATUS_CODE] = status_code
        return dict(error)