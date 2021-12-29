import json
import unittest

import serverless_wsgi

import app
from lambda_app import APP_NAME, APP_VERSION
from lambda_app.config import get_config
from tests.unit.mocks.aws_mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.mocks.lambda_event_mocks.request_event import create_aws_api_gateway_proxy_request_event
from tests.unit.testutils import BaseUnitTestCase, get_function_name


class AppTestCase(BaseUnitTestCase):
    CONFIG = None

    def test_index(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.skipTest("Unable to mock dependencies")
        # event = create_aws_api_gateway_proxy_request_event('GET', '/')
        # context = FakeLambdaContext()
        #
        # response = serverless_wsgi.handle_request(app.app, event, context)
        #
        # self.assertTrue('statusCode' in response)
        # self.assertTrue('body' in response)
        #
        # body = json.loads(response['body'])
        # self.logger.info(body)
        #
        # self.assertTrue('app' in body)
        # self.assertEqual(body['app'], "%s:%s" % (APP_NAME, APP_VERSION))

    def test_alive(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.skipTest("Unable to mock dependencies")

        # event = create_aws_api_gateway_proxy_request_event('GET', '/alive')
        # context = FakeLambdaContext()
        #
        # response = serverless_wsgi.handle_request(app.app, event, context)
        #
        # self.assertTrue('statusCode' in response)
        # self.assertTrue('body' in response)
        #
        # body = json.loads(response['body'])
        # self.logger.info(body)
        #
        # self.assertTrue('status' in body)
        # self.assertTrue('entries' in body)


if __name__ == '__main__':
    unittest.main()
