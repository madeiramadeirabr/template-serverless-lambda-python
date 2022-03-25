"""
App Unit Test for Flambda APP
Version: 1.0.0
"""
import json
import unittest
from unittest.mock import patch

import serverless_wsgi

import app
from flambda_app import APP_NAME, APP_VERSION
from flambda_app.config import get_config
from tests.unit.mocks.aws_mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.mocks.flambda_app_mocks.services.healthcheck_manager_mock import health_check_manager_caller
from tests.unit.mocks.flambda_app_mocks.services.v1.healthcheck.resources_mock import \
    mysql_connection_health_check_mock, redis_connection_health_check_mock
from tests.unit.mocks.lambda_event_mocks.request_event import create_aws_api_gateway_proxy_request_event
from tests.unit.testutils import BaseUnitTestCase, get_function_name


class AppTestCase(BaseUnitTestCase):
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        BaseUnitTestCase.setUpClass()
        cls.CONFIG = get_config()

    def test_index(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        event = create_aws_api_gateway_proxy_request_event('GET', '/')
        context = FakeLambdaContext()

        response = serverless_wsgi.handle_request(app.APP, event, context)

        self.assertTrue('statusCode' in response)
        self.assertTrue('body' in response)

        body = json.loads(response['body'])
        self.logger.info(body)

        self.assertTrue('app' in body)
        self.assertEqual(body['app'], "%s:%s" % (APP_NAME, APP_VERSION))

    @patch('app.HealthCheckManager', health_check_manager_caller)
    @patch.multiple('flambda_app.services.healthcheck_manager',
                    MysqlConnectionHealthCheck=mysql_connection_health_check_mock,
                    RedisConnectionHealthCheck=redis_connection_health_check_mock
                    )
    def test_alive(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        event = create_aws_api_gateway_proxy_request_event('GET', '/alive')
        context = FakeLambdaContext()

        # utiliza mocks no lugar do objetos reais
        response = serverless_wsgi.handle_request(app.APP, event, context)

        self.assertTrue('statusCode' in response)
        self.assertTrue('body' in response)

        body = json.loads(response['body'])
        self.logger.info(body)

        self.assertTrue('status' in body)
        self.assertTrue('entries' in body)


if __name__ == '__main__':
    unittest.main()
