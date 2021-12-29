import unittest

from lambda_app.config import get_config
from lambda_app.services.v1.healthcheck import HealthStatus, HealthCheckResult
from lambda_app.services.v1.healthcheck.resources import RedisConnectionHealthCheck
from tests.unit.mocks.database.redis_mock import get_connection
from tests.unit.testutils import get_function_name, BaseUnitTestCase


class RedisConnectionHealthCheckTestCase(BaseUnitTestCase):
    EXECUTE_FIXTURE = True
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        BaseUnitTestCase.setUpClass()
        cls.CONFIG = get_config()

    def setUp(self):
        super().setUp()
        self.connection = get_connection()
        self.config = get_config()
        self.service = RedisConnectionHealthCheck(self.logger, self.config, self.connection)

    def test_check_health(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        result = self.service.check_health()

        self.assertIsInstance(result, HealthCheckResult)
        self.assertEqual(result.status, HealthStatus.HEALTHY)


if __name__ == '__main__':
    unittest.main()
