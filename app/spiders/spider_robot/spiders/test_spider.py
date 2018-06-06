__author__ = 'chenfeiyu'
import logging
from scrapy.http import FormRequest
from ..items import TestItem
from scrapy.selector import Selector
from scrapy.http import Request
from ....common.constants import Constants
from ....common.utils import Utils
from .common_spider import CommonSpider
from ....common.exceptions import ForbiddenError


class TestSpider(CommonSpider):
    # spider name call by crawler

    name = Constants.SPIDER_NAME_TEST_SPIDER
    domain = "testdomain.com"
    url = "https://www.testdomain.com/"
    allowed_domains = [domain]
    key = ''

    def __init__(self, params):
        CommonSpider.__init__(self)
        # when it comes to here, it must have one key
        self.key = params['key']

    def start_requests(self):
        yield Request(self.url,
                      callback=self.parse,
                      errback=self.errback_httpbin,
                      dont_filter=True)

    def parse(self, response):
        sel = Selector(response)
        logging.info("Visited %s" % response.url)
        test_item = TestItem()
        test_item[Constants.XML_ROOT_SPIDER_NAME] = self.name
        try:
            # scrape data here
            logging.info("Start scraping %s" % response.url)

        except Exception as e:
            logging.exception(e)
            self.send_no_response_email()
            error = self.get_error_item(
                    Constants.ERROR_TYPE_PROCESSING,
                    'Parsing original data failed.',
                    Constants.HTTP_CODE_500
                )
            test_item[Constants.XML_ROOT_ERROR] = error
        return test_item