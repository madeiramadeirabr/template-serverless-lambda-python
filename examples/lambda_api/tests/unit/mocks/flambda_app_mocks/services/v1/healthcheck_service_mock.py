from unittest.mock import Mock

from flambda_app.services.v1.healthcheck import HealthCheckResponse
from flambda_app.services.v1.healthcheck_service import HealthCheckService

healthcheck_service_mock = Mock(HealthCheckService)
healthcheck_service_mock.get_response.side_effect = lambda: HealthCheckResponse().get_response()
