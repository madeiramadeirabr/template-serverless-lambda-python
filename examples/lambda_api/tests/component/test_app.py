import os
import unittest

import serverless_wsgi

from unittest_data_provider import data_provider
from lambda_app import APP_NAME, APP_VERSION
from lambda_app.repositories.mysql.product_repository import ProductRepository
from tests import ROOT_DIR
from tests.component.componenttestutils import BaseComponentTestCase
from lambda_app.config import get_config
from lambda_app.logging import get_logger

from tests.component.helpers.database.mysql_helper import MySQLHelper
from tests.component.helpers.events.aws.sqs_helper import SQSHelper
from tests.unit.helpers.aws.sqs_helper import get_sqs_event_sample
from tests.unit.mocks.aws_mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.mocks.lambda_event_mocks.request_event import create_aws_api_gateway_proxy_request_event
from tests.unit.testutils import get_function_name
import app
import json


def get_queue_message():
    queue_url = os.getenv("APP_QUEUE")
    event = SQSHelper.get_message(queue_url)
    return (event,)


class AppTestCase(BaseComponentTestCase):
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

            logger.info("Fixture: MYSQL Database connection")
            logger.info("Fixture: drop table")

            mysql_connection = MySQLHelper.get_connection()
            table_name = ProductRepository.BASE_TABLE
            cls.fixture_table(logger, mysql_connection, table_name)

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

    @classmethod
    def fixture_table(cls, logger, mysql_connection, table_name):
        dropped = MySQLHelper.drop_table(mysql_connection, table_name)
        if dropped:
            logger.info(f"Table dropped:: {table_name}")
        file_name = ROOT_DIR + f"tests/datasets/database/structure/mysql/create.table.store.{table_name}.sql"
        created = MySQLHelper.create_table(mysql_connection, table_name, file_name)
        if created:
            logger.info(f"Table created:: {table_name}")
        file_name = ROOT_DIR + f"tests/datasets/database/seeders/mysql/seeder.table.store.{table_name}.sql"
        populated = MySQLHelper.sow_table(mysql_connection, table_name, file_name)
        if populated:
            logger.info(f"Table populated:: {table_name}")

    def test_index(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        event = create_aws_api_gateway_proxy_request_event('GET', '/')
        context = FakeLambdaContext()

        response = serverless_wsgi.handle_request(app.APP, event, context)

        self.assertTrue('statusCode' in response)
        self.assertTrue('body' in response)

        body = json.loads(response['body'])
        self.logger.info(body)

        self.assertTrue('app' in body)
        self.assertEqual(body['app'], "%s:%s" % (APP_NAME, APP_VERSION))

    def test_alive(self):
        self.logger.info('Running test: %s', get_function_name(__name__))

        event = create_aws_api_gateway_proxy_request_event('GET', '/alive')
        context = FakeLambdaContext()

        response = serverless_wsgi.handle_request(app.APP, event, context)

        self.assertTrue('statusCode' in response)
        self.assertTrue('body' in response)

        body = json.loads(response['body'])
        self.logger.info(body)

        self.assertTrue('status' in body)
        self.assertTrue('entries' in body)


if __name__ == '__main__':
    unittest.main()
