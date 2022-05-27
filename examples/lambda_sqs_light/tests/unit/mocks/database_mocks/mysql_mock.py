import random
from time import sleep

from mock import Mock
import pymysql
from mock.mock import MagicMock

from pymysql import OperationalError

# ************************
# Cursor
# ************************
# def execute(self, query, args=None):
#     return True
from flambda_app.database.mysql import MySQLConnector

iterable = MagicMock(return_value=iter([MagicMock(return_value=1), MagicMock(return_value=2)]))
cursor_mock = Mock(pymysql.cursors.DictCursor)
cursor_mock.__iter__ = iterable
cursor_mock.execute.side_effect = lambda query, args=None: True
cursor_mock.fetchone.side_effect = lambda: None
cursor_mock.fetchall.side_effect = lambda: iterable
# ************************
# Connect mock
# ************************
connect_mock = Mock(pymysql.connect)
# ************************
# Connection Mock
# ************************
connection_mock = Mock(pymysql.connections.Connection)
connection_mock.connect.return_value = True
connection_mock.cursor.return_value = cursor_mock
connection_mock.insert_id.side_effect = lambda: random.randrange(1, 100)

_CONNECTION = False
_RETRY_COUNT = 0
_MAX_RETRY_ATTEMPTS = 3


def reset():
    global _CONNECTION
    _CONNECTION = False


def mock_raise_exception():
    raise OperationalError((1045, "Access denied for user 'undefined'@'192.168.160.1' (using password: YES)"))


def get_connection(config=None, connect=True, retry=False):
    global _CONNECTION, _RETRY_COUNT, _MAX_RETRY_ATTEMPTS, connection_mock

    from flambda_app.logging import get_logger
    from flambda_app.config import get_config

    logger = get_logger()

    if not _CONNECTION:
        connection = None
        if config is None:
            config = get_config()
        try:
            params = {
                'host': config.get('DB_HOST'),
                'user': config.get('DB_USER'),
                'password': config.get('DB_PASSWORD'),
                'db': config.get('DB')
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
                    if config.get('DB_HOST') == 'mysql':
                        old_value = config.get('DB_HOST')
                        config.set('DB_HOST', 'localhost')
                        logger.info(
                            'Changing the endpoint from {} to {}'.format(old_value, config.get('DB_HOST')))
                    return get_connection(config, True)
    else:
        connection = _CONNECTION

    return connection


mysql_connector_mock = Mock(MySQLConnector)
mysql_connector_mock.get_connection.side_effect = get_connection
