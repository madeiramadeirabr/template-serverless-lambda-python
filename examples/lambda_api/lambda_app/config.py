# fix config loaded
import inspect
import logging
import os

from lambda_app import APP_NAME, APP_VERSION

_CONFIG = None


class Configuration:
    # APP
    APP_NAME = ''
    APP_VERSION = ''

    def __init__(self):
        # APP
        self.APP_NAME = APP_NAME
        self.APP_VERSION = APP_VERSION

        # montagem dinamica de atributos
        env_keys = Configuration.get_env_keys()
        for k in env_keys:
            value = os.getenv(k) if k in os.environ else None
            setattr(Configuration, k, value)

    def __dict__(self):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        return {k: v for k, v in attributes if not (k.startswith('__') and k.endswith('__'))}

    def to_dict(self):
        return self.__dict__()

    @staticmethod
    def get_env_keys():
        from lambda_app.boot import get_env_keys
        return get_env_keys()


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
