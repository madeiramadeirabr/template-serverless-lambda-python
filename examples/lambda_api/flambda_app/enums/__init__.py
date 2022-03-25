"""
Enumerators Module for Flambda APP
Version: 1.0.0
"""
import json
from enum import Enum, IntEnum


class CustomEnum(Enum):

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        return {'value': self.value}

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def get_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def get_codes(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def from_value(cls, value):
        for e in cls:
            # print(e.value, value, e.value == value)
            if isinstance(e.value, tuple):
                if e.value[0] == value:
                    return e
                elif e.value == value:
                    return e
            elif e.value == value:
                return e
        return None

    @classmethod
    def from_code(cls, code):
        for e in cls:
            if e.name == code:
                return e
        return None


class CustomIntEnum(IntEnum):
    @classmethod
    def get_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def get_codes(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def from_value(cls, value):
        for e in cls:
            # print(e.value, value, e.value == value)
            if isinstance(e.value, tuple):
                if e.value[0] == value:
                    return e
                elif e.value == value:
                    return e
            elif e.value == value:
                return e
        return None

    @classmethod
    def from_code(cls, code):
        for e in cls:
            if e.name == code:
                return e
        return None


class CustomStringEnum(CustomEnum):
    # não usar propriedades default value, name etc
    # def __new__(cls, value):
    #     obj = object.__new__(cls)
    #     obj.value = value
    #     return obj

    @classmethod
    def from_description(cls, description):
        for e in cls:
            if e.description == description:
                return e
        return None
