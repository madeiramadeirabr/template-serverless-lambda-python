import os
import unittest

from unittest_data_provider import data_provider

from lambda_app import helper
from lambda_app.config import get_config
from lambda_app.database.mysql import get_connection
from lambda_app.logging import get_logger
from lambda_app.repositories.mysql.ocoren_repository import OcorenRepository
from lambda_app.services.v1.carrier_notifier_service import CarrierNotifierService
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
        SQSHelper.create_message(message, queue_url)
        logger.info('created message: {}'.format(message))

    def setUp(self):
        super().setUp()
        self.connection = get_connection()
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
