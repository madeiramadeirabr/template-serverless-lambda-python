from lambda_app.logging import get_logger


class ProductManager:
    def __init__(self, logger=None, product_service=None):
        self.logger = logger if logger is not None else get_logger()

    def list(self):
        pass

    def get(self):
        pass

    def create(self):
        pass

    def soft_update(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
