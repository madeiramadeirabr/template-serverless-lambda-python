"""
HealthCheck Resources Module for Flambda APP
Version: 1.0.0
"""
import os

import requests

from boot import get_environment
from flambda_app.services.v1.healthcheck import AbstractHealthCheck, HealthCheckResult
from flambda_app.database.mysql import MySQLConnector
from flambda_app.database.redis import RedisConnector
from flambda_app.aws.sqs import SQS


class SelfConnectionHealthCheck(AbstractHealthCheck):
    def __init__(self, logger=None, config=None, http_client=None):
        super().__init__(logger=logger, config=config)
        self.http_client = http_client if http_client is not None else requests

    def check_health(self):
        result = False
        description = "Unable to connect"
        check_result = HealthCheckResult.unhealthy(description)
        # para o ambiente docker implementar uma verificação compativel
        if get_environment() == "development":
            result = True
            #     # retry for docker
            #     url = "http://0.0.0.0:5000"
            #     url = url + "/docs"
            #     check_result, description, result = self.do_request(check_result, description, result, url)
            # else:
            #     description = "internal error"
            #     check_result = HealthCheckResult.degraded(description)
        else:
            try:
                result = True
                # todo migrar para usar self.config e adicionar API_PORT
                url = os.environ["API_SERVER"] if "API_SERVER" in os.environ else "http://0.0.0.0:5000"
                url = url + "/docs"
                try:
                    check_result, description, result = self.do_request(check_result, description, result, url)
                except Exception as err:
                    self.logger.error(err)
                    result = False

            except Exception as err:
                self.logger.error(err)
                description = "internal error"
                check_result = HealthCheckResult.degraded(description)

        if result:
            check_result = HealthCheckResult.healthy(description)
        return check_result

    def do_request(self, check_result, description, result, url):
        self.logger.info("requesting url: {}".format(url))
        response = self.http_client.get(url, timeout=2)
        if response:
            if response.status_code == 200:
                result = True
                description = "Connection successful"
            else:
                result = False
                description = "Something wrong"
                check_result = HealthCheckResult.degraded(description)
        else:
            raise Exception("Unable to connect")
        return check_result, description, result


class MysqlConnectionHealthCheck(AbstractHealthCheck):
    def __init__(self, logger=None, config=None, mysql_connector=None):
        super().__init__(logger=logger, config=config)
        # database connection
        self.mysql_connector = mysql_connector if mysql_connector is not None else MySQLConnector()

    def check_health(self):
        result = False
        description = "Unable to connect"
        check_result = HealthCheckResult.unhealthy(description)

        try:
            if self.mysql_connector:
                connection = self.mysql_connector.get_connection()
                connection.connect()
                connection.ping()
                result = True
                description = "Connection successful"
            else:
                raise Exception("mysql_connector is None")
        except Exception as err:
            self.logger.error(err)

        if result:
            check_result = HealthCheckResult.healthy(description)
        return check_result


class RedisConnectionHealthCheck(AbstractHealthCheck):
    def __init__(self, logger=None, config=None, redis_connector=None):
        super().__init__(logger=logger, config=config)
        # database connection
        self.redis_connector = redis_connector if redis_connector is not None else RedisConnector()

    def check_health(self):
        result = False
        description = "Unable to connect"
        check_result = HealthCheckResult.unhealthy(description)

        try:
            if self.redis_connector:
                redis_connection = self.redis_connector.get_connection()
                result = redis_connection.set('connection', 'true')
                description = "Connection successful"
            else:
                raise Exception("redis_connection is None")
        except Exception as err:
            self.logger.error(err)

        if result:
            check_result = HealthCheckResult.healthy(description)
        return check_result


class SQSConnectionHealthCheck(AbstractHealthCheck):
    def __init__(self, logger=None, config=None, sqs=None):
        super().__init__(logger=logger, config=config)
        # sqs connection
        self.sqs = sqs if sqs is not None else SQS()

    def check_health(self):
        result = False
        description = "Unable to connect"
        check_result = HealthCheckResult.unhealthy(description)

        try:
            if self.sqs:
                connection = self.sqs.connect()
                if connection:
                    result = True
                    description = "Connection successful"
            else:
                raise Exception("redis_connection is None")
        except Exception as err:
            self.logger.error(err)

        if result:
            check_result = HealthCheckResult.healthy(description)
        return check_result
