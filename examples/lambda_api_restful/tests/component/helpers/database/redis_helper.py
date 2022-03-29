"""
Redis Helper Module for test resources
Version: 1.0.0
"""
import os

import redis

if __package__:
    current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
else:
    current_path = os.path.abspath(os.path.dirname(__file__))

if not current_path[-1] == '/':
    current_path += '/'


class ConnectionHelper:
    @staticmethod
    def get_dynamodb_local_connection():
        host = 'redis'
        port = '6379'
        test = False
        connection = None
        try:
            connection = redis.Redis(
                host=host,
                port=int(port)
            )
            test = connection.set('connection', 'true')
        except Exception as err:
            # docker
            if host == 'redis':
                # localhost
                host = 'localhost'
                connection = redis.Redis(
                    host=host,
                    port=int(port)
                )
                test = connection.set('connection', 'true')

        return connection


class RedisHelper:

    @staticmethod
    def get_connection():
        """
        :return:
        """
        return ConnectionHelper.get_dynamodb_local_connection()
