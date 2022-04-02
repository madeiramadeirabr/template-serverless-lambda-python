"""
Exception Module for Flambda APP
Version: 1.0.0
"""
import json

from flambda_app import helper


class CustomException(Exception):
    def __init__(self, message_enum, errors=None):
        """
        :param (MessagesEnum) message_enum:
        :param errors:
        """
        # print(message_enum)
        super(Exception, self).__init__(message_enum.message, errors)
        self.code = message_enum.code
        self.label = message_enum.label
        self.message = message_enum.message
        self.params = None

    def set_message(self, message, params):
        if params:
            self.params = params
            if isinstance(params, Exception):
                self.message = message % str(params)
            else:
                self.message = message % tuple(params)
        else:
            self.message = message

    def set_message_params(self, params=None):
        if params is not None:
            self.params = params
        else:
            params = self.params

        if isinstance(params, Exception):
            self.message = self.message % str(params)
        else:
            if isinstance(params, tuple) or isinstance(params, list):
                self.message = self.message % tuple(params)
            else:
                self.message = self.message % params

    def set_params(self, params):
        self.params = params

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return str(self.to_dict())

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return helper.to_dict(self)


class EventException(CustomException):
    def __init__(self, message_enum, errors=None):
        """
        :param (MessagesEnum) message_enum:
        :param errors:
        """
        super(CustomException, self).__init__(message_enum.message, errors)
        self.code = message_enum.code
        self.label = message_enum.label
        self.message = message_enum.message
        self.params = None


class ApiException(CustomException):
    def __init__(self, message_enum, errors=None):
        """
        :param (MessagesEnum) message_enum:
        :param errors:
        """
        super(CustomException, self).__init__(message_enum.message, errors)
        self.code = message_enum.code
        self.label = message_enum.label
        self.message = message_enum.message
        self.params = None


class DatabaseException(ApiException):
    def __init__(self, message_enum, errors=None):
        """
        :param (MessagesEnum) message_enum:
        :param errors:
        """
        super(ApiException, self).__init__(message_enum, errors)
        self.code = message_enum.code
        self.label = message_enum.label
        self.message = message_enum.message
        self.params = None


class FilterException(ApiException):
    def __init__(self, message_enum, errors=None):
        """
        :param (MessagesEnum) message_enum:
        :param errors:
        """
        super(ApiException, self).__init__(message_enum, errors)
        self.code = message_enum.code
        self.label = message_enum.label
        self.message = message_enum.message
        self.params = None


class ValidationException(ApiException):
    def __init__(self, message_enum, errors=None):
        """
        :param (MessagesEnum) message_enum:
        :param errors:
        """
        super(ApiException, self).__init__(message_enum, errors)
        self.code = message_enum.code
        self.label = message_enum.label
        self.message = message_enum.message
        self.params = None


class ServiceException(CustomException):
    def __init__(self, message_enum, errors=None):
        """
        :param (MessagesEnum) message_enum:
        :param errors:
        """
        super(CustomException, self).__init__(message_enum.message, errors)
        self.code = message_enum.code
        self.label = message_enum.label
        self.message = message_enum.message
        self.params = None
