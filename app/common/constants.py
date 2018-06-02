__author__ = 'chenfeiyu'

class Constants():
    # TODO put other spider name here
    SPIDER_NAME_TEST_SPIDER = 'test_spider'
    # we check table spider_configure instead

    XML_ROOT_ADMIN = 'Admin'
    XML_ROOT_ERROR = 'Error'
    XML_ROOT_REGISTRATION = 'Registration'
    XML_ROOT_SPIDER_NAME = 'SpiderName'
    XML_ERROR_TYPE = 'Type'
    XML_ERROR_MESSAGE = 'Message'
    XML_ERROR_STATUS_CODE = 'StatusCode'

    XML_ROOT_FLASK_SCRAPY = 'FlaskScrapy'

    VALUE_YES = 'yes'
    VALUE_NO = 'no'

    VALUE_STATE_ON = 'on'
    VALUE_STATE_OFF = 'off'

    ERROR_TYPE_BAD_REQUEST = 'Bad request'
    ERROR_TYPE_UNAUTHORIZED = 'Unauthorized'
    ERROR_TYPE_FORBIDDEN = 'Forbidden'
    ERROR_TYPE_HTTP = 'HTTP error'
    ERROR_TYPE_TIMEOUT = 'Request timeout'
    ERROR_TYPE_NOT_FOUND = 'Not found'
    ERROR_TYPE_PROCESSING = 'Processing error'
    ERROR_TYPE_NO_RESPONSE = 'No response'

    HTTP_CODE_401 = 401
    HTTP_CODE_403 = 403
    HTTP_CODE_404 = 404
    HTTP_CODE_408 = 408
    HTTP_CODE_500 = 500

    VIN_LENGTH = 17

    PARAM_DATE_FROM = 'date_from'

    REPLACEMENTS = [
        ("&quot;", "\""),
        ("&apos;", "'"),
        ("&amp;", "&"),
        ("&lt;", "<"),
        ("&gt;", ">"),
        ("&laquo;", "<<"),
        ("&raquo;", ">>"),
        ("&#039;", "'"),
        ("&#8220;", "\""),
        ("&#8221;", "\""),
        ("&#8216;", "\'"),
        ("&#8217;", "\'"),
        ("&#9632;", ""),
        ("&#8226;", "-"),
        (u'\xa0', '')
    ]

    # used to map some data like five-speed to 5-speed
    numbers_map = {
        'one':'1',
        'two':'2',
        'three':'3',
        'four':'4',
        'five':'5',
        'six':'6',
        'seven':'7',
        'eight':'8',
        'nine':'9'
    }

    MINETYPE_TEXT_XML = 'text/xml'
