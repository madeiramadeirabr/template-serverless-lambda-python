"""
Product Helper module for test resources
Version: 1.0.0
"""
import json
from os import path

from tests import ROOT_DIR


def get_product_sample():
    """

    :return: dict
    """
    with open(path.join(ROOT_DIR, 'tests/datasources/products/sample.json')) as f:
        product_str = f.read()
    try:
        product_dict = json.loads(product_str)
        return product_dict
    except Exception as err:
        print(err)
        raise Exception('Invalid JSON')
