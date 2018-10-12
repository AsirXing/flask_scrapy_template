__author__ = 'chenfeiyu'
import logging, random
from ...api_1_0.errors import timeout, not_found
from ...common.exceptions import RequestTimeoutError, NotFoundError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from scrapy import signals

# This middleware is not used currently, but leave it as a example
class CustomDownloaderMiddleware(object):

    def process_exception(self, request, exception, spider):
        # logging.error(repr(exception))

        if isinstance(exception, HttpError):
        # if exception.check(HttpError):
            # you can get the response
            raise NotFoundError('HttpError on %s : %s', (request.url, exception))

        elif isinstance(exception, DNSLookupError):
        # elif exception.check(DNSLookupError):
            # this is the original request
            raise NotFoundError('DNSLookupError on %s : %s', (request.url, exception))

        elif isinstance(exception, TimeoutError):
        # elif exception.check(TimeoutError):
            raise RequestTimeoutError('TimeoutError on %s : %s', (request.url, exception))

        return None


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        # 30% useragent change
        if random.choice(range(1, 100)) <= 30:
            user_agent = random.choice(self.agents)
            logging.info("changing random user agent: " + user_agent)
            request.headers.setdefault('User-Agent', user_agent)

