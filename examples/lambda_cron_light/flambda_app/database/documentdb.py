"""
DocumentDb Module for Flambda APP
Version: 1.0.0
"""
import os
from time import sleep

from flambda_app.config import get_config
from flambda_app.logging import get_logger
from pymongo import MongoClient


_CONNECTION = False
_RETRY_COUNT = 0
_MAX_RETRY_ATTEMPTS = 3


def reset():
    global _CONNECTION
    _CONNECTION = False


class MongodbConnector:
    def __init__(self, config=None, logger=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # config
        self.config = config if config is not None else get_config()
        # last_exception
        self.exception = None

    def get_connection(self, connect=True, retry=False):
        global _CONNECTION, _RETRY_COUNT, _MAX_RETRY_ATTEMPTS
        if not _CONNECTION:
            connection = None
            try:
                connection = MongoClient(
                    self.config.get('MONGO_CONNECTION_STRING')
                )

                if connect:
                    database_name = self.config.get('MONGO_DB')
                    databases_list = connection.list_database_names()

                    if database_name not in databases_list:
                        _CONNECTION = None
                        connection = None
                        raise Exception("Collection not found: {}".format(database_name))

                _CONNECTION = connection
                _RETRY_COUNT = 0
                self.logger.info('Connected')

            except Exception as err:
                if _RETRY_COUNT == _MAX_RETRY_ATTEMPTS:
                    _RETRY_COUNT = 0
                    self.logger.error(err)
                    return connection
                else:
                    self.logger.error(err)
                    self.logger.info('Trying to reconnect... {}'.format(_RETRY_COUNT))

                    sleep(0.1)
                    # retry
                    if not retry:
                        _RETRY_COUNT += 1
                        return self.get_connection(True)
        else:
            connection = _CONNECTION

        return connection
