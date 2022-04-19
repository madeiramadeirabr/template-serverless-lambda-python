import os
import time
import unittest
from time import sleep

from flambda_app.repositories.v1.mysql.ocoren_repository import OcorenRepository
from tests import ROOT_DIR
from tests.component.componenttestutils import BaseComponentTestCase
from flambda_app import helper
from unittest_data_provider import data_provider
from flambda_app.config import get_config
from flambda_app.logging import get_logger
from tests.component.helpers.database.mysql_helper import MySQLHelper
from tests.component.helpers.aws.sqs_helper import SQSHelper
from tests.unit.helpers.aws.sqs_helper import get_sqs_event_sample, create_chalice_sqs_event
from tests.unit.helpers.events_helper import get_delivery_time_simulator_event_sample, get_cancelamento_event
from tests.unit.mocks.aws_mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.testutils import get_function_name
import app
import json


def get_queue_message():
    queue_url = os.getenv("APP_QUEUE")

    message = get_cancelamento_event()
    SQSHelper.create_message(message, queue_url)
    time.sleep(1)

    event = SQSHelper.get_message(queue_url)

    return (event,),


def get_queue_events_samples():
    event = get_cancelamento_event()
    # delivery_event = get_delivery_time_simulator_event_sample()
    sqs_event = create_chalice_sqs_event(event)

    return (sqs_event,),


class AppTestCase(BaseComponentTestCase):
    """
    Obs: If you will execute this test, please execute the ./scripts/testenv.sh instead ./scripts/runenv.sh
    """
    EXECUTE_FIXTURE = False
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        BaseComponentTestCase.setUpClass()
        cls.CONFIG = get_config()
        cls.CONFIG.SQS_ENDPOINT = cls.SQS_LOCALSTACK

        # fixture
        if cls.EXECUTE_FIXTURE:
            logger = get_logger()

            logger.info("Fixture: MYSQL Database connection")
            logger.info('Fixture: create sqs queue')

            mysql_connection = MySQLHelper.get_connection()
            database_name='store'
            table_name = OcorenRepository.BASE_TABLE
            cls.fixture_table(logger, mysql_connection, table_name, database_name)

            logger.info('Fixture: create sqs queue')

            queue_url = cls.CONFIG.APP_QUEUE
            cls.fixture_sqs(logger, queue_url)


    @data_provider(get_queue_message)
    def test_index(self, event):
        """
        TODO precisa de ajustes para funcionar
        """
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
