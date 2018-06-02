from flask import jsonify, request, current_app, url_for, g, Response
import logging
from . import api
from ..common.utils import Utils
from ..common.constants import Constants
from ..common.exceptions import ValidationError
from ..models.spider_configure import SpiderConfigure
from .authentication import auth


# http --auth cartell:CaRtelLiStHeAdmiN GET http://0.0.0.0:5002/api/v1.0/admin/check
# http://0.0.0.0:5002/api/v1.0/admin/turn_on?spider=test_spider
# http://0.0.0.0:5002/api/v1.0/admin/turn_off?spider=test_spider
@api.route('/admin/<action>', methods=['GET'])
def spider_admin(action):
    if action == 'check':
        return check_spider_states()
    elif action == 'turn_on':
        return turn_on_spiders()
    elif action == 'turn_off':
        return turn_off_spiders()
    else:
        raise ValidationError('Invalid admin action %s ' % action)


def check_spider_states():
    spider_configures = SpiderConfigure.get_all_spiders()
    json_data = []
    for spider_configure in spider_configures:
        json_data.append(spider_configure.to_json())
    return Response(Utils.json_to_xml({'SpiderState': json_data}, Constants.XML_ROOT_ADMIN), mimetype=Constants.MINETYPE_TEXT_XML)


def turn_on_spiders():
    spider_names = Utils.get_spider_names(request)
    if not spider_names:
        raise ValidationError('Missing spider')
    SpiderConfigure.turn_on(spider_names)
    return check_spider_states()


def turn_off_spiders():
    spider_names = Utils.get_spider_names(request)
    if not spider_names:
        raise ValidationError('Missing spider')
    SpiderConfigure.turn_off(spider_names)
    return check_spider_states()