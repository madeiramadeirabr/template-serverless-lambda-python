import unittest

from flambda_app.config import get_config
from tests.unit.testutils import BaseUnitTestCase, get_function_name


class ConfigTestCase(BaseUnitTestCase):
    CONFIG = None

    def test_get_config(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        config = get_config()
        config_dict = config.to_dict()

        self.assertTrue(getattr(config, 'APP_NAME'))
        self.logger.info(config.APP_NAME)
        self.assertTrue(getattr(config, 'APP_ENV'))
        self.logger.info(config.APP_ENV)

        self.logger.info(config_dict)


if __name__ == '__main__':
    unittest.main()
