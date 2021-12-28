from time import sleep

from mock import Mock
import pymysql

from pymysql import OperationalError

_CONNECTION = False
_RETRY_COUNT = 0
_MAX_RETRY_ATTEMPTS = 3


def reset():
    global _CONNECTION
    _CONNECTION = False


cursor_mock = Mock(pymysql.cursors.DictCursor)
connection_mock = Mock(pymysql.connect)
connection_mock.connect.return_value = True
connection_mock.cursor.return_value = cursor_mock


def mock_raise_exception():
    # raise Exception('Connection exception')
    raise OperationalError((1045, "Access denied for user 'undefined'@'192.168.160.1' (using password: YES)"))


def get_connection(config=None, connect=True, retry=False):
    global _CONNECTION, _RETRY_COUNT, _MAX_RETRY_ATTEMPTS, connection_mock

    from lambda_app.logging import get_logger
    from lambda_app.config import get_config

    logger = get_logger()

    if not _CONNECTION:
        connection = None
        if config is None:
            config = get_config()
        try:
            params = {
                'host': config.DB_HOST,
                'user': config.DB_USER,
                'password': config.DB_PASSWORD,
                'db': config.DB
            }

            connection = connection_mock

            if connect:
                connection.connect()
            _CONNECTION = connection
            _RETRY_COUNT = 0
            logger.info('Connected')
        except Exception as err:
            if _RETRY_COUNT == _MAX_RETRY_ATTEMPTS:
                _RETRY_COUNT = 0
                logger.error(err)
                connection = None
                return connection
            else:
                logger.error(err)
                logger.info('Trying to reconnect... {}'.format(_RETRY_COUNT))

                sleep(0.1)
                # retry
                if not retry:
                    _RETRY_COUNT += 1
                    # Fix para tratar diff entre docker/local
                    if config.DB_HOST == 'mysql':
                        old_value = config.DB_HOST
                        config.DB_HOST = 'localhost'
                        logger.info(
                            'Changing the endpoint from {} to {}'.format(old_value, config.DB_HOST))
                    return get_connection(config, True)
    else:
        connection = _CONNECTION

    return connection
