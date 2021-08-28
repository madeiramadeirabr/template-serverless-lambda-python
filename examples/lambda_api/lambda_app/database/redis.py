from time import sleep

import redis

from lambda_app.config import get_config
from lambda_app.logging import get_logger

logger = get_logger()

_CONNECTION = False
_RETRY_COUNT = 0
_MAX_RETRY_ATTEMPTS = 3


def reset():
    global _CONNECTION
    _CONNECTION = False


def get_connection(config=None, retry=False):
    global _CONNECTION, _RETRY_COUNT, _MAX_RETRY_ATTEMPTS
    if not _CONNECTION:
        connection = None

        if config is None:
            config = get_config()

        try:
            host = config.REDIS_HOST
            port = config.REDIS_PORT
            test = False
            try:
                connection = redis.Redis(
                    host=host,
                    port=port
                )
                test = connection.set('connection', 'true')
            except Exception as err:
                logger.error(err)
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
                _CONNECTION = connection
                _RETRY_COUNT = 0
                logger.info('Redis - Connected')
        except Exception as err:
            if _RETRY_COUNT == _MAX_RETRY_ATTEMPTS:
                _RETRY_COUNT = 0
                logger.error(err)
                connection = None
                return connection
            else:
                logger.error(err)
                logger.info('Redis - Trying to reconnect... {}'.format(_RETRY_COUNT))

                sleep(0.1)
                # retry
                if not retry:
                    _RETRY_COUNT += 1
                    return get_connection(config)
    else:
        connection = _CONNECTION

    return connection
