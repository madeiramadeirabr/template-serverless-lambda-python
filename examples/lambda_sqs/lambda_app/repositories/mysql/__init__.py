from lambda_app.database.mysql import get_connection
from lambda_app.logging import get_logger
import pymysql


class AbstractRepository:
    def __init__(self, logger, mysql_connection):
        self.logger = logger if logger is not None else get_logger()
        self.connection = mysql_connection if mysql_connection is not None else get_connection()
        self._exception = None
        self.debug = False

    def get_connection(self):
        return self.connection

    def get_exception(self):
        return self._exception

    def _execute(self, sql, params=None):
        if self.debug:
            self.logger.info("SQL: {}".format(sql))
            self.logger.info("SQL Values: {}".format(params))

        # issubclass(connection_mock.__class__, pymysql.connections.Connection)
        if isinstance(self.connection, pymysql.connections.Connection) \
                or issubclass(self.connection.__class__, pymysql.connections.Connection):
            # always connect because is treadsafe
            self.connection.connect()
            # with self.connection.cursor() as cursor:
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql, params)
            except Exception as err:
                self.logger.error(err)
            finally:
                result = cursor
            # close connection only in read
            # self.connection.close()
        else:
            result = self.connection.execute(sql, params)
        return result

    def _close(self):
        self.connection.close()


