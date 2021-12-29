import json
import unittest
from unittest.mock import Mock, patch

import serverless_wsgi

import app
import lambda_app.database.mysql
from lambda_app import APP_NAME, APP_VERSION
from lambda_app.config import get_config
from lambda_app.services.v1.healthcheck import HealthCheckResponse
from lambda_app.services.v1.healthcheck.resources import MysqlConnectionHealthCheck, RedisConnectionHealthCheck, \
    SQSConnectionHealthCheck
from lambda_app.services.v1.healthcheck_service import HealthCheckService
from tests.unit.mocks.aws_mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.mocks.lambda_event_mocks.request_event import create_aws_api_gateway_proxy_request_event
from tests.unit.testutils import BaseUnitTestCase, get_function_name

service_mock = Mock(HealthCheckService)
service_mock.get_response.side_effect = lambda: HealthCheckResponse().get_response()


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

        response = serverless_wsgi.handle_request(app.app, event, context)

        self.assertTrue('statusCode' in response)
        self.assertTrue('body' in response)

        body = json.loads(response['body'])
        self.logger.info(body)

        self.assertTrue('app' in body)
        self.assertEqual(body['app'], "%s:%s" % (APP_NAME, APP_VERSION))

    # TODO terminar a implmentação dos patchs
    @patch('app.HealthCheckService', return_value=service_mock)
    @patch('app.MysqlConnectionHealthCheck', spec=MysqlConnectionHealthCheck)
    @patch('app.RedisConnectionHealthCheck', spec=RedisConnectionHealthCheck)
    @patch('app.SQSConnectionHealthCheck', spec=SQSConnectionHealthCheck)
    def test_alive(self, sqs_mock, redis_mock, mysql_mock, hc_mock):
        self.logger.info('Running test: %s', get_function_name(__name__))

        event = create_aws_api_gateway_proxy_request_event('GET', '/alive')
        context = FakeLambdaContext()

        response = serverless_wsgi.handle_request(app.app, event, context)

        self.assertTrue('statusCode' in response)
        self.assertTrue('body' in response)

        body = json.loads(response['body'])
        self.logger.info(body)

        self.assertTrue('status' in body)
        self.assertTrue('entries' in body)


if __name__ == '__main__':
    unittest.main()
