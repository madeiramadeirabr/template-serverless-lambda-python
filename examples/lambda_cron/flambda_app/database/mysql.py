"""
MySQL Module for Flambda APP
Version: 1.0.0
"""
from time import sleep

import pymysql

from flambda_app.config import get_config
from flambda_app.logging import get_logger

_CONNECTION = False
_RETRY_COUNT = 0
_MAX_RETRY_ATTEMPTS = 3


def reset():
    global _CONNECTION
    _CONNECTION = False


class MySQLConnector:
    def __init__(self, config=None, logger=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # logger
        self.config = config if config is not None else get_config()
        # last_exception
        self.exception = None

    def get_connection(self, connect=True, retry=False):
        global _CONNECTION, _RETRY_COUNT, _MAX_RETRY_ATTEMPTS
        if not _CONNECTION:
            connection = None

            try:
                params = {
                    'host': self.config.get('DB_HOST'),
                    'user': self.config.get('DB_USER'),
                    'password': self.config.get('DB_PASSWORD'),
                    'db': self.config.get('DB')
                }

                connection = pymysql.connect(host=params['host'],
                                             user=params['user'],
                                             password=params['password'],
                                             database=params['db'],
                                             cursorclass=pymysql.cursors.DictCursor)
                if connect:
                    connection.connect()
                _CONNECTION = connection
                _RETRY_COUNT = 0
                self.logger.info('Connected')
            except Exception as err:
                if _RETRY_COUNT == _MAX_RETRY_ATTEMPTS:
                    _RETRY_COUNT = 0
                    self.logger.error(err)
                    connection = None
                    return connection
                else:
                    self.logger.error(err)
                    self.logger.info('Trying to reconnect... {}'.format(_RETRY_COUNT))

                    sleep(0.1)
                    # retry
                    if not retry:
                        _RETRY_COUNT += 1
                        # Fix para tratar diff entre docker/local
                        if self.config.get('DB_HOST') == 'mysql':
                            old_value = self.config.get('DB_HOST')
                            self.config.set('DB_HOST', 'localhost')
                            self.logger.info(
                                'Changing the endpoint from {} to {}'.format(
                                    old_value, self.config.get('DB_HOST')))
                        return self.get_connection(True)
        else:
            connection = _CONNECTION

        return connection
