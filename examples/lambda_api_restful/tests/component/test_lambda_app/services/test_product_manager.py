import unittest

from unittest_data_provider import data_provider

from lambda_app.config import get_config
from lambda_app.http_resources.request import ApiRequest
from lambda_app.http_resources.request_control import Pagination, Order
from lambda_app.logging import get_logger
from lambda_app.repositories.v1.mysql.product_repository import ProductRepository
from lambda_app.services.product_manager import ProductManager
from tests import ROOT_DIR
from tests.component.componenttestutils import BaseComponentTestCase
from tests.component.helpers.database.mysql_helper import MySQLHelper
from tests.unit.testutils import get_function_name


def get_list_data():
    where = dict()
    fields = []
    sort_by = None
    order_by = None
    offset = Pagination.OFFSET
    limit = Pagination.LIMIT
    http_method = 'GET'
    host = 'localhost'
    path_base = '/v1/product?limit={}&offset={}'
    path = path_base.format(limit, offset)

    return (ApiRequest.factory(http_method, host, path),), \
           (ApiRequest.factory(http_method, host, path+"&fields=id,name"),),
    #        (where, offset, limit, ['id', 'name'], sort_by, order_by), \
    #        (where, offset, limit, ['id', 'name'], sort_by, Order.DESC), \
    #        ({'uuid': 'fecfddd9-7cb8-413b-9de3-ec86de30a888'}, offset, limit, ['id', 'name'], sort_by, Order.DESC),


class ProductManagerTestCase(BaseComponentTestCase):
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

    def setUp(self):
        super(ProductManagerTestCase, self).setUp()
        self.config = get_config()
        self.manager = ProductManager(logger=self.logger, config=self.config)
        self.manager.debug(True)

    @data_provider(get_list_data)
    def test_list(self, api_request):
        self.logger.info('Running test: %s', get_function_name(__name__))

        result = self.manager.list(api_request)
        self.logger.info(result)
        self.assertIsInstance(result, list)

    @data_provider(get_list_data)
    def test_count(self, api_request):
        self.logger.info('Running test: %s', get_function_name(__name__))

        result = self.manager.count(api_request)
        self.logger.info(result)
        self.assertIsInstance(result, int)


if __name__ == '__main__':
    unittest.main()
