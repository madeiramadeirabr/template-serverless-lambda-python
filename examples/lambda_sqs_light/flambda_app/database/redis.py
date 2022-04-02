"""
Redis Module for Flambda APP
Version: 1.0.0
"""
from time import sleep

import redis

from flambda_app.config import get_config
from flambda_app.logging import get_logger

_CONNECTION = False
_RETRY_COUNT = 0
_MAX_RETRY_ATTEMPTS = 3


def reset():
    global _CONNECTION
    _CONNECTION = False


class RedisConnector:
    def __init__(self, config=None, logger=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # logger
        self.config = config if config is not None else get_config()
        # last_exception
        self.exception = None
        # singleton
        self.connection = None

    def get_connection(self, retry=False):
        global _CONNECTION, _RETRY_COUNT, _MAX_RETRY_ATTEMPTS
        if not self.connection:
            connection = None

            try:
                host = self.config.get('REDIS_HOST', None)
                port = self.config.get('REDIS_PORT', None)
                test = False
                try:
                    connection = redis.Redis(
                        host=host,
                        port=port
                    )
                    test = connection.set('connection', 'true')
                except Exception as err:
                    self.logger.error(err)
                    # docker
                    if host == 'redis':
                        # localhost
                        host = 'localhost'
                        connection = redis.Redis(
                            host=host,
                            port=port
                        )
                        test = connection.set('connection', 'true')

                if not test:
                    raise Exception('Redis - Unable to connect')
                else:
                    self.connection = connection
                    _CONNECTION = connection
                    _RETRY_COUNT = 0
                    self.logger.info('Redis - Connected')
            except Exception as err:
                if _RETRY_COUNT == _MAX_RETRY_ATTEMPTS:
                    _RETRY_COUNT = 0
                    self.logger.error(err)
                    connection = None
                    return connection
                else:
                    self.logger.error(err)
                    self.logger.info('Redis - Trying to reconnect... {}'.format(_RETRY_COUNT))

                    sleep(0.1)
                    # retry
                    if not retry:
                        _RETRY_COUNT += 1
                        return self.get_connection()
        else:
            connection = self.connection

        return connection
