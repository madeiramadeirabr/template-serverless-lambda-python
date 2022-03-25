from flambda_app.config import get_config
from flambda_app.logging import get_logger
from flambda_app.services.v1.product_service import ProductService


class ProductManager:
    def __init__(self, logger=None, config=None, product_service=None):

        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # service
        self.product_service = product_service if product_service is not None else ProductService(self.logger)

        # exception
        self.exception = None

        # debug
        self.DEBUG = None

    def debug(self, flag: bool = False):
        self.DEBUG = flag
        self.product_service.debug(self.DEBUG)

    def list(self, request: dict):
        data = self.product_service.list(request)
        if (data is None or len(data) == 0) and self.product_service.exception:
            self.exception = self.product_service.exception
            raise self.exception
        return data

    def count(self, request: dict):
        total = self.product_service.count(request)
        if self.product_service.exception:
            self.exception = self.product_service.exception
            raise self.exception
        return total

    def get(self, request: dict, uuid):
        data = self.product_service.get(request, uuid)
        if (data is None) and self.product_service.exception:
            self.exception = self.product_service.exception
            raise self.exception
        return data

    def create(self, request: dict):
        data = self.product_service.create(request)
        if (data is None) and self.product_service.exception:
            self.exception = self.product_service.exception
            raise self.exception
        return data

    def soft_update(self, request: dict, uuid):
        data = self.product_service.soft_update(request, uuid)
        if (data is None) and self.product_service.exception:
            self.exception = self.product_service.exception
            raise self.exception
        return data

    def update(self, request: dict, uuid):
        data = self.product_service.update(request, uuid)
        if (data is None) and self.product_service.exception:
            self.exception = self.product_service.exception
            raise self.exception
        return data

    def delete(self, request: dict, uuid):
        result = self.product_service.delete(request, uuid)
        if (result is None) and self.product_service.exception:
            self.exception = self.product_service.exception
            raise self.exception
        return result
