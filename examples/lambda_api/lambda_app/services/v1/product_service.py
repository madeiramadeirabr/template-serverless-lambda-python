import json

from lambda_app import helper
from lambda_app.enums import messages
from lambda_app.enums.messages import MessagesEnum
from lambda_app.exceptions import DatabaseException
from lambda_app.http_resources.request import ApiRequest
from lambda_app.logging import get_logger
from lambda_app.repositories.v1.mysql.product_repository import ProductRepository
from lambda_app.repositories.v1.redis.product_repository import ProductRepository as RedisProductRepository
from lambda_app.database.mysql import get_connection as mysql_get_connection
from lambda_app.database.redis import get_connection as redis_get_connection


class ProductService:
    DEBUG = False
    REDIS_ENABLED = False

    def __init__(self, logger=None, mysql_connection=None, redis_connection=None, product_repository=None,
                 redis_product_repository=None):
        # logger
        self.logger = logger if logger is None else get_logger()
        # database connection
        self.mysql_connection = mysql_connection if mysql_connection is not None else mysql_get_connection()
        # mysql repository
        self.product_repository = product_repository if product_repository is not None \
            else ProductRepository(mysql_connection=mysql_connection)

        # exception
        self.exception = None

        if self.REDIS_ENABLED:
            # redis connection
            self.redis_connection = redis_connection if redis_connection is not None else redis_get_connection()
            # redis repository
            self.redis_product_repository = redis_product_repository if redis_product_repository is not None \
                else RedisProductRepository(redis_connection=redis_connection)

        self.debug(self.DEBUG)

    def debug(self, flag: bool = False):
        self.DEBUG = flag
        self.product_repository.debug = self.DEBUG
        if self.REDIS_ENABLED:
            self.redis_product_repository.debug = self.DEBUG

    def list(self, request: ApiRequest):
        self.logger.info('method: {} - request: {}'
                         .format('list', request.to_json()))

        data = []
        where = request.where
        if where == dict():
            where = {
                'active': 1
            }

        try:
            data = self.product_repository.list(
                where=where, offset=request.offset, limit=request.limit, order_by=request.order_by,
                sort_by=request.sort_by, fields=request.fields)

            # set exception if it happens
            if self.product_repository.get_exception():
                raise DatabaseException(MessagesEnum.LIST_ERROR)

        except Exception as err:
            self.logger.error(err)
            self.exception = err

        return data

    def count(self, request: ApiRequest):
        self.logger.info('method: {} - request: {}'
                         .format('count', request.to_json()))

        total = 0
        where = request.where
        if where == dict():
            where = {
                'active': 1
            }

        try:
            total = self.product_repository.count(
                where=where, order_by=request.order_by, sort_by=request.sort_by)
        except Exception as err:
            self.logger.error(err)
            self.exception = DatabaseException(MessagesEnum.LIST_ERROR)

        return total
