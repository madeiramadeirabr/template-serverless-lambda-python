import unittest

from unittest_data_provider import data_provider

from flambda_app.database.mysql import MySQLConnector
from flambda_app.request_control import Pagination, Order
from flambda_app.logging import get_logger
from flambda_app.repositories.v1.mysql.ocoren_repository import OcorenRepository
from flambda_app.vos.ocoren import OcorenVO
from tests import ROOT_DIR
from tests.component.componenttestutils import BaseComponentTestCase
from tests.component.helpers.database.mysql_helper import MySQLHelper
from tests.unit.helpers.ocoren_helper import get_ocoren_cancelamento_sample
from tests.unit.testutils import get_function_name


# def get_request():
#     request = ApiRequest()
#     request.offset = Pagination.OFFSET
#     request.limit = 2
#
#     request.where = {"random": random_string(10)}
#     return (request,),
#
#
# def get_event():
#     request = ApiRequest()
#     request.where = {"random": random_string(10)}
#     event_type = EventType.SALE_EVENT
#     event = EventVO(event_type, request)
#     event.hash = generate_hash(data=event.data)
#     return (event,),

def get_ocoren():
    ocoren_dict = get_ocoren_cancelamento_sample()
    ocoren_dict["id"] = None
    ocoren = OcorenVO(ocoren_dict)

    return (ocoren,),


def get_list_data():
    where = dict()
    offset = Pagination.OFFSET
    limit = Pagination.LIMIT
    fields = []
    sort_by = None
    order_by = None

    return (where, offset, limit, fields, sort_by, order_by), \
           (where, offset, limit, ['id', 'chavenfe'], sort_by, order_by), \
           (where, offset, limit, ['id', 'chavenfe'], sort_by, Order.DESC), \
           ({'chavenfe': '32210206107255000134550010001712551245826554'}, offset, limit,
            ['id', 'chavenfe'], sort_by,
            Order.DESC),


class OcorenRepositoryTestCase(BaseComponentTestCase):
    EXECUTE_FIXTURE = True
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        BaseComponentTestCase.setUpClass()
        mysql_connection = MySQLHelper.get_connection()

        if cls.EXECUTE_FIXTURE:
            logger = get_logger()
            logger.info("Fixture: drop table")

            database_name = "store"
            table_name = OcorenRepository.BASE_TABLE
            cls.fixture_table(logger, mysql_connection, table_name, database_name)


    def setUp(self):
        super().setUp()
        self.connection = MySQLConnector().get_connection()
        self.repository = OcorenRepository(mysql_connection=self.connection)
        self.repository.debug = True

    @data_provider(get_ocoren)
    def test_create(self, ocoren: OcorenVO):
        self.logger.info('Running test: %s', get_function_name(__name__))

        result = self.repository.create(ocoren)
        self.assertTrue(result)
        self.logger.info('Ocoren created: {}'.format(ocoren.id))

    @data_provider(get_ocoren)
    def test_get(self, ocoren: OcorenVO):
        self.logger.info('Running test: %s', get_function_name(__name__))

        # change the values to create a new one
        ocoren.ocor = 'MOTIVO FRAUDE'
        ocoren.chavenfe = '32210206107255000134550010001712551245878995'

        result = self.repository.create(ocoren)

        response = self.repository.get(ocoren.id)

        self.assertTrue(result)
        self.assertIsNotNone(response)

        response = self.repository.get(ocoren.chavenfe, key='chavenfe')
        self.assertIsNotNone(response)

    @data_provider(get_list_data)
    def test_list(self, where, offset, limit, fields, sort_by, order_by):
        self.logger.info('Running test: %s', get_function_name(__name__))

        result = self.repository.list(where, offset, limit, fields, sort_by, order_by)
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)

        self.logger.info('Ocoren list count: {}'.format(len(result)))

    @data_provider(get_list_data)
    def test_count(self, where, offset, limit, fields, sort_by, order_by):
        self.logger.info('Running test: %s', get_function_name(__name__))

        result = self.repository.count(where, sort_by, order_by)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, int)

        self.logger.info('Ocoren list count: {}'.format(result))

    # @data_provider(get_event)
    # def test_delete(self, event: EventVO):
    #     self.logger.info('Running test: %s', get_function_name(__name__))
    #
    #     event_type = event.type
    #     key = '%s:%s' % (event_type, event.hash)
    #
    #     config = get_config()
    #     connection = get_connection(config)
    #
    #     repository = EventRepository(redis_connection=connection)
    #
    #     with self.assertRaises(DatabaseException):
    #         repository.delete(key)
    #
    #     result = repository.create(key, event.to_json())
    #     self.assertTrue(result)
    #
    #     event.data = {**event.data, **{"updated": True}}
    #     result = repository.delete(key)
    #     self.assertTrue(result)
    #
    # @data_provider(get_event)
    # def test_update(self, event: EventVO):
    #     self.logger.info('Running test: %s', get_function_name(__name__))
    #
    #     event_type = event.type
    #     key = '%s:%s' % (event_type, event.hash)
    #
    #     config = get_config()
    #     connection = get_connection(config)
    #
    #     repository = EventRepository(redis_connection=connection)
    #
    #     with self.assertRaises(DatabaseException):
    #         repository.update(key, event.to_json())
    #
    #     result = repository.create(key, event.to_json())
    #     self.assertTrue(result)
    #
    #     event.data = {**event.data, **{"updated": True}}
    #     result = repository.update(key, event.to_json())
    #     self.assertTrue(result)


if __name__=='__main__':
    unittest.main()
