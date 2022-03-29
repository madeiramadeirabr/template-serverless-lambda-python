"""
Redis Product Repository Unit Test for Flambda APP
Version: 1.0.0
"""
import unittest

from unittest_data_provider import data_provider

from flambda_app.config import get_config
from flambda_app.request_control import Pagination
from flambda_app.repositories.v1.redis.product_repository import ProductRepository
from flambda_app.vos.product import ProductVO
from tests.unit.helpers.product_helper import get_product_sample
from tests.unit.mocks.database_mocks.redis_mock import get_connection
from tests.unit.testutils import get_function_name, BaseUnitTestCase


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

def get_product():
    product_dict = get_product_sample()
    product = ProductVO(product_dict)
    return (product,),


def get_list_data():
    where = "{}:*".format('product')
    offset = Pagination.OFFSET
    limit = Pagination.LIMIT

    return (where, offset, limit),


class ProductRepositoryTestCase(BaseUnitTestCase):
    EXECUTE_FIXTURE = True
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        BaseUnitTestCase.setUpClass()
        cls.CONFIG = get_config()

    def setUp(self):
        super().setUp()

    @data_provider(get_product)
    def test_create(self, product: ProductVO):
        self.logger.info('Running test: %s', get_function_name(__name__))

        key = '%s:%s' % ('product', product.uuid)
        self.logger.info('key: {}'.format(key))

        config = get_config()
        connection = get_connection(config)

        repository = ProductRepository(redis_connection=connection)
        result = repository.create(key, product.to_json())
        self.assertTrue(result)
        self.logger.info('Product created: {}'.format(key))

    @data_provider(get_product)
    def test_get(self, product: ProductVO):
        self.logger.info('Running test: %s', get_function_name(__name__))

        # change the values to create a new one
        product.name = product.name + ' V2'
        # valor para facilitar a tarefa do fixture
        product.uuid = "8374b976-a74e-475c-b78c-39717468926c"

        key = '%s:%s' % ('product', product.uuid)
        self.logger.info('key: {}'.format(key))

        config = get_config()
        connection = get_connection(config)

        repository = ProductRepository(redis_connection=connection)
        result = repository.create(key, product.to_json())

        response = repository.get(key)

        self.assertTrue(result)
        self.assertIsNotNone(response)
        self.logger.info('Product found: {}'.format(key))

    @data_provider(get_list_data)
    def test_list(self, where, offset, limit):
        self.logger.info('Running test: %s', get_function_name(__name__))

        config = get_config()
        connection = get_connection(config)

        repository = ProductRepository(redis_connection=connection)

        result = repository.list(where=where, offset=offset, limit=limit)
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)

        self.logger.info('Product list count: {}'.format(len(result)))

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


if __name__ == '__main__':
    unittest.main()
