__author__ = 'chenfeiyu'
from scrapy import signals
import logging
from ...api_1_0.errors import timeout, not_found
from ...common.exceptions import RequestTimeoutError, NotFoundError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError


class OutputPiplines(object):
    results = []

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        # crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def process_item(self, item, spider):
        self.results.append(dict(item))
        return item

    def spider_closed(self, spider):
        # this result will be output to spider_manager thread
        return self.results

