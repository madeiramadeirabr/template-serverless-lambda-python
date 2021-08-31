import logging
import os
import unittest
import warnings

from lambda_app.boot import reset, load_dot_env, load_env
from lambda_app.config import reset as reset_config, get_config


class BaseComponentTestCase(unittest.TestCase):
    SQS_LOCALSTACK = 'http://localhost:4566'
    REDIS_LOCALSTACK = 'localhost'
    CONFIG = None

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


    """
    Classe base para testes de componentes
    """

    def setUp(self):
        log_name = 'component_test'
        log_filename = None
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=logging.DEBUG)
        self.logger = logging.getLogger(log_name)

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
