import os
import logging

from lambda_app import APP_NAME

_LOGGER = None
# fix + reset
_VERSION = "1.1.1"


def get_log_level():
    log_level = os.app_env = logging.getLevelName(
        os.getenv("LOG_LEVEL").upper()) if 'LOG_LEVEL' in os.environ else logging.INFO
    return log_level


def get_console_logger():
    log_level = get_log_level()
    log_name = "console-{}".format(APP_NAME)
    log_filename = None
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=log_format, filename=log_filename, level=log_level)
    logger = logging.getLogger(log_name)
    return logger


def get_stream_handler():
    return get_console_logger().parent.handlers[0]


def set_debug_mode(logger, level=None):
    logger.addHandler(get_stream_handler())
    logger.level = level if level is not None else logging.INFO


def get_logger():
    global _LOGGER
    if not _LOGGER:
        log_name = APP_NAME
        log_filename = None
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=get_log_level())
        logger = logging.getLogger(log_name)
        _LOGGER = logger
    else:
        logger = _LOGGER

    if logger.level == logging.NOTSET:
        # if no set, try again
        logger.level = get_log_level()

    return logger
