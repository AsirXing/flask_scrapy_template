__author__ = 'chenfeiyu'
import logging, os
from ..spiders.spider_robot.spiders.test_spider import TestSpider

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor, defer
from ..common.constants import Constants
from ..common.utils import Utils
from ..common.exceptions import RequestTimeoutError, NotFoundError, ValidationError
from multiprocessing import Process
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from ..models.spider_configure import SpiderConfigure


class SpiderManager(Process):
    items = []
    result_queue = None
    spiders = []

    def __init__(self, params, spider_name, result_queue):
        self.__init__(params, result_queue)
        self.spiders = []
        self.add_spider(spider_name)

    def __init__(self, params, result_queue):
        Process.__init__(self)
        self.params = params
        self.result_queue = result_queue
        self.spiders = []
        dispatcher.connect(self._item_passed, signals.item_passed)

    def add_spider(self, spider_name):
        #  TODO put other spider here
        if spider_name == Constants.SPIDER_NAME_TEST_SPIDER:
            self.spiders.append(TestSpider)

    def _item_passed(self, item):
        self.items.append(item) # the script will block here until the crawling is finished

    def run(self):
        # set custom settings here if you want
        # e.g self.spider.custom_settings={'RETRY_TIMES':10}
        logging.info('Spider thread is running. Calling spiders: %s ' % self.spiders)
        if not self.spiders:
            raise ValidationError('Missing spiders')

        # crawler = CrawlerProcess(get_project_settings())
        settings = Settings()
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'app.spiders.spider_robot.settings'
        settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        settings.setmodule(settings_module_path, priority='project')
        crawler = CrawlerRunner(settings)
        live_spider_names = SpiderConfigure.get_all_live_spider_names()
        is_crawl = False
        logging.info(live_spider_names)
        for spider in self.spiders:
            if spider.name in live_spider_names:
                is_crawl = True
                crawler.crawl(spider, params=self.params)

        if is_crawl:
            d = crawler.join()
            d.addBoth(lambda _: reactor.stop())
            reactor.run() # The script will block here until all crawlers are finished
        else:
            logging.warn('No live spider found')

        self.result_queue.put(self.items)

