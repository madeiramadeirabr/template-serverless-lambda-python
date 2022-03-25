"""
Config Module for Flambda APP
Version: 1.0.1
"""
import inspect
import os

from flambda_app import APP_NAME, APP_VERSION, helper

_CONFIG = None


class Configuration:
    """
    Configuration class of the project, load the env vars dynamically
    """
    # APP
    APP_NAME = ''
    APP_VERSION = ''

    def __init__(self):
        # APP
        self.APP_NAME = APP_NAME
        self.APP_VERSION = APP_VERSION

        # get the env vars built dynamically on load
        env_keys = Configuration.get_env_keys()
        for k in env_keys:
            value = os.getenv(k) if k in os.environ else None
            setattr(Configuration, k, value)

    def __dict__(self):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        return {k: v for k, v in attributes if not (k.startswith('__') and k.endswith('__'))}

    def get(self, key_name, default_value=None):
        if helper.has_attr(self, key_name):
            return getattr(self, key_name)
        elif key_name in os.environ:
            value = os.environ[key_name]
            self.set(key_name, value)
            return value
        else:
            return default_value

    def set(self, key_name, value):
        if helper.has_attr(self, key_name):
            setattr(self, key_name, value)

    def to_dict(self):
        return self.__dict__()

    @staticmethod
    def get_env_keys():
        from boot import get_env_keys
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
