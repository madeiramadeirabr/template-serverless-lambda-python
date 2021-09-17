import os
import unittest

from tests.component.componenttestutils import BaseComponentTestCase
from unittest_data_provider import data_provider
from flask_app.config import get_config
from flask_app.logging import get_logger
from tests.component.helpers.events.aws.sqs_helper import SQSHelper
from tests.unit.helpers.aws.sqs_helper import get_sqs_event_sample
from tests.unit.mocks.aws_mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.testutils import get_function_name
import app
import json


def get_queue_message():
    queue_url = os.getenv("APP_QUEUE")
    event = SQSHelper.get_message(queue_url)
    return (event,)


class AppTestCase(BaseComponentTestCase):
    EXECUTE_FIXTURE = True
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        cls.CONFIG = get_config()
        cls.CONFIG.SQS_ENDPOINT = cls.SQS_LOCALSTACK

        # fixture
        if cls.EXECUTE_FIXTURE:
            logger = get_logger()
            logger.info('Fixture: create sqs queue')

    #         queue_url = cls.CONFIG.APP_QUEUE
    #         cls.fixture_sqs(logger, queue_url)
    #
    # @classmethod
    # def fixture_sqs(cls, logger, queue_url):
    #     queue_name = SQSHelper.get_queue_name(queue_url)
    #     deleted = SQSHelper.delete_queue(queue_url)
    #     if deleted:
    #         logger.info(f'Deleting queue name: {queue_name}')
    #
    #     attributes = {'DelaySeconds': '1'}
    #     result = SQSHelper.create_queue(queue_url, attributes)
    #     if result is not None:
    #         logger.info(f'queue {queue_name} created')
    #     else:
    #         logger.error(f'queue {queue_name} not created')
    #
    #     event = get_sqs_event_sample()
    #     message = event['Records'][0]
    #     SQSHelper.create_message(message, queue_url)
    #     logger.info('created message: {}'.format(message))
    #
    # @data_provider(get_queue_message)
    # def test_sqs_handler(self, event):
    #     self.logger.info('Running test: %s', get_function_name(__name__))
    #     self.logger.info('Event: {}'.format(event))
    #
    #     lambda_context = FakeLambdaContext()
    #     try:
    #         response = app.sqs_handler(event=event, context=lambda_context)
    #     except Exception as err:
    #         self.logger.error(err)
    #     # response = app.sqs_handler(event=event)
    #
    #     self.assertTrue(response)


if __name__ == '__main__':
    unittest.main()
