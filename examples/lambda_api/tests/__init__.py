import os
import sys

from boot import load_env, set_root_dir

if __package__:
    current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
else:
    current_path = os.path.abspath(os.path.dirname(__file__))

if not current_path[-1] == '/':
    current_path += '/'

ROOT_DIR = current_path.replace('tests/', '')

_REGISTERED_PATHS = False


def register_paths():
    global _REGISTERED_PATHS
    if not _REGISTERED_PATHS:
        # path fixes, define the priority of the modules search
        sys.path.insert(0, ROOT_DIR)
        sys.path.insert(1, ROOT_DIR + 'chalicelib/')
        sys.path.insert(1, ROOT_DIR + 'flask_app/')
        sys.path.insert(1, ROOT_DIR + 'lambda_app/')
        sys.path.insert(2, ROOT_DIR + 'vendor/')
        _REGISTERED_PATHS = True
    pass


register_paths()

_LOADED = False

set_root_dir(ROOT_DIR)
load_env()
