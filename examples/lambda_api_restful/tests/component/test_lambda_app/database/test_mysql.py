import unittest

from tests.component.componenttestutils import BaseComponentTestCase
from lambda_app.config import get_config
from lambda_app.database.mysql import get_connection, reset
from tests.unit.testutils import get_function_name


class MySQLTestCase(BaseComponentTestCase):

    def setUp(self):
        super().setUp()
        # Para que os testes possam ser executados de forma completa, precisamos resetar esta variavel interna
        reset()

    def test_connection(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        config = get_config()
        self.logger.info('DB_HOST: {}'.format(config.DB_HOST))
        self.logger.info('DB_USER: {}'.format(config.DB_USER))
        self.logger.info('DB: {}'.format(config.DB))

        connection = get_connection()

        self.assertIsNotNone(connection)

    def test_connection_error(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        config = get_config()
        # forca os parametros
        config.DB_HOST = 'localhost'
        config.DB_USER = 'undefined'

        self.logger.info('DB_HOST: {}'.format(config.DB_HOST))
        self.logger.info('DB_USER: {}'.format(config.DB_USER))
        self.logger.info('DB: {}'.format(config.DB))
        connection = get_connection(config)

        self.assertIsNone(connection)


if __name__ == '__main__':
    unittest.main()
