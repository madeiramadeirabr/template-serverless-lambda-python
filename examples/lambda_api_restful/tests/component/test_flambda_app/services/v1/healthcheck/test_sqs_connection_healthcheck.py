import unittest

from flambda_app.config import get_config
from flambda_app.aws.sqs import SQS
from flambda_app.logging import get_logger
from flambda_app.services.v1.healthcheck import HealthStatus, HealthCheckResult
from flambda_app.services.v1.healthcheck.resources import SQSConnectionHealthCheck
from tests.component.componenttestutils import BaseComponentTestCase
from tests.component.helpers.aws.sqs_helper import SQSHelper
from tests.unit.helpers.aws.sqs_helper import get_sqs_event_sample
from tests.unit.testutils import get_function_name


class SQSConnectionHealthCheckTestCase(BaseComponentTestCase):
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

        event = get_sqs_event_sample()
        message = event['Records'][0]
        SQSHelper.create_message(message, queue_url)
        logger.info('created message: {}'.format(message))

    def setUp(self):
        super().setUp()
        self.config = get_config()
        self.sqs = SQS(logger=self.logger, config=self.config)
        self.service = SQSConnectionHealthCheck(self.logger, self.config, self.sqs)

    def test_check_health(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        result = self.service.check_health()
        self.logger.info(result.to_dict())

        self.assertIsInstance(result, HealthCheckResult)
        self.assertEqual(result.status, HealthStatus.HEALTHY)


if __name__ == '__main__':
    unittest.main()
