"""
HealthCheck Resources Module Mock for Flambda APP
Version: 1.0.0
"""
from unittest.mock import Mock

from flambda_app.services.v1.healthcheck import HealthCheckResult
from flambda_app.services.v1.healthcheck.resources import SelfConnectionHealthCheck, MysqlConnectionHealthCheck, \
    RedisConnectionHealthCheck, SQSConnectionHealthCheck

self_connection_health_check_mock = Mock(SelfConnectionHealthCheck)
self_connection_health_check_mock.check_health.side_effect = \
    lambda: HealthCheckResult.healthy(description="Connection successful")

mysql_connection_health_check_mock = Mock(MysqlConnectionHealthCheck)
mysql_connection_health_check_mock.check_health.side_effect = \
    lambda: HealthCheckResult.healthy(description="Connection successful")

redis_connection_health_check_mock = Mock(RedisConnectionHealthCheck)
redis_connection_health_check_mock.check_health.side_effect = \
    lambda: HealthCheckResult.healthy(description="Connection successful")

sqs_connection_health_check_mock = Mock(SQSConnectionHealthCheck)
sqs_connection_health_check_mock.check_health.side_effect = \
    lambda: HealthCheckResult.healthy(description="Connection successful")
