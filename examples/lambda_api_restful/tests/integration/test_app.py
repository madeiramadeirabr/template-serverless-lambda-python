"""
App Integration Test for Flambda APP
Version: 1.0.0
"""
import json
import os
import unittest

import serverless_wsgi

import app
from flambda_app import APP_NAME, APP_VERSION
from flambda_app.aws.sqs import SQS
from tests.integration.integrationtestutils import BaseIntegrationTestCase
from tests.unit.mocks.aws_mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.mocks.lambda_event_mocks.request_event import create_aws_api_gateway_proxy_request_event
from tests.unit.testutils import get_function_name


def get_queue_message():
    queue_url = os.getenv("APP_QUEUE")
    sqs = SQS(config=None, profile=None, session=None)
    # force None to connect to staging
    sqs.endpoint_url = None
    event = sqs.get_message(queue_url)
    return (event,)


class AppTestCase(BaseIntegrationTestCase):
    """
    Attention: Do not execute fixture on integration tests
    """

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

    def test_alive(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        event = create_aws_api_gateway_proxy_request_event('GET', '/alive')
        context = FakeLambdaContext()

        response = serverless_wsgi.handle_request(app.APP, event, context)

        self.assertTrue('statusCode' in response)
        self.assertTrue('body' in response)

        body = json.loads(response['body'])
        self.logger.info(body)

        self.assertTrue('status' in body)
        self.assertTrue('entries' in body)


if __name__ == '__main__':
    unittest.main()
