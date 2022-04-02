"""
HealthCheck Manager Mock for Flambda APP
Version: 1.0.0
"""
from unittest.mock import Mock

from flambda_app.config import get_config
from flambda_app.logging import get_logger
from flambda_app.services.healthcheck_manager import HealthCheckManager
from tests.unit.mocks.flambda_app_mocks.services.v1.healthcheck_service_mock import healthcheck_service_mock

logger = get_logger()
config = get_config()

health_check_manager_mock = Mock(HealthCheckManager)
health_check_manager = HealthCheckManager(logger=logger, config=config, healthcheck_service=healthcheck_service_mock)


def health_check_manager_caller():
    return health_check_manager
