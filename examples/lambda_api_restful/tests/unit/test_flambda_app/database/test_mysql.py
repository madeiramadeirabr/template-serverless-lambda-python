"""
MySQL Module Unit Test for Flambda APP
Version: 1.0.0
"""
import unittest

from flambda_app.config import get_config
from tests.unit.mocks.database_mocks.mysql_mock import get_connection, reset, connection_mock, mock_raise_exception
from tests.unit.testutils import get_function_name, BaseUnitTestCase


class MySQLTestCase(BaseUnitTestCase):

    def setUp(self):
        super().setUp()
        # Para que os testes possam ser executados de forma completa, precisamos resetar esta variavel interna
        reset()

    def test_connection(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        config = get_config()
        self.logger.info('DB_HOST: {}'.format(config.get('DB_HOST')))
        self.logger.info('DB_USER: {}'.format(config.get('DB_USER')))
        self.logger.info('DB: {}'.format(config.get('DB')))

        connection = get_connection()

        self.assertIsNotNone(connection)

    def test_connection_error(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        # **************************
        # Mocking result
        # **************************
        # sobrescreve o comportamento do mock
        connection_mock.connect.side_effect = mock_raise_exception

        config = get_config()
        # forca os parametros
        config.set('DB_HOST', 'localhost')
        config.set('DB_USER', 'undefined')

        self.logger.info('DB_HOST: {}'.format(config.get('DB_HOST')))
        self.logger.info('DB_USER: {}'.format(config.get('DB_USER')))
        self.logger.info('DB: {}'.format(config.get('DB')))
        connection = get_connection(config)

        self.assertIsNone(connection)

    @classmethod
    def tearDownClass(cls):
        # **************************
        # Mocking result
        # **************************
        # sobrescreve o comportamento do mock
        connection_mock.connect.return_value = True
        connection_mock.connect.side_effect = lambda: True


if __name__ == '__main__':
    unittest.main()
