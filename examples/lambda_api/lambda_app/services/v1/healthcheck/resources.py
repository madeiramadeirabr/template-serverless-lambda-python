import os

import requests

from lambda_app.services.v1.healthcheck import AbstractHealthCheck, HealthCheckResult
from lambda_app.database.mysql import get_connection
from lambda_app.database.redis import get_connection as redis_get_connection
from lambda_app.events.aws.sqs import SQSEvents


class SelfConnectionHealthCheck(AbstractHealthCheck):
    def __init__(self, logger=None, config=None, http_client=None):
        super().__init__(logger=logger, config=config)
        self.http_client = http_client if http_client is not None else requests

    def check_health(self):
        result = False
        description = "Unable to connect"
        check_result = HealthCheckResult.unhealthy(description)
        try:
            result = True
            url = os.environ["API_SERVER"] if "API_SERVER" in os.environ else None
            url = url + "/docs"
            self.logger.info("requesting url: {}".format(url))
            response = self.http_client.get(url)
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
        except Exception as err:
            self.logger.error(err)

        if result:
            check_result = HealthCheckResult.healthy(description)
        return check_result


class MysqlConnectionHealthCheck(AbstractHealthCheck):
    def __init__(self, logger=None, config=None, mysql_connection=None):
        super().__init__(logger=logger, config=config)
        # database connection
        self.mysql_connection = mysql_connection if mysql_connection is not None else get_connection()

    def check_health(self):
        result = False
        description = "Unable to connect"
        check_result = HealthCheckResult.unhealthy(description)

        try:
            if self.mysql_connection:
                self.mysql_connection.connect()
                self.mysql_connection.ping()
                result = True
                description = "Connection successful"
            else:
                raise Exception("mysql_connection is None")
        except Exception as err:
            self.logger.error(err)

        if result:
            check_result = HealthCheckResult.healthy(description)
        return check_result


class RedisConnectionHealthCheck(AbstractHealthCheck):
    def __init__(self, logger=None, config=None, redis_connection=None):
        super().__init__(logger=logger, config=config)
        # database connection
        self.redis_connection = redis_connection if redis_connection is not None else redis_get_connection()

    def check_health(self):
        result = False
        description = "Unable to connect"
        check_result = HealthCheckResult.unhealthy(description)

        try:
            if self.redis_connection:
                result = self.redis_connection.set('connection', 'true')
                description = "Connection successful"
            else:
                raise Exception("redis_connection is None")
        except Exception as err:
            self.logger.error(err)

        if result:
            check_result = HealthCheckResult.healthy(description)
        return check_result


class SQSConnectionHealthCheck(AbstractHealthCheck):
    def __init__(self, logger=None, config=None, sqs_events=None):
        super().__init__(logger=logger, config=config)
        # sqs_events connection
        self.sqs_events = sqs_events if sqs_events is not None else SQSEvents()

    def check_health(self):
        result = False
        description = "Unable to connect"
        check_result = HealthCheckResult.unhealthy(description)

        try:
            if self.sqs_events:
                connection = self.sqs_events.connect()
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
