import json
from datetime import timedelta

from flambda_app import helper
from flambda_app.config import get_config
from flambda_app.enums import CustomStringEnum
from flambda_app.http_resources.response import ApiResponse
from flambda_app.logging import get_logger
from flask import Response
from marshmallow import Schema, fields


class HealthStatus(CustomStringEnum):
    # all available
    HEALTHY = 'healthy'
    # partial
    DEGRADED = 'degraded'
    # unavailable
    UNHEALTHY = 'unhealthy'


class HealthCheckResult:
    def __init__(self, status, description):
        self.status = status if status is not None and isinstance(status, HealthStatus) else HealthStatus.UNHEALTHY
        self.description = description if description is not None else ""

    @staticmethod
    def healthy(description):
        return HealthCheckResult(HealthStatus.HEALTHY, description)

    @staticmethod
    def unhealthy(description):
        return HealthCheckResult(HealthStatus.UNHEALTHY, description)

    @staticmethod
    def degraded(description):
        return HealthCheckResult(HealthStatus.DEGRADED, description)

    def __str__(self):
        return self.to_dict()

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        return {'status': self.status, 'description': self.description}

    def to_json(self):
        return json.dumps(self.to_dict())


class EntrySchema(Schema):
    status = fields.Str(example=HealthStatus.HEALTHY.value)
    duration = fields.Str(example="0:00:00.013737")
    tags = fields.List(fields.Str(example="db"))


class EntryData(Schema):
    name = fields.Nested(EntrySchema)


class HealthCheckSchema(Schema):
    status = fields.Str(example=HealthStatus.HEALTHY.value)
    total_duration = fields.Str(example="0:00:00.013737")
    entries = fields.Nested(EntryData)


class AbstractHealthCheck:
    def __init__(self, logger=None, config=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()

    def check_health(self):
        return HealthCheckResult.unhealthy("undefined test")


class HealthCheckResponse(ApiResponse):

    def __init__(self, api_request=None):
        super(HealthCheckResponse, self).__init__(api_request)
        self.status_code = 200
        self.status = HealthStatus.HEALTHY
        self.total_duration = timedelta()
        self.duration = timedelta()
        self.entries = {}

    def get_response(self, status_code=None):

        if not status_code:
            if self.status == HealthStatus.UNHEALTHY:
                self.status_code = 503
            elif self.status == HealthStatus.DEGRADED:
                self.status_code = 424
        else:
            self.status_code = status_code

        headers = self.headers

        # # update entries
        # self.entries["self"] = {
        #     "status": self.self_status,
        #     "duration": self.duration,
        #     "tags": []
        # }
        self.entries.update(self.data)

        body = {
            "status": self.status,
            "total_duration": self.total_duration,
            "entries": self.entries
        }

        if 'Content-Type' in headers and headers['Content-Type'] == 'application/json':
            body = helper.to_json(body)
        return Response(response=body, status=self.status_code, headers=headers)
