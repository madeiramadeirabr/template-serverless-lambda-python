"""
General Helper Module for Flambda APP
Version: 1.0.0
"""
import hashlib
import json
import os
import sys
import traceback
from datetime import datetime
from datetime import date
from enum import Enum
from boot import get_environment as get_env

import pytz

from flambda_app.logging import get_logger, get_console_logger

TZ_AMERICA_SAO_PAULO = 'America/Sao_Paulo'


def generate_process():
    return generate_hash(str("default" + datetime.now().isoformat()))


def generate_hash(data):
    event_hash = hashlib.sha256(str(data).encode()).hexdigest()
    return event_hash


def open_vendor_file(filename, mode):
    if __package__:
        current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
    else:
        current_path = os.path.abspath(os.path.dirname(__file__))

    directories = [
        '.',
        './vendor',
        '/opt/python/lib/python%s.%s/site-packages' % sys.version_info[:2],
        current_path
    ]

    for dirname in directories:
        full_path = os.path.join(dirname, filename)
        if os.path.isfile(full_path):
            return open(full_path, mode=mode)


def empty(where):
    result = False
    if isinstance(where, dict) and where == {}:
        result = True
    elif isinstance(where, list) and len(where) == 0:
        result = True
    elif isinstance(where, str) and where == '':
        result = True
    elif isinstance(where, bytes) and len(where) == 0:
        result = True
    elif where is None:
        result = True
    return result


def has_attr(object, attribute):
    try:
        if hasattr(object, attribute):
            return True
    except Exception as err:
        return False


def to_dict(obj, force_str=False):
    data = obj.__dict__
    if force_str:
        return {k: str(v) for k, v in data.items() if v is not None}
    else:
        _dict = {}
        for k, v in data.items():
            if isinstance(v, Enum):
                _dict[k] = str(v)
            elif getattr(v, "to_dict", None):
                # recursivo
                _dict[k] = to_dict(v, force_str)
            else:
                _dict[k] = v
        return _dict


def to_json(obj):
    return json.dumps(obj, default=str)


def debug_mode():
    result = False
    if 'DEBUG' in os.environ and str(os.getenv('DEBUG')).lower() == 'true':
        result = True
    return result


def convert_to_int(str_value):
    """
    Essa função foi criada para ser usada em loops funcionais z = [x for x in y]
    :param str_value:
    :return:
    :rtype: int
    """
    value = 0
    try:
        value = int(str_value)
    except Exception as err:
        get_logger().error(err)

    return value


def convert_to_float(str_value):
    """
    Essa função foi criada para ser usada em loops funcionais z = [x for x in y]
    :param str_value:
    :return:
    :rtype: float
    """
    value = 0
    try:
        value = float(str_value)
    except Exception as err:
        get_logger().error(err)

    return value


def datetime_now_with_timezone(timezone_name='America/Sao_Paulo'):
    return datetime.now(tz=pytz.timezone(timezone_name))


def datetime_format_for_database(datetime_object):
    return datetime_object.strftime('%Y-%m-%d %H:%M:%S')


def datetime_format_for_lifecycle(datetime_object):
    return datetime_object.isoformat()


def datetime_add_timezone(datetime_object: datetime, timezone_name='America/Sao_Paulo'):
    return datetime.fromtimestamp(datetime_object.timestamp(), tz=pytz.timezone(timezone_name))


def datetime_convert_utc_to_local_timezone(datetime_object: datetime, timezone_name='America/Sao_Paulo'):
    local_tz = pytz.timezone(timezone_name)
    datetime_with_timezone = datetime_object.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(datetime_with_timezone)
    # return datetime_with_timezone


def datetime_convert_local_timezone_to_utc(datetime_object: datetime, timezone_name='America/Sao_Paulo'):
    local_tz = pytz.timezone(timezone_name)
    utc_tz = pytz.utc
    datetime_with_timezone = datetime_object.replace(tzinfo=local_tz).astimezone(utc_tz)
    return utc_tz.normalize(datetime_with_timezone)
    # return datetime_with_timezone


def get_protocol():
    protocol = 'http://'
    if is_https():
        protocol = 'https://'
    return protocol


def is_https():
    result = False
    if 'HTTPS' in os.environ and str(os.getenv('HTTPS')).lower() == 'true':
        result = True
    return result


def is_count_request(app):
    request = app.current_request.query_params
    return True if request is not None and (request.get('count') == "true" or request.get('count') == "1") else False


def print_routes(app, logger=None):
    """
    :param logger:
    :param (chalice.Chalice) app:
    :return:
    """
    if logger is None:
        logger = get_console_logger()
    logger.info('List of routes:')

    if has_attr(app, 'get_routes'):
        routes = app.get_routes()
    elif has_attr(app, 'url_map'):
        routes = {rule.rule: dict.fromkeys(rule.methods, 0) for rule in app.url_map.iter_rules()}
    else:
        routes = app.routes
    for path, dict_route in routes.items():
        methods = list(dict_route.keys())
        for method in methods:
            logger.info('Route: %s - %s', method, path)


def get_environment():
    return get_env()


def is_running_on_lambda(force=False):
    if get_environment() == 'development':
        return False if force is False else True
    else:
        return os.environ.get("AWS_EXECUTION_ENV") is not None


def has_method(obj, method_name):
    if has_attr(obj, method_name):
        method = getattr(obj, method_name, None)
        if callable(method):
            return True
        else:
            return False
    else:
        return False


def convert_object_dates_to_iso_with_timezone(target_object, timezone_name=None):
    attrs = [att for att in dir(target_object) if not att.startswith('__')]
    for att in attrs:
        try:
            val = getattr(target_object, att, None)
            if isinstance(val, datetime) or isinstance(val, date):
                if timezone_name:
                    val = datetime_add_timezone(val, TZ_AMERICA_SAO_PAULO)
                setattr(target_object, att, val.isoformat())
        except Exception as err:
            get_logger().error(err)


def convert_object_dates_to_iso_utc(target_object):
    attrs = [att for att in dir(target_object) if not att.startswith('__')]
    for att in attrs:
        try:
            val = getattr(target_object, att, None)
            if isinstance(val, datetime):
                # val = datetime_add_timezone(val)
                val = datetime_convert_local_timezone_to_utc(val)
                setattr(target_object, att, val.isoformat())
        except Exception as err:
            get_logger().error(err)


def get_function_name(class_name=""):
    fn_name = class_name + "::" + traceback.extract_stack(None, 2)[0][2]
    if not class_name:
        fn_name = traceback.extract_stack(None, 2)[0][2]
    return fn_name


def convert_list_to_dict(item_list, key_name):
    result = dict()
    if isinstance(item_list, list):
        for item in item_list:
            if isinstance(item, dict) and key_name in item.keys():
                result[item.get(key_name)] = item

    return result
