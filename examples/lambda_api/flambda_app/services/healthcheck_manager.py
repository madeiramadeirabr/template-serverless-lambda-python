"""
HealthCheck Manager for Flambda APP
Version: 1.0.0
"""
from flambda_app.config import get_config
from flambda_app.logging import get_logger
from flambda_app.services.v1.healthcheck import HealthCheckResult
from flambda_app.services.v1.healthcheck.resources import SelfConnectionHealthCheck, MysqlConnectionHealthCheck, \
    RedisConnectionHealthCheck
from flambda_app.services.v1.healthcheck_service import HealthCheckService


class HealthCheckManager:
    def __init__(self, logger=None, config=None, healthcheck_service=None):

        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # service
        self.healthcheck_service = healthcheck_service if healthcheck_service is not None else HealthCheckService(self.logger)

        # exception
        self.exception = None

        # debug
        self.DEBUG = None

    def debug(self, flag: bool = False):
        self.DEBUG = flag
        self.healthcheck_service.debug(self.DEBUG)

    def check(self):
        self.healthcheck_service.add_check("self", SelfConnectionHealthCheck(self.logger, self.config), [])
        self.healthcheck_service.add_check(
            "mysql", MysqlConnectionHealthCheck(self.logger, self.config), ["db"])
        self.healthcheck_service.add_check("redis", RedisConnectionHealthCheck(
            self.logger, self.config), ["redis"])
        self.healthcheck_service.add_check("internal", lambda: HealthCheckResult.healthy("connect"), ["example"])
        # example with a lambda check
        # self.healthcheck_service.add_check("internal", lambda: HealthCheckResult.unhealthy("connect"), ["example"])

        return self.healthcheck_service.get_response()
