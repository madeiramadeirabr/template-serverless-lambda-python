import os
import unittest

from unittest_data_provider import data_provider

import app
from flambda_app.aws.sqs import SQS
from flambda_app.config import get_config
from flambda_app.logging import get_logger
from flambda_app.repositories.v1.mysql.ocoren_repository import OcorenRepository
from tests.component.helpers.database.mysql_helper import MySQLHelper
from tests.integration.integrationtestutils import BaseIntegrationTestCase
from tests.unit.helpers.aws.sqs_helper import create_chalice_sqs_event
from tests.unit.helpers.events_helper import get_cancelamento_event
from tests.unit.mocks.aws_mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.testutils import get_function_name


def get_queue_message():
    queue_url = os.getenv("APP_QUEUE")
    sqs = SQS(config=None, profile=None, session=None)
    # force None to connect to staging
    sqs.endpoint_url = None
    event = sqs.get_message(queue_url)
    return (event,)


def get_queue_events_samples():
    event = get_cancelamento_event()
    # delivery_event = get_delivery_time_simulator_event_sample()
    sqs_event = create_chalice_sqs_event(event)

    return (sqs_event,),

class AppTestCase(BaseIntegrationTestCase):
    """
    Attention: Do not execute fixture on integration tests
    """
    EXECUTE_FIXTURE = True
    CONFIG = None

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
    def test_index_with_samples(self, event):
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
