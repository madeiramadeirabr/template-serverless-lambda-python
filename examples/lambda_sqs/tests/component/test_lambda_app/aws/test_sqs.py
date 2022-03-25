import unittest

from unittest_data_provider import data_provider

from flambda_app.aws.sqs import SQSEvents
from flambda_app.config import get_config
from flambda_app.logging import get_logger
from tests.component.componenttestutils import BaseComponentTestCase
from tests.component.helpers.aws.sqs_helper import SQSHelper
from tests.unit.helpers.events_helper import get_cancelamento_event
from tests.unit.testutils import get_function_name


def get_sqs_event_sample():
    event = get_cancelamento_event()
    return (event,),


class SQSEventsTestCase(BaseComponentTestCase):
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

    def test_connect(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        sqs = SQSEvents()
        connection = sqs.connect()
        self.assertIsNotNone(connection)

    @data_provider(get_sqs_event_sample)
    def test_send_message(self, message):
        self.logger.info('Running test: %s', get_function_name(__name__))
        sqs = SQSEvents()
        queue_url = self.CONFIG.APP_QUEUE
        response = sqs.send_message(message, queue_url)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertTrue('MD5OfMessageBody' in response)
        self.assertTrue('MessageId' in response)


if __name__ == '__main__':
    unittest.main()
