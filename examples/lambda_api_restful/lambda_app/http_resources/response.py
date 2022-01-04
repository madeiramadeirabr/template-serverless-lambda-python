import json

from flask import Response
from lambda_app import helper
from lambda_app.enums.messages import MessagesEnum
from lambda_app.exceptions import ApiException
from lambda_app.http_resources.request_control import Pagination
from lambda_app.http_helper import CUSTOM_DEFAULT_HEADERS


class ApiResponse:
    def __init__(self, api_request=None):
        """
        :param (ApiRequest) api_request:
        """
        self.hateos = True
        self.status_code = 200
        self.headers = CUSTOM_DEFAULT_HEADERS
        self.exception = None

        self.links = []
        self.meta = {}
        self.data = {}

        # others
        self.first = {}
        self.next = {}
        self.last = {}
        self.limit = api_request.limit if api_request is not None else Pagination.LIMIT
        self.offset = api_request.offset if api_request is not None else Pagination.OFFSET
        self.total = 0
        self.count = 0

        self.api_request = api_request

    def set_hateos(self, flag: bool):
        self.hateos = flag

    def set_data(self, data):
        # data
        self.data = data
        if isinstance(data, list):
            self.count = len(self.data)
        else:
            self.count = 1
            self.total = 1

    def set_total(self, total):
        self.total = total

    def set_exception(self, exception):
        self.exception = exception

    def get_response(self, status_code=None):

        if status_code:
            self.status_code = status_code

        headers = self.headers
        status_code = self.status_code
        success = status_code == 200
        message = MessagesEnum.OK.message
        code = MessagesEnum.OK.code
        label = MessagesEnum.OK.label
        params = []

        if self.exception is not None:
            if isinstance(self.exception, ApiException):
                code = self.exception.code
                label = self.exception.label
                message = self.exception.message
                params = self.exception.params
            else:
                message = self.data if not None else MessagesEnum.UNKNOWN_ERROR
                code = MessagesEnum.NOK.code
                label = MessagesEnum.NOK.label
                message = MessagesEnum.NOK.message % message

            # TODO rever
            body = {
                "error": {
                    "code": code,
                    "label": label,
                    "message": message,
                    "params": params
                }
            }

        else:
            if self.total > 1:
                self.links = []
            else:
                self.links = [
                    {
                        "href": "",
                        "rel": "update",
                        "method": "POST",
                    },
                    {
                        "href": "",
                        "rel": "delete",
                        "method": "DELETE",
                    },
                    {
                        "href": "",
                        "rel": "patch",
                        "method": "PATCH",
                    }
                ]

            self.meta = {
                "href": "",
                "next": "",
                "previous": "",
                "first": "",
                "last": ""
            }

            body = {
                # success
                "success": success,
                "label": label,
                "code": code,
                "message": message,
                "params": [],
                # data
                "data": self.data,
                # navigation
                "control": {
                    "offset": self.offset,
                    "limit": self.limit,
                    "total": self.total,
                    "count": self.count,
                },
                # hypermedia info
                "meta": self.meta,
                # hypermedia links
                "links": self.links
            }

            if not self.hateos:
                del body["meta"]
                del body["links"]

           # todo deletar o control na leitura de um item unico

        if 'Content-Type' in headers and headers['Content-Type'] == 'application/json':
            body = helper.to_json(body)
        return Response(response=body, status=status_code, headers=headers)

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return list(self.__dict__.keys())

    def __str__(self):
        return self.to_json()

    def to_dict(self, force_str=False):
        return helper.to_dict(self, force_str)

    def to_json(self):
        return json.dumps(self.to_dict(force_str=False))
