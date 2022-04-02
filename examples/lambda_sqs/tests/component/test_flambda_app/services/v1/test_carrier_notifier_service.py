import os
import unittest

from unittest_data_provider import data_provider

from flambda_app import helper
from flambda_app.config import get_config
from flambda_app.database.mysql import MySQLConnector
from flambda_app.logging import get_logger
from flambda_app.repositories.v1.mysql.ocoren_repository import OcorenRepository
from flambda_app.services.v1.carrier_notifier_service import CarrierNotifierService
from tests.component.componenttestutils import BaseComponentTestCase
from tests.component.helpers.aws.sqs_helper import SQSHelper
from tests.unit.helpers.aws.sqs_helper import create_chalice_sqs_event, get_sqs_event_sample
from tests.unit.helpers.events_helper import get_cancelamento_event, get_cancelamento_error_event, \
    get_cancelamento_quote_error_event
from tests.unit.testutils import get_function_name


def get_queue_message():
    queue_url = os.getenv("APP_QUEUE")
    event = SQSHelper.get_message(queue_url)

    return (event,),


def get_queue_events_samples():
    event = get_cancelamento_event()
    sqs_event = create_chalice_sqs_event(event)

    return (sqs_event,),


def get_queue_events_error_samples():
    event = get_cancelamento_error_event()
    qevent = get_cancelamento_quote_error_event()

    return (create_chalice_sqs_event(event),), (create_chalice_sqs_event(qevent),),


class CarrierNotifierServiceTestCase(BaseComponentTestCase):
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

    def setUp(self):
        super().setUp()
        self.connection = MySQLConnector().get_connection()
        self.repository = OcorenRepository(self.logger, self.connection)
        self.service = CarrierNotifierService(self.logger, self.repository)

    @data_provider(get_queue_message)
    def test_process_by_queue(self, sqs_event):
        self.logger.info('Running test: %s', get_function_name(__name__))

        result = self.service.process(sqs_event=sqs_event)

        self.assertTrue(result)

    @data_provider(get_queue_events_samples)
    def test_process_by_events(self, sqs_event):
        self.logger.info('Running test: %s', get_function_name(__name__))

        result = self.service.process(sqs_event=sqs_event)

        self.assertTrue(result)

    @data_provider(get_queue_events_error_samples)
    def test_process_by_error_events(self, sqs_event):
        self.logger.info('Running test: %s', get_function_name(__name__))

        with self.assertRaises(Exception):
            self.service.process(sqs_event=sqs_event)


if __name__ == '__main__':
    unittest.main()
