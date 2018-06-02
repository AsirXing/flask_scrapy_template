__author__ = 'chenfeiyu'
from ..common.exceptions import ValidationError
from dicttoxml import dicttoxml
from ..common.constants import Constants
import re, logging, xmltodict, json, math
from decimal import Decimal


class Utils:
    
    @staticmethod
    def clean_data(value):
        if value is None:
            return None

        for entity, replacement in Constants.REPLACEMENTS:
            value = value.replace(entity, replacement)
        # value = value.replace(u'\xa0', '')

        value = re.sub('\t', '', value)
        value = re.sub('\n', '', value)
        value = re.sub('\r', '', value)
        value = re.sub(' +', ' ', value)
        value = value.strip()

        return value
    
    @staticmethod
    def is_empty(str):
        if str is None or str == '':
            return True
        else:
            return False

    @staticmethod
    def get_parameter(request, name, required=False):
        value = request.args.get(name)

        if value is None:
            if request.json is not None:
                value = request.json.get(name)

        if value is None and required:
            raise ValidationError('Missing %s' % name)
        else:
            value = Utils.clean_data(value)
            return value
              
    @staticmethod
    def get_latest_flag(request):
        get_latest = request.args.get('get_latest')
        if get_latest is None:
            if request.json is not None:
                get_latest = request.json.get('get_latest')
        if get_latest is not None and get_latest.lower() == 'true':
            get_latest = True
        else:
            # default searching cache first
            get_latest = False

        return get_latest

    @staticmethod
    def db_only_flag(request):
        db_only = request.args.get('db_only')
        if db_only is None:
            if request.json is not None:
                db_only = request.json.get('db_only')
        if db_only is not None and db_only.lower() == 'true':
            db_only = True
        else:
            # default searching cache first
            db_only = False

        return db_only
    
    @staticmethod
    def get_spider(request):
        spider = request.args.get('spider')
        if spider is None:
            if request.json is not None:
                spider = request.json.get('spider')

        return spider

    @staticmethod
    def get_clean_failures_flag(request):
        clean_failures = request.args.get('clean_failures')
        if clean_failures is None:
            if request.json is not None:
                clean_failures = request.json.get('clean_failures')
        if clean_failures is not None and clean_failures.lower() == 'true':
            clean_failures = True
        else:
            # default not clean the failures table
            clean_failures = False

        return clean_failures

    @staticmethod
    def get_spider_names(request):
        spiders = request.args.getlist('spider')
        if spiders is None:
            if request.json is not None:
                spiders = request.json.get('spider')
        return spiders

    @staticmethod
    def dict_to_xml(dict_data, custom_root=None, root=True):
        if dict_data is None:
            raise ValidationError('Missing dict data')
        xml = dicttoxml(dict_data, custom_root=custom_root, attr_type=False, root=root)
        return xml

    @staticmethod
    def json_to_xml(json_data, custom_root=None, root=True):
        if json_data is None:
            raise ValidationError('Missing json data')
        return Utils.dict_to_xml(dict(json_data), custom_root, root)

    @staticmethod
    def xml_to_dict(xml):
        if xml is None:
            raise ValidationError('Missing xml data')
        json_str = json.dumps(xmltodict.parse(xml))
        return json.loads(json_str)

    # both 3.00 and 3.03 are true, but 3 is false
    @staticmethod
    def is_float(value):
        try:
            x = float(value)
            if '.' in str(value):
                return True
            else:
                return False
        except ValueError:
            return False

    # 3.00 will return false, 3.01 will be true
    @staticmethod
    def is_decimal(value):
        if Utils.is_float(value):
            return (Decimal(value) % 1 != 0)
        else:
            return False

    @staticmethod
    def is_int(value):
        try:
            x = int(value)
            return True
        except ValueError:
            return False

    # this method will remove everything except digits.
    # It also removes dot, so pls be careful. e.g    3.8aaabbbccc -> 38
    @staticmethod
    def keep_only_digits(value):
        if value is None:
            return value
        return re.sub(r"\D", "", value)

    @staticmethod
    def get_first_digit_index(value):
        m = re.search("\d", value)
        if m:
            return m.start()
        else:
            return None

    @staticmethod
    def match_regex(regex, value):
        m = re.match(regex, value)
        if m:
            return True
        else:
            return False

    @staticmethod
    def replace_str(from_str, to_str, str):
        return str.replace(from_str, to_str)
