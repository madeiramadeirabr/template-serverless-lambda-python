# fix config loaded
import inspect
import logging
import os

from lambda_app import APP_NAME, APP_VERSION

_CONFIG = None


class Configuration:
    # APP
    APP_ENV = os.getenv("APP_ENV")
    APP_NAME = ''
    APP_VERSION = ''

    # LOG
    LOG_LEVEL = logging.INFO

    # NEW RELIC
    NEW_RELIC_DEVELOPER_MODE = os.getenv("APP_ENV")
    NEW_RELIC_LICENSE_KEY = os.getenv("NEW_RELIC_LICENSE_KEY")
    NEW_RELIC_LOG_HOST = os.getenv("NEW_RELIC_LOG_HOST")

    DB_HOST = ""
    DB_USER = ""
    DB_PASSWORD = ""
    DB = ""

    APP_QUEUE = ""

    REDIS_HOST = ""
    REDIS_PORT = 6379
    REGION_NAME = ""

    SQS_ENDPOINT = None
    SQS_LOCALSTACK = os.getenv("APP_SQS_LOCALSTACK")
    SECRET_KEY = 'teste'

    def __init__(self):
        # APP
        self.APP_ENV = os.getenv("APP_ENV") if 'APP_ENV' in os.environ else 'development'
        self.APP_NAME = APP_NAME
        self.APP_VERSION = APP_VERSION
        self.SECRET_KEY = os.getenv("SECRET_KEY") if 'SECRET_KEY' in os.environ else self.SECRET_KEY

        self.LOG_LEVEL = os.getenv("LOG_LEVEL") if 'LOG_LEVEL' in os.environ else self.LOG_LEVEL

        self.DB_HOST = os.getenv("DB_HOST") if 'DB_HOST' in os.environ else self.DB_HOST
        self.DB_USER = os.getenv("DB_USER") if 'DB_USER' in os.environ else self.DB_USER
        self.DB_PASSWORD = os.getenv("DB_PASSWORD") if 'DB_PASSWORD' in os.environ else self.DB_PASSWORD
        self.DB = os.getenv("DB") if 'DB' in os.environ else self.DB

        self.APP_QUEUE = os.getenv("APP_QUEUE") if 'APP_QUEUE' in os.environ else self.APP_QUEUE

        self.REDIS_HOST = os.getenv("REDIS_HOST") if 'REDIS_HOST' in os.environ else self.REDIS_HOST
        self.REDIS_PORT = os.getenv("REDIS_PORT") if 'REDIS_PORT' in os.environ else self.REDIS_PORT
        self.REGION_NAME = os.getenv("REGION_NAME") if 'REGION_NAME' in os.environ else self.REGION_NAME

        self.SQS_ENDPOINT = os.getenv("SQS_ENDPOINT") if 'SQS_ENDPOINT' in os.environ else self.SQS_ENDPOINT
        self.SQS_LOCALSTACK = os.getenv("SQS_LOCALSTACK") if 'SQS_LOCALSTACK' in os.environ else self.SQS_LOCALSTACK

    def __dict__(self):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        return {k: v for k, v in attributes if not (k.startswith('__') and k.endswith('__'))}

    def to_dict(self):
        return self.__dict__()


def reset():
    global _CONFIG
    _CONFIG = None


def get_config():
    global _CONFIG
    if not _CONFIG:
        config = Configuration()
        _CONFIG = config
    else:
        config = _CONFIG
    return config
