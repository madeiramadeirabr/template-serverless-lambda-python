"""
Logging Module for Flambda APP
Version: 1.0.2
"""
import os
import logging

from flambda_app import APP_NAME, APP_VERSION


def get_environment():
    environment = 'development'
    if 'ENVIRONMENT' in os.environ:
        environment = os.environ['ENVIRONMENT']
    elif 'ENVIRONMENT_NAME' in os.environ:
        environment = os.environ['ENVIRONMENT_NAME']
    elif 'APP_ENV' in os.environ:
        environment = os.environ['APP_ENV']
    return environment


_LOGGER = None
_LOG_ATTRIBUTES = {
    "service": "%s:%s" % (APP_NAME, APP_VERSION),
    "service_name": APP_NAME,
    "hostname": os.environ["API_SERVER"] if "API_SERVER" in os.environ else "",
    "environment": get_environment()
}


class LoggerProfile:
    CONSOLE = 'console'
    ELK = 'elk'
    NEWRELIC = 'newrelic'
    NEWRELIC_SQS = 'newrelic_sqs'


_LOGGER_PROFILE = LoggerProfile.CONSOLE


def set_profile(profile: LoggerProfile):
    global _LOGGER_PROFILE
    _LOGGER_PROFILE = profile


def get_logger_profile():
    global _LOGGER_PROFILE
    return _LOGGER_PROFILE


def reset():
    global _LOGGER
    _LOGGER = None


def get_log_attributes():
    global _LOG_ATTRIBUTES
    return _LOG_ATTRIBUTES


def set_log_attributes(data: dict):
    global _LOG_ATTRIBUTES
    _LOG_ATTRIBUTES = {**_LOG_ATTRIBUTES, **data}


def get_log_level():
    log_level = os.app_env = logging.getLevelName(
        os.getenv("LOG_LEVEL").upper()) if 'LOG_LEVEL' in os.environ else logging.INFO
    return log_level


def get_tracker_logger(profile: LoggerProfile = None, **kwargs):
    log_level = logging.INFO
    log_name = "tracker-{}".format(APP_NAME)
    log_filename = None
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=log_format, filename=log_filename, level=log_level)
    logger = logging.getLogger(log_name)
    if 'default_index' not in kwargs:
        kwargs['default_index'] = 'event-tracking'
    set_handler_by_profile(logger, profile=profile, **kwargs)
    return logger


def get_console_logger():
    log_level = get_log_level()
    log_name = "console-{}".format(APP_NAME)
    log_filename = None
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=log_format, filename=log_filename, level=log_level)
    logger = logging.getLogger(log_name)
    # print('get_console_logger - logger.level', logger.level)
    return logger


def get_stream_handler():
    return get_console_logger().parent.handlers[0]


def set_debug_mode(logger, level=None, add_stream_handler=True):
    global _LOGGER_PROFILE
    has_stream_logger = False
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            has_stream_logger = True
            break
    # verify root logger
    if not has_stream_logger:
        for handler in logger.root.handlers:
            if isinstance(handler, logging.StreamHandler):
                if _LOGGER_PROFILE == LoggerProfile.CONSOLE:
                    has_stream_logger = True
                else:
                    # ignore StreamHandler stderr (NOTSET)
                    if handler.name is not None and handler.level != 0:
                        has_stream_logger = True
                        break

    if not has_stream_logger and add_stream_handler:
        stream_handler = get_stream_handler()
        stream_handler.setLevel(get_log_level())
        logger.addHandler(stream_handler)
    logger.level = level if level is not None else logging.DEBUG


def get_logger(profile: LoggerProfile = None, **kwargs):
    global _LOGGER
    force = False
    log_level = get_log_level()

    if 'force' in kwargs:
        force = kwargs['force']

    if not _LOGGER or force:
        log_name = kwargs['log_name'] if 'log_name' in kwargs else APP_NAME
        log_filename = None

        if profile:
            log_format = '%(asctime)s - %(name)s - {} - %(levelname)s - %(message)s'.format(profile)
        else:
            log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=log_level)
        logger = logging.getLogger(log_name)

        # define the profile
        if profile:
            set_profile(profile)

        # handlers by profile
        set_handler_by_profile(logger, profile=profile, **kwargs)

        # add log level for all
        for handler in logger.handlers:
            handler.setLevel(log_level)

        # force log level
        logger.setLevel(log_level)
        # print('get_logger - profile', profile)
        # print('get_logger - setting log level', log_level)
        # print('get_logger - logger', logger)

        # factory
        logging.setLogRecordFactory(record_factory)

        _LOGGER = logger
    else:
        logger = _LOGGER

    return logger


def record_factory(*args, **kwargs):
    global _LOG_ATTRIBUTES
    record = logging.LogRecord(*args, **kwargs)
    for k, v in _LOG_ATTRIBUTES.items():
        try:
            if not hasattr(record, k):
                setattr(record, k, v)
        except Exception as err:
            get_console_logger().error(err)

    return record


def set_handler_by_profile(logger: logging.Logger, **kwargs):
    global _LOGGER_PROFILE
    if _LOGGER_PROFILE != LoggerProfile.CONSOLE:
        # Remove all handlers
        logger.handlers = []
        logger.parent.handlers = []

    add_handler_by_profile(logger, **kwargs)


def add_handler_by_profile(logger: logging.Logger, profile=None, **kwargs):
    global _LOGGER_PROFILE
    try:
        if profile is None:
            profile = _LOGGER_PROFILE

        if profile == LoggerProfile.ELK:
            from flambda_app.logging_resources.elk_resource import add_elk_handler
            add_elk_handler(logger, **kwargs)

        elif profile == LoggerProfile.NEWRELIC:
            from flambda_app.logging_resources.newrelic_resource import add_newrelic_handler
            # new relic attrib
            if "NEW_RELIC_ENTITY_GUID" in os.environ:
                set_log_attributes({"entity.guid": os.environ["NEW_RELIC_ENTITY_GUID"]})

            stream_handler = logger.handlers[0] if len(logger.handlers) > 0 else None
            add_newrelic_handler(logger, stream_handler, **kwargs)

        elif profile == LoggerProfile.NEWRELIC_SQS:
            from flambda_app.logging_resources.newrelic_sqs_resource import add_newrelic_handler
            # new relic attrib
            if "NEW_RELIC_ENTITY_GUID" in os.environ:
                set_log_attributes({"entity.guid": os.environ["NEW_RELIC_ENTITY_GUID"]})

            add_newrelic_handler(logger, **kwargs)

        # force log level
        logger.setLevel(get_log_level())

    except Exception as err:
        logger.error(err)


def remove_handler(logger: logging.Logger, class_name):
    try:
        # parent logger
        for handler in logger.parent.handlers:
            if isinstance(handler, class_name):
                logger.parent.removeHandler(handler)

        # logger
        for handler in logger.handlers:
            if isinstance(handler, class_name):
                logger.removeHandler(handler)
    except Exception as err:
        logger.error(err)


def remove_last_handler(logger: logging.Logger):
    try:
        count = len(logger.handlers)
        position = count - 1
        del logger.handlers[position]
    except Exception as err:
        logger.error(err)
