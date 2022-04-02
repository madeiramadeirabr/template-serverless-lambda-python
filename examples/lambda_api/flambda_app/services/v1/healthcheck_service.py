"""
HealthCheck Service for Flambda APP
Version: 1.0.0
"""
import datetime

from flambda_app.config import get_config
from flambda_app.logging import get_logger
from flambda_app.services.v1.healthcheck import AbstractHealthCheck, HealthCheckResponse, HealthStatus


class HealthCheckService:
    def __init__(self, logger=None, config=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # checks
        self.entries = []

    def add_check(self, name: str, health_check, tags: list, args: dict = None):
        entry = {
            "name": name,
            "health_check": health_check,
            "tags": tags,
            "args": args
        }
        self.entries.append(entry)

    def get_result(self):

        service_status = HealthStatus.HEALTHY
        total_duration = datetime.timedelta()

        result = {
            "status": service_status,
            "total_duration": total_duration,
            "entries": {}
        }

        for entry in self.entries:
            name = entry["name"]
            health_check = entry["health_check"]
            tags = entry["tags"]
            args = entry["args"]
            status = HealthStatus.UNHEALTHY
            start = datetime.datetime.now()

            try:
                if isinstance(health_check, AbstractHealthCheck):
                    check = health_check.check_health()
                elif callable(health_check):
                    if args and len(args) > 0:
                        check = health_check(**args)
                    else:
                        check = health_check()
                else:
                    check = None
                if check is None or check.status == HealthStatus.UNHEALTHY:
                    status = HealthStatus.UNHEALTHY
                else:
                    status = check.status

            except Exception as err:
                self.logger.error(err)

            end = datetime.datetime.now()
            duration = (end - start)
            total_duration = total_duration.__add__(duration)

            if status != HealthStatus.HEALTHY:
                if service_status == HealthStatus.HEALTHY:
                    service_status = HealthStatus.DEGRADED
                else:
                    service_status = HealthStatus.UNHEALTHY

            result["entries"][name] = {
                "status": status,
                "duration": duration,
                "tags": tags
            }

        # update variables
        result["status"] = service_status
        result["total_duration"] = total_duration
        return result

    def get_response(self):
        result = self.get_result()
        response = HealthCheckResponse()
        response.status = result["status"]
        response.total_duration = result["total_duration"]
        response.set_data(result["entries"])
        return response.get_response()
