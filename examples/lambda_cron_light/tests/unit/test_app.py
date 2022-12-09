import unittest

from unittest_data_provider import data_provider

import app
from flambda_app.config import get_config
from tests.unit.helpers.events_helper import get_cron_event_sample
from tests.unit.mocks.aws_mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.testutils import get_function_name, BaseUnitTestCase


def get_cron_event():
    cron_event = get_cron_event_sample()
    return (cron_event,),


class AppTestCase(BaseUnitTestCase):
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        BaseUnitTestCase.setUpClass()
        cls.CONFIG = get_config()

    @data_provider(get_cron_event)
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
