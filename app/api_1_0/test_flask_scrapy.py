from flask import jsonify, request, current_app, url_for, g, Response
import logging
from . import api
from ..common.utils import Utils
from ..common.constants import Constants
from ..models.flask_scrapy_cache import FlaskScrapyCache
from ..models.flask_scrapy_status import FlaskScrapyStatus
from ..spiders.spider_manager import SpiderManager
from multiprocessing import Queue
from ..common.exceptions import HttpError, NotFoundError


# http --auth username:secret_key GET http://localhost:5002/api/v1.0/test_flask_scrapy key=some_search_key get_latest=True
@api.route('/test_flask_scrapy', methods=['GET'])
def test_flask_scrapy():
    get_latest = Utils.get_latest_flag(request)
    db_only = Utils.db_only_flag(request)

    key = Utils.get_parameter(request, 'key')

    spider_name = Constants.SPIDER_NAME_TEST_SPIDER
    #     searching db
    if not get_latest:
        logging.info('Try to get data from cache...')
        cache_data = FlaskScrapyCache.load_cache(key, spider_name)
        if cache_data:
            logging.info('Found cache from db')
            return Response(cache_data.xml, mimetype=Constants.MINETYPE_TEXT_XML)
        if db_only:
            logging.info('Only check cache, but no cache found, so we stop process here.')
            raise NotFoundError('db_only flag is true, but no cache data found')
        logging.info('No cache found, trying to crawl site...')

    # check failed status to decide continue or not
    status = FlaskScrapyStatus.load_status(key, spider_name)
    if status and not status.can_retry:
        raise NotFoundError('Key is not supported')

    logging.info('Start searching jobs for ' + key)

    result_queue = Queue()
    crawler = SpiderManager({'key':key}, result_queue)
    crawler.add_spider(spider_name)
    crawler.start()
    crawler.join(30)

    # the queue will block here until scrapy get a result back
    error_data = None
    # json data used for actual data table
    json_data = None
    # xml data used for cache
    xml_data = None
    for item in result_queue.get():
        if item:
            if item.get(Constants.XML_ROOT_ERROR):
                # got some error back from spider
                error_data = item
                if item.get(Constants.XML_ROOT_SPIDER_NAME) == spider_name:
                    # this error is come from the correct spider, then we use the error data
                    json_data = item
                    xml_data = Utils.json_to_xml(json_data, Constants.XML_ROOT_FLASK_SCRAPY)
                    break
            else:
                # only set the data is succ
                json_data = item
                xml_data = Utils.json_to_xml(json_data, Constants.XML_ROOT_FLASK_SCRAPY)
                error_data = None
                break

    # stop thread
    if crawler.is_alive():
        crawler.terminate()

    if error_data:
        # we got response from spider but it is an error data
        # record failed vins
        FlaskScrapyStatus.save_or_update(key, spider_name, True)
        logging.info('Finish searching jobs for ' + key + ', and not found.')
        if xml_data:
            #error data is come from the correct spider, then just return the error data
            return Response(xml_data, mimetype=Constants.MINETYPE_TEXT_XML)
        else:
            # this vin cannot found from all spider
            raise NotFoundError('Data is not found')
    elif not xml_data:
        # no error and no response from spider, it must be a http error, like timeout, site change or site down
        FlaskScrapyStatus.save_or_update(key, spider_name, True)
        raise HttpError('No response from the site')
    else:
        # no error and we have data, then update cache
        FlaskScrapyCache.save_or_update(key, spider_name, xml_data)
        FlaskScrapyStatus.save_or_update(key, spider_name, False)
        logging.info('Finish searching jobs for ' + key)
        return Response(xml_data, mimetype=Constants.MINETYPE_TEXT_XML)