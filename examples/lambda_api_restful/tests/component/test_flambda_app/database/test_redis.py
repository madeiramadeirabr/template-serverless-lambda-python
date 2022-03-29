"""
Redis Component Test for Flambda APP
Version: 1.0.0
"""
import unittest

from tests.component.componenttestutils import BaseComponentTestCase
from flambda_app.config import get_config
from flambda_app.database.redis import RedisConnector, reset
from tests.unit.testutils import get_function_name


class RedisTestCase(BaseComponentTestCase):

    def setUp(self):
        super().setUp()
        # Para que os testes possam ser executados de forma completa, precisamos resetar esta variavel interna
        reset()

    def test_connection(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        config = get_config()
        self.logger.info('REDIS_HOST: {}'.format(config.get('REDIS_HOST', None)))
        self.logger.info('REDIS_PORT: {}'.format(config.get('REDIS_PORT', None)))

        connection = RedisConnector().get_connection()

        self.assertIsNotNone(connection)

    def test_connection_singleton(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        config = get_config()
        self.logger.info('REDIS_HOST: {}'.format(config.get('REDIS_HOST', None)))
        self.logger.info('REDIS_PORT: {}'.format(config.get('REDIS_PORT', None)))

        connector = RedisConnector()
        first_connection = connector.get_connection()
        last_connection = None
        for i in range(0, 3):
            last_connection = connector.get_connection()

        self.assertIsNotNone(first_connection)
        self.assertIsNotNone(last_connection)
        self.assertEquals(first_connection, last_connection)

    def test_connection_error(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        config = get_config()
        # forca os parametros
        config.REDIS_HOST = 'localhost'
        config.REDIS_PORT = '1111'

        self.logger.info('REDIS_HOST: {}'.format(config.REDIS_HOST))
        self.logger.info('REDIS_PORT: {}'.format(config.REDIS_PORT))
        connection = RedisConnector(config=config).get_connection()

        self.assertIsNone(connection)


if __name__ == '__main__':
    unittest.main()
