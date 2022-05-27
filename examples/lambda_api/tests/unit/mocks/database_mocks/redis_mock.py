from time import sleep
from unittest.mock import Mock

import fakeredis

from flambda_app.database.redis import RedisConnector

_CONNECTION = False
_RETRY_COUNT = 0
_MAX_RETRY_ATTEMPTS = 3

server = fakeredis.FakeServer()
connection_mock = fakeredis.FakeStrictRedis(server=server)


def reset():
    global _CONNECTION
    _CONNECTION = False


def get_connection(config=None, retry=False):
    global _CONNECTION, _RETRY_COUNT, _MAX_RETRY_ATTEMPTS
    if not _CONNECTION:
        connection = None

        from flambda_app.config import get_config
        from flambda_app.logging import get_logger

        logger = get_logger()

        if config is None:
            config = get_config()

        try:
            host = config.REDIS_HOST
            port = config.REDIS_PORT
            test = False
            try:
                connection = connection_mock
                test = connection.set('connection', 'true')
            except Exception as err:
                logger.error(err)
                # docker
                if host == 'redis':
                    # localhost
                    host = 'localhost'
                    connection = connection_mock
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


redis_connector_mock = Mock(RedisConnector)
redis_connector_mock.get_connection.side_effect = get_connection
