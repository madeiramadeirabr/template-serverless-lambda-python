import logging
import random
import string
import traceback
import unittest


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def get_function_name(class_name=""):
    fn_name = class_name + "::" + traceback.extract_stack(None, 2)[0][2]
    if not class_name:
        fn_name = traceback.extract_stack(None, 2)[0][2]
    return fn_name


class BaseUnitTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    """
    Classe base para testes de unidade
    """

    def setUp(self):
        log_name = 'unit_test'
        log_filename = None
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=logging.DEBUG)
        self.logger = logging.getLogger(log_name)