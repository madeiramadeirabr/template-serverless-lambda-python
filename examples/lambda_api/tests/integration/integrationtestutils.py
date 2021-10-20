import logging
import os
import unittest
import warnings

from chalicelib.boot import reset, load_dot_env, load_env
from chalicelib.config import reset as reset_config, get_config


class BaseIntegrationTestCase(unittest.TestCase):
    """
    Classe base para testes de integração
    """

    def setUp(self):
        log_name = 'integration_test'
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
            load_dot_env('integration')
        else:
            load_env('integration')
        self.config = get_config()
