import hashlib
import json
import os
import sys
from datetime import datetime
from enum import Enum

import pytz

from flask_app.logging import get_logger

TZ_AMERICA_SAO_PAULO = 'America/Sao_Paulo'


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
        # return {k: v for k, v in data.items() if v is not None}
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
    return json.dumps(obj)


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


def print_routes(app, logger):
    """
    :param logger:
    :param (chalice.Chalice) app:
    :return:
    """
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
