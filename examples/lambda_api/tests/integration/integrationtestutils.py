import logging
import os
import unittest
import warnings

from boot import reset, load_dot_env, load_env
from flambda_app.config import reset as reset_config, get_config

_ENV = 'integration'


# Fix to load correctly the environment
def load_integration_env():
    # reset config and env
    reset()
    reset_config()
    # load integration
    APP_TYPE = os.environ['APP_TYPE'] if 'APP_TYPE' in os.environ else None
    if APP_TYPE == 'Flask':
        load_dot_env(env=_ENV)
    else:
        load_env(env=_ENV)


# force the env load
load_integration_env()


class BaseIntegrationTestCase(unittest.TestCase):
    """
    Classe base para testes de integração
    """
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        cls.CONFIG = get_config()

    def setUp(self):
        log_name = 'integration_test'
        log_filename = None
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=logging.DEBUG)
        self.logger = logging.getLogger(log_name)

        # ignora falso positivos
        # https://github.com/boto/boto3/issues/454
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.config = get_config()
