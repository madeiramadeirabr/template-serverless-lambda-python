import os
import unittest

from unittest_data_provider import data_provider

import app
from lambda_app.config import get_config
from lambda_app.logging import get_logger
from tests import ROOT_DIR
from tests.component.componenttestutils import BaseComponentTestCase
from tests.component.helpers.events.aws.sqs_helper import SQSHelper
from tests.unit.helpers.aws.sqs_helper import create_chalice_sqs_event
from tests.unit.helpers.events_helper import get_cancelamento_event
from tests.unit.mocks.aws_mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.testutils import get_function_name


def get_queue_message():
    queue_url = os.getenv("APP_QUEUE")
    event = SQSHelper.get_message(queue_url)
    return (event,)


def get_queue_events_samples():
    event = get_cancelamento_event()
    sqs_event = create_chalice_sqs_event(event)

    return (sqs_event,),


class AppTestCase(BaseComponentTestCase):
    """

    """
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

            logger.info('Fixture: create sqs queue')

            queue_url = cls.CONFIG.APP_QUEUE
            cls.fixture_sqs(logger, queue_url)

    @classmethod
    def fixture_sqs(cls, logger, queue_url):
        queue_name = SQSHelper.get_queue_name(queue_url)
        deleted = SQSHelper.delete_queue(queue_url)
        if deleted:
            logger.info(f'Deleting queue name: {queue_name}')

        attributes = {'DelaySeconds': '1'}
        result = SQSHelper.create_queue(queue_url, attributes)
        if result is not None:
            logger.info(f'queue {queue_name} created')
        else:
            logger.error(f'queue {queue_name} not created')

        event = get_cancelamento_event()
        message = event['Records'][0]
        if 'body' in message:
            message = message['body']
        # print(message)
        SQSHelper.create_message(message, queue_url)
        logger.info('created message: {}'.format(message))

    @data_provider(get_queue_message)
    def test_index(self, event):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.logger.info('Event: {}'.format(event))

        response = False
        lambda_context = FakeLambdaContext()
        try:
            response = app.index(event=event, context=lambda_context)
        except Exception as err:
            self.logger.error(err)

        self.assertTrue(response)

    @data_provider(get_queue_events_samples)
    def test_cancelamento_event_index(self, event):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.logger.info('Event: {}'.format(event))

        response = False
        lambda_context = FakeLambdaContext()
        try:
            response = app.index(event=event, context=lambda_context)
        except Exception as err:
            self.logger.error(err)

        self.assertTrue(response)


if __name__ == '__main__':
    unittest.main()
