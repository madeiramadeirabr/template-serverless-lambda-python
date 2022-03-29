"""
OpenApi Generator Script Tool
Version: 1.0.0
"""
import sys
import os
import logging

os.environ["LOG_LEVEL"] = logging.getLevelName(logging.INFO)

if __package__:
    current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
else:
    current_path = os.path.abspath(os.path.dirname(__file__))

if not current_path[-1] == '/':
    current_path += '/'

ROOT_DIR = current_path.replace('scripts/openapi/', '')
# print(ROOT_DIR)
_REGISTERED_PATHS = False


def register_paths():
    global _REGISTERED_PATHS
    if not _REGISTERED_PATHS:
        # path fixes, define the priority of the modules search
        sys.path.insert(0, ROOT_DIR)
        sys.path.insert(0, ROOT_DIR + 'venv/')
        sys.path.insert(1, ROOT_DIR + 'chalicelib/')
        sys.path.insert(1, ROOT_DIR + 'flask_app/')
        sys.path.insert(1, ROOT_DIR + 'flambda_app/')
        sys.path.insert(2, ROOT_DIR + 'vendor/')
        _REGISTERED_PATHS = True
    pass


def load_env():
    from boot import load_env
    from flambda_app.helper import get_environment
    load_env(get_environment())


def openapi():
    from flambda_app.openapi import generate_openapi_yml
    from app import spec
    from flambda_app.logging import get_console_logger
    LOGGER = get_console_logger()

    generate_openapi_yml(spec, LOGGER, force=True)


# register the paths
register_paths()

# load env
load_env()
# create openapi.yml
openapi()
