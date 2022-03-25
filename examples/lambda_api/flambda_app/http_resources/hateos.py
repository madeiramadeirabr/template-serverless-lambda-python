"""
HTTP HATEOS Module for Flambda APP
Version: 1.0.0
"""
from flambda_app.enums import CustomStringEnum


class HateosMeta(CustomStringEnum):
    HREF = 'href'
    NEXT = 'next'
    PREVIOUS = 'previous'
    FIRST = 'first'
    LAST = 'last'

    def __new__(cls, value):
        obj = object.__new__(cls)
        # obj.value = value
        obj.meta_name = value
        return obj


class HateosLink(CustomStringEnum):
    DELETE = 'DELETE', 'delete'
    UPDATE = 'UPDATE', 'update'
    PATCH = 'PATCH', 'soft_update'
    GET = 'GET', 'get'

    def __new__(cls, method, rel):
        # obj = CustomStringEnum.__new__(cls, value=method)
        obj = object.__new__(cls)
        obj.method = method
        obj.rel = rel
        return obj
