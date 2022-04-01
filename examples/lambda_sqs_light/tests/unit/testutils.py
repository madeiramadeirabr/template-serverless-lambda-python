"""
Base Unit Test Case for Flambda APP
Version: 1.0.0
"""
import logging
import os
import secrets
import string
import unittest
import warnings

from boot import reset, load_dot_env, load_env
from flambda_app.config import reset as reset_config, get_config
from flambda_app.helper import get_function_name as get_fn


def random_string(string_length=10):
    """Generate a random string of fixed length """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(string_length))


def get_function_name(class_name=""):
    return get_fn(class_name)


class BaseUnitTestCase(unittest.TestCase):
    """
    Classe base para testes de unidade
    """
    CONFIG = None
    LOGGER = None

    @classmethod
    def setUpClass(cls):
        # pass
        # reset config and env
        reset()
        reset_config()
        # load integration
        APP_TYPE = os.environ['APP_TYPE']
        if APP_TYPE == 'Flask':
            load_dot_env()
        else:
            load_env()

        cls.CONFIG = get_config()
        cls.setUpLogger()

    @classmethod
    def setUpLogger(cls):
        log_name = 'unit_test'
        log_filename = None
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=logging.DEBUG)
        cls.LOGGER = logging.getLogger(log_name)

    def setUp(self):
        self.logger = self.LOGGER
        # ignora falso positivos
        # https://github.com/boto/boto3/issues/454
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")

        # reset config and env
        reset()
        reset_config()
        # load integration
        APP_TYPE = os.environ['APP_TYPE']
        if APP_TYPE == 'Flask':
            load_dot_env()
        else:
            load_env()
        self.config = get_config()
