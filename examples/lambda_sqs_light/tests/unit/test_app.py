import unittest

from unittest_data_provider import data_provider

import app
from lambda_app.config import get_config
from tests.component.componenttestutils import BaseComponentTestCase
from tests.unit.helpers.aws.sqs_helper import create_chalice_sqs_event
from tests.unit.helpers.events_helper import get_cancelamento_event
from tests.unit.mocks.aws_mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.testutils import get_function_name, BaseUnitTestCase


def get_queue_message():
    event = get_cancelamento_event()
    sqs_event = create_chalice_sqs_event(event)
    return (sqs_event,),


def get_queue_events_samples():
    event = get_cancelamento_event()
    sqs_event = create_chalice_sqs_event(event)

    return (sqs_event,),


class AppTestCase(BaseUnitTestCase):
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        BaseComponentTestCase.setUpClass()
        cls.CONFIG = get_config()
        cls.CONFIG.SQS_ENDPOINT = cls.SQS_LOCALSTACK

    @data_provider(get_queue_message)
    def test_index(self, event):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.logger.info('Event: {}'.format(event))

        response = False
        lambda_context = FakeLambdaContext()
        try:
            response = app.index(event=event, context=lambda_context)
            self.logger.info('Response: {}'.format(response))
        except Exception as err:
            self.logger.error(err)

        self.assertTrue(response)



if __name__ == '__main__':
    unittest.main()
