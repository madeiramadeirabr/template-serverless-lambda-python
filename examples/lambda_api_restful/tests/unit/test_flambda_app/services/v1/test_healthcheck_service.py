"""
HealthCheck Service Unit Test for Flambda APP
Version: 1.0.0
"""
import unittest

from flambda_app.config import get_config
from flambda_app.services.v1.healthcheck import HealthCheckResult
from flambda_app.services.v1.healthcheck.resources import MysqlConnectionHealthCheck, RedisConnectionHealthCheck, \
    SelfConnectionHealthCheck
from flambda_app.services.v1.healthcheck_service import HealthCheckService
from tests.unit.mocks.database_mocks.mysql_mock import get_connection as mysql_get_connection
from tests.unit.mocks.database_mocks.redis_mock import get_connection as redis_get_connection
from tests.unit.mocks.http_mocks import http_client_mock
from tests.unit.testutils import get_function_name, BaseUnitTestCase


class HealthCheckServiceTestCase(BaseUnitTestCase):
    EXECUTE_FIXTURE = True
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        BaseUnitTestCase.setUpClass()
        cls.CONFIG = get_config()

    def setUp(self):
        super().setUp()
        self.config = get_config()
        self.mysql_connection = mysql_get_connection()
        self.redis_connection = redis_get_connection()
        self.http_client = http_client_mock
        self.service = HealthCheckService(self.logger, self.config)

    def test_add_check(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.service.add_check("MysqlConnection", MysqlConnectionHealthCheck(
            self.logger, self.config, self.mysql_connection), ["db"])

        result = self.service.get_result()
        self.logger.info(result)

        self.assertIsInstance(result, dict)
        self.assertTrue('status' in result)

    def test_add_lambda_check(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.service.add_check("Lambda test", lambda: HealthCheckResult.healthy("test success"), ["lambda_test"])

        result = self.service.get_result()
        self.logger.info(result)

        self.assertIsInstance(result, dict)
        self.assertTrue('status' in result)

    def test_add_multi_checks(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.service.add_check("self", SelfConnectionHealthCheck(
            self.logger, self.config, self.http_client), [])
        self.service.add_check("mysql", MysqlConnectionHealthCheck(
            self.logger, self.config, self.mysql_connection), ["db"])
        self.service.add_check("redis", RedisConnectionHealthCheck(
            self.logger, self.config, self.redis_connection), ["redis"])

        result = self.service.get_result()
        self.logger.info(result)

        self.assertIsInstance(result, dict)
        self.assertTrue('status' in result)

    def test_get_response(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.service.add_check("self", SelfConnectionHealthCheck(
            self.logger, self.config, self.http_client), [])
        self.service.add_check("mysql", MysqlConnectionHealthCheck(
            self.logger, self.config, self.mysql_connection), ["db"])
        self.service.add_check("redis", RedisConnectionHealthCheck(
            self.logger, self.config, self.redis_connection), ["redis"])

        response = self.service.get_response()
        self.logger.info(response.data)
        self.assertIsNotNone(response.data)


if __name__ == '__main__':
    unittest.main()
