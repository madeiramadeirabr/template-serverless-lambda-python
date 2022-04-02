"""
MySQL HealthCheck Service Unit Test for Flambda APP
Version: 1.0.0
"""
import unittest

from flambda_app.config import get_config
from flambda_app.services.v1.healthcheck import HealthStatus, HealthCheckResult
from flambda_app.services.v1.healthcheck.resources import MysqlConnectionHealthCheck
from tests.unit.mocks.database_mocks.mysql_mock import mysql_connector_mock
from tests.unit.testutils import get_function_name, BaseUnitTestCase


class MysqlConnectionHealthCheckTestCase(BaseUnitTestCase):
    EXECUTE_FIXTURE = True
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        BaseUnitTestCase.setUpClass()
        cls.CONFIG = get_config()

    def setUp(self):
        super().setUp()
        self.connector = mysql_connector_mock
        self.config = get_config()
        self.service = MysqlConnectionHealthCheck(self.logger, self.config, self.connector)

    def test_check_health(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        result = self.service.check_health()

        self.assertIsInstance(result, HealthCheckResult)
        self.assertEqual(HealthStatus.HEALTHY, result.status)


if __name__ == '__main__':
    unittest.main()
