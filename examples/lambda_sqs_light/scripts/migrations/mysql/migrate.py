"""
MySQL Migrate Script Tool
Version: 1.0.0
"""
import logging
import os
import re
import sys
import pymysql

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
        sys.path.insert(1, ROOT_DIR + 'flambda_app/')
        sys.path.insert(2, ROOT_DIR + 'vendor/')
        _REGISTERED_PATHS = True
    pass


def get_internal_logger():
    from flambda_app.logging import get_console_logger
    return get_console_logger()


def get_command(line):
    sql_command = None
    if "CREATE TABLE" in line:
        sql_command = Command.CREATE_TABLE
    if "INSERT INTO" in line:
        sql_command = Command.INSERT_INTO
    return sql_command


def get_table_name(content, only_table=False):
    table_name = None
    rx = re.search("CREATE TABLE (IF NOT EXISTS )?([\\w.]+)", content)
    if not rx:
        rx = re.search("INSERT INTO ([\\w.]+)", content)
    if rx:
        groups = rx.groups()
        if len(groups) > 0:
            table_name = groups[len(groups) - 1]

        if table_name and only_table:
            table_name_parts = table_name.split('.')
            table_name = table_name_parts[len(table_name_parts) - 1]
    return table_name


# register the paths
register_paths()

logger = get_internal_logger()
logger.info("ROOT_DIR " + ROOT_DIR)

if __package__:
    current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
else:
    current_path = os.path.abspath(os.path.dirname(__file__))

if not current_path[-1] == '/':
    current_path += '/'


class Command:
    CREATE_TABLE = 'CREATE_TABLE'
    INSERT_INTO = 'INSERT_INTO'


class ConnectionHelper:
    @staticmethod
    def get_mysql_local_connection():
        from flambda_app.config import get_config
        project_config = get_config()

        params = {
            'host': project_config.DB_HOST,
            'user': project_config.DB_USER,
            'password': project_config.DB_PASSWORD,
            'db': project_config.DB
        }

        mysql_connection = pymysql.connect(host=params['host'],
                                           user=params['user'],
                                           password=params['password'],
                                           database=params['db'],
                                           cursorclass=pymysql.cursors.DictCursor)
        mysql_connection.connect()
        return mysql_connection


class MySQLHelper:

    @staticmethod
    def get_connection():
        """
        :return:
        """
        return ConnectionHelper.get_mysql_local_connection()

    @staticmethod
    def drop_table(connection, table_name):
        result = True
        try:
            # connection = MySQLHelper.get_connection()
            connection.connect()

            content = "DROP TABLE IF EXISTS " + table_name
            print(f"Deleting {table_name}...")
            with connection.cursor() as cursor:
                cursor.execute(content)
                print(f"{table_name} deleted")

        except Exception as err:
            print(f"{table_name} not exists")
        try:
            connection.close()
        except Exception as err:
            pass
        return result

    @staticmethod
    def sow_table(connection, table_name, file_name):
        result = False
        cnt = 0
        seeder_file = None
        try:
            connection.connect()
            seeder_file = open(file_name, 'r')
            line = seeder_file.readline().strip().replace(';', '')
            cnt = 0
            try:
                while line:
                    cnt += 1
                    with connection.cursor() as cursor:
                        if line != '':
                            cursor.execute(line, )
                    line = seeder_file.readline().strip().replace(';', '')

                connection.commit()
                result = True
            except Exception as ex:
                result = False
                connection.rollback()
                print(ex)
        except Exception as ex:
            result = False
            print(ex)
        finally:
            if seeder_file is not None:
                seeder_file.close()

        print("Total of rows affected: %d" % cnt)
        try:
            connection.close()
        except Exception as err:
            pass
        return result

    @staticmethod
    def create_table(connection, table_name, file_name):
        result = False

        connection.connect()
        try:
            sql = 'SELECT table_name FROM information_schema.tables WHERE table_schema = %s'
            with connection.cursor() as cursor:
                cursor.execute(sql, (table_name,))
                table_exists = cursor.fetchone()
        except Exception as err:
            table_exists = False

        if not table_exists:
            sql_file = open(file_name, 'r')
            create_table = sql_file.read()
            sql_file.close()

            try:
                with connection.cursor() as cursor:
                    result = cursor.execute(create_table)
                    print(f"Creating {table_name}...")
            except Exception as err:
                result = False
                print(f"Not created {table_name}...")
        else:
            print(f'Table {table_name} already exists')
        try:
            connection.close()
        except Exception as err:
            pass
        return result


command = None
sql_file = None
try:
    sql_file = sys.argv[1]
except IndexError as err:
    logger.error(err)
    exit('Filename required')

try:
    from boot import reset, load_dot_env, load_env
    from flambda_app.config import reset as reset_config, get_config

    logger.info("Load configuration")
    # reset config and env
    reset()
    reset_config()
    # load integration
    APP_TYPE = os.environ['APP_TYPE'] if 'APP_TYPE' in os.environ else 'Flask'
    if APP_TYPE == 'Flask':
        load_dot_env()
    else:
        load_env()
    config = get_config()
except IndexError as err:
    logger.error(err)
    exit('Filename required')


try:
    connection = MySQLHelper.get_connection()
    with open(ROOT_DIR + sql_file, 'r') as f:
        content = f.read()
        f.close()

    command = get_command(content)
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
