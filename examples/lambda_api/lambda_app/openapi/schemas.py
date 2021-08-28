from marshmallow import Schema, fields

from lambda_app.http_resources.request_control import Pagination


class DeletionSchema(Schema):
    success = fields.Bool()
    code = fields.Int(required=True)
    label = fields.Str()
    message = fields.Str()
    params = fields.List(fields.Str())


class ErrorSchema(Schema):
    code = fields.Int(required=True)
    label = fields.Str()
    message = fields.Str()


class RequestControlSchema(Schema):
    offset = fields.Int(default=Pagination.OFFSET)
    limit = fields.Int(required=True, default=Pagination.LIMIT)
    total = fields.Int()
    count = fields.Int()


class MetaSchema(Schema):
    href = fields.URL()
    next = fields.URL()
    previous = fields.URL()
    first = fields.URL()
    last = fields.URL()


class LinkSchema(Schema):
    href = fields.Str()
    rel = fields.Str()
    method = fields.Str()


class PingSchema(Schema):
    message = fields.Str(example="PONG")


class AliveSchema(Schema):
    app = fields.Str(example="I'm alive!")
