import json
import os
import boto3

from os import path

from flambda_app.database.mysql import MySQLConnector
from tests import ROOT_DIR

if __package__:
    current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
else:
    current_path = os.path.abspath(os.path.dirname(__file__))

if not current_path[-1] == '/':
    current_path += '/'


class ConnectionHelper:
    @staticmethod
    def get_mysql_local_connection():
        return MySQLConnector().get_connection()


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
                            cursor.execute(line,)
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
        if connection:
            try:
                connection.connect()
            except Exception as err:
                pass

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
        else:
            print("Invalid connection")
        return result
