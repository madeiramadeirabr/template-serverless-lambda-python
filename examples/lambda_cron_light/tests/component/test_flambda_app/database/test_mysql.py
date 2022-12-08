"""
MySQL Component Test for Flambda APP
Version: 1.0.0
"""
import unittest

from tests.component.componenttestutils import BaseComponentTestCase
from flambda_app.config import get_config
from flambda_app.database.mysql import MySQLConnector, reset
from tests.unit.testutils import get_function_name


class MySQLTestCase(BaseComponentTestCase):

    def setUp(self):
        super().setUp()
        # Para que os testes possam ser executados de forma completa, precisamos resetar esta variavel interna
        reset()

    def test_connection(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        config = get_config()
        self.logger.info('DB_HOST: {}'.format(config.get('DB_HOST', None)))
        self.logger.info('DB_USER: {}'.format(config.get('DB_USER', None)))
        self.logger.info('DB: {}'.format(config.get('DB')))

        connection = MySQLConnector().get_connection()

        self.assertIsNotNone(connection)

    def test_connection_error(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        config = get_config()
        # forca os parametros
        config.set('DB_HOST', 'localhost')
        config.set('DB_USER', 'undefined')

        self.logger.info('DB_HOST: {}'.format(config.get('DB_HOST', None)))
        self.logger.info('DB_USER: {}'.format(config.get('DB_USER', None)))
        self.logger.info('DB: {}'.format(config.get('DB')))
        connection = MySQLConnector(config=config).get_connection()

        self.assertIsNone(connection)


if __name__ == '__main__':
    unittest.main()
