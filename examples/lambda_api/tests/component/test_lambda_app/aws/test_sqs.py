"""
AWS SQS Module Component Test for Flambda APP
Version: 1.0.0
"""
import unittest
from time import sleep

from unittest_data_provider import data_provider

from flambda_app.config import get_config
from flambda_app.aws.sqs import SQS
from flambda_app.logging import get_logger
from tests.component.componenttestutils import BaseComponentTestCase
from tests.component.helpers.aws.sqs_helper import SQSHelper
from tests.unit.helpers.events_helper import get_cancelamento_event
from tests.unit.testutils import get_function_name


def get_sqs_event_sample():
    event = get_cancelamento_event()
    return (event,),


class SQSTestCase(BaseComponentTestCase):
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

            queue_url = cls.CONFIG.get('APP_QUEUE', None)
            cls.fixture_sqs(logger, queue_url)

    def setUp(self):
        super().setUp()
        self.sqs = SQS()

    def test_multi_connection(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        sqs = SQS()
        _conn = None
        _last_conn = None
        for i in range(0, 3):
            self.logger.info('i: {}'.format(i))
            conn = sqs.connect()
            _last_conn = conn
            if i == 0:
                _conn = conn

        self.assertIsNotNone(_conn)
        self.assertEqual(_conn, _last_conn)

    def test_connect(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        connection = self.sqs.connect()
        self.assertIsNotNone(connection)

    #todo revisar pois as vezes está dando problemas
    @data_provider(get_sqs_event_sample)
    def test_send_message(self, message):
        self.logger.info('Running test: %s', get_function_name(__name__))
        queue_url = self.CONFIG.get('APP_QUEUE', None)
        response = self.sqs.send_message(message, queue_url)

        self.logger.info(response)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertTrue('MD5OfMessageBody' in response)
        self.assertTrue('MessageId' in response)


if __name__ == '__main__':
    unittest.main()
