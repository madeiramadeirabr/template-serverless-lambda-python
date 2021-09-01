import sys
import re
import os
import logging

os.environ["LOG_LEVEL"] = logging.getLevelName(logging.INFO)

if __package__:
    current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
else:
    current_path = os.path.abspath(os.path.dirname(__file__))

if not current_path[-1] == '/':
    current_path += '/'

ROOT_DIR = current_path.replace('scripts/migrations/mysql/', '')

_REGISTERED_PATHS = False


def register_paths():
    global _REGISTERED_PATHS
    if not _REGISTERED_PATHS:
        # path fixes, define the priority of the modules search
        sys.path.insert(0, ROOT_DIR)
        sys.path.insert(0, ROOT_DIR + 'venv/')
        sys.path.insert(1, ROOT_DIR + 'chalicelib/')
        sys.path.insert(1, ROOT_DIR + 'flask_app/')
        sys.path.insert(1, ROOT_DIR + 'lambda_app/')
        sys.path.insert(2, ROOT_DIR + 'vendor/')
        _REGISTERED_PATHS = True
    pass


# register the paths
register_paths()

from lambda_app.logging import get_logger
from lambda_app.boot import reset, load_dot_env, load_env
from lambda_app.config import reset as reset_config, get_config
from tests.component.helpers.database.mysql_helper import MySQLHelper

logger = get_logger()
logger.info("ROOT_DIR " + ROOT_DIR)

command = None
sql_file = None
try:
    sql_file = sys.argv[1]
except IndexError as err:
    logger.error(err)
    exit('Filename required')

try:
    logger.info("Load configuration")
    # reset config and env
    reset()
    reset_config()
    # load integration
    APP_TYPE = os.environ['APP_TYPE']
    if APP_TYPE == 'Flask':
        load_dot_env()
    else:
        load_env()
    config = get_config()
except IndexError as err:
    logger.error(err)
    exit('Filename required')


class Command:
    CREATE_TABLE = 'CREATE_TABLE'
    INSERT_INTO = 'INSERT_INTO'


def get_commnad(line):
    command = None
    if "CREATE TABLE" in line:
        command = Command.CREATE_TABLE
    if "INSERT INTO" in line:
        command = Command.INSERT_INTO
    return command


def get_table_name(content, only_table=False):
    table_name = None
    rx = re.search("CREATE TABLE (IF NOT EXISTS )?([\w.]+)", content)
    if not rx:
        rx = re.search("INSERT INTO ([\w.]+)", content)
    if rx:
        groups = rx.groups()
        if len(groups) > 0:
            table_name = groups[len(groups)-1]

        if table_name and only_table:
            table_name_parts = table_name.split('.')
            table_name = table_name_parts[len(table_name_parts)-1]
    return table_name


try:
    connection = MySQLHelper.get_connection()
    with open(ROOT_DIR + sql_file, 'r') as f:
        content = f.read()
        f.close()

    command = get_commnad(content)
    file_name = ROOT_DIR + sql_file
    if command == Command.CREATE_TABLE:
        table_name = get_table_name(content)
        created = MySQLHelper.create_table(connection, table_name, file_name)
        if created is not False:
            logger.info("Table created")
    if command == Command.INSERT_INTO:
        table_name = get_table_name(content)
        sow = MySQLHelper.sow_table(connection, table_name, file_name)
        if sow is not False:
            logger.info("Table sow")


except Exception as err:
    logger.error(err)
    exit('File not found')
