"""
Default API Schemas Module for Flambda APP
Version: 1.0.0
"""
from marshmallow import Schema, fields

from flambda_app.enums.messages import MessagesEnum
from flambda_app.request_control import Pagination


class DeletionSchema(Schema):
    success = fields.Bool(default=False)
    code = fields.Int(required=True)
    label = fields.Str()
    message = fields.Str()
    params = fields.List(fields.Str())


class ErrorSchema(Schema):
    success = fields.Bool(example=False, default=False)
    code = fields.Int(example=MessagesEnum.INTERNAL_SERVER_ERROR.code, required=True)
    label = fields.Str(example=MessagesEnum.INTERNAL_SERVER_ERROR.label)
    message = fields.Str(example=MessagesEnum.INTERNAL_SERVER_ERROR.message)
    params = fields.List(fields.Str())
    details = fields.Str()
    trace = fields.Str()


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


class DefaultResponseSchema(Schema):
    success = fields.Bool(example=True, default=True)
    code = fields.Int(example=MessagesEnum.OK.code, required=True)
    label = fields.Str(example=MessagesEnum.OK.label)
    message = fields.Str(example=MessagesEnum.OK.message)
    params = fields.List(fields.Str())


class HateosDefaultResponseSchema(DefaultResponseSchema):
    meta = fields.Nested(MetaSchema)
    links = fields.List(fields.Nested(LinkSchema))


class HateosDefaultListResponseSchema(DefaultResponseSchema):
    meta = fields.Nested(MetaSchema)
