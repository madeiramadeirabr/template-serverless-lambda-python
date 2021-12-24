import unittest

from lambda_app.config import get_config
from lambda_app.logging import get_logger
from lambda_app.services.v1.healthcheck import HealthStatus, HealthCheckResult
from lambda_app.services.v1.healthcheck.resources import MysqlConnectionHealthCheck, RedisConnectionHealthCheck, \
    SQSConnectionHealthCheck, SelfConnectionHealthCheck
from lambda_app.services.v1.healthcheck_service import HealthCheckService
from tests.component.componenttestutils import BaseComponentTestCase
from tests.unit.testutils import get_function_name


class HealthCheckServiceTestCase(BaseComponentTestCase):
    EXECUTE_FIXTURE = True
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        BaseComponentTestCase.setUpClass()
        cls.CONFIG = get_config()
        cls.CONFIG.SQS_ENDPOINT = cls.SQS_LOCALSTACK

        # fixture
        if cls.EXECUTE_FIXTURE:
            logger = get_logger()
            # logger.info('Fixture: create database')
            # todo a implementar

    def setUp(self):
        super().setUp()
        self.config = get_config()
        self.service = HealthCheckService(self.logger, self.config)

    def test_add_check(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.service.add_check("MysqlConnection", MysqlConnectionHealthCheck(self.logger, self.config), ["db"])

        # self.assertEqual(len(self.service.entries), 1)

        result = self.service.get_result()
        print(result)

        # self.assertEqual(result["status"], HealthStatus.HEALTHY)
        self.assertIsInstance(result, dict)
        self.assertTrue('status' in result)

    def test_add_lambda_check(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.service.add_check("Lambda test", lambda: HealthCheckResult.healthy("test success"), ["lambda_test"])

        result = self.service.get_result()
        print(result)

        # self.assertEqual(result["status"], HealthStatus.HEALTHY)
        self.assertIsInstance(result, dict)
        self.assertTrue('status' in result)

    def test_add_multi_checks(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.service.add_check("self", SelfConnectionHealthCheck(self.logger, self.config), [])
        self.service.add_check("mysql", MysqlConnectionHealthCheck(self.logger, self.config), ["db"])
        self.service.add_check("redis", RedisConnectionHealthCheck(self.logger, self.config), ["redis"])
        # self.service.add_check("SQSConnection", SQSConnectionHealthCheck(self.logger, self.config), ["db"])

        #self.assertEqual(len(self.service.entries), 3)

        result = self.service.get_result()
        print(result)

        # self.assertEqual(result["status"], HealthStatus.HEALTHY)
        self.assertIsInstance(result, dict)
        self.assertTrue('status' in result)

    def test_get_response(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.service.add_check("self", SelfConnectionHealthCheck(self.logger, self.config), [])
        self.service.add_check("mysql", MysqlConnectionHealthCheck(self.logger, self.config), ["db"])
        self.service.add_check("redis", RedisConnectionHealthCheck(self.logger, self.config), ["redis"])

        response = self.service.get_response()
        print(response.data)
        self.assertIsNotNone(response.data)


if __name__ == '__main__':
    unittest.main()
