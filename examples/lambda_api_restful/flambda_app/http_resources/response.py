"""
HTTP Response Module for Flambda APP
Version: 1.0.0
"""
import json
import traceback

from flask import Response

from boot import get_environment
from flambda_app import helper
from flambda_app.enums import CustomStringEnum
from flambda_app.enums.messages import MessagesEnum
from flambda_app.exceptions import ApiException
from flambda_app.http_helper import CUSTOM_DEFAULT_HEADERS
from flambda_app.http_resources.hateos import HateosLink, HateosMeta
from flambda_app.request_control import Pagination
from flambda_app.logging import get_logger


class ApiResponse:
    def __init__(self, api_request=None, logger=None):
        """
        :param (ApiRequest) api_request:
        """
        self.logger = logger if logger is not None else get_logger()
        self.hateos = True
        self.status_code = 200
        self.headers = CUSTOM_DEFAULT_HEADERS
        self.exception = None
        # used when you decide to describe the origin of the exception
        # example: unable to insert the product because another product with the same data already was found
        self.exception_details = None

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
        self.params = api_request.fields if api_request is not None else []

        self.api_request = api_request

    def set_hateos(self, flag: bool):
        self.hateos = flag

    def set_data(self, data):
        # data
        self.data = data

        # has method dict to convert
        if helper.has_method(self.data, 'to_dict'):
            self.data = data.to_dict()

        if isinstance(self.data, list):
            # has method dict to convert
            if helper.has_method(self.data[0], 'to_dict'):
                dict_data = []
                for item in self.data:
                    dict_data.append(item.to_dict())
                self.data = dict_data

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

            body = {
                "success": success,
                "code": code,
                "label": label,
                "message": message,
                "params": params,
                "details": self.exception_details
            }

            # only for development
            if get_environment() == "development":
                try:
                    # raise exception to get the trace
                    raise self.exception
                except Exception as err:
                    self.logger.debug('getting trace for debug of the exception {}'.format(err))
                    body["trace"] = traceback.format_exc()

        else:
            if self.total > 1:
                self.links = []
            else:
                self.logger.info('links: {}'.format(self.links))
                if self.links == list():
                    self.links = [
                        {
                            "href": "",
                            "rel": HateosLink.UPDATE.rel,
                            "method": HateosLink.UPDATE.method,
                        },
                        {
                            "href": "",
                            "rel": HateosLink.DELETE.rel,
                            "method": HateosLink.DELETE.method,
                        },
                        {
                            "href": "",
                            "rel": HateosLink.PATCH.rel,
                            "method": HateosLink.PATCH.method,
                        },
                        {
                            "href": "",
                            "rel": HateosLink.GET.rel,
                            "method": HateosLink.GET.method,
                        }
                    ]

            if self.meta == dict():
                self.meta = {
                    "href": HateosMeta.HREF,
                    "next": HateosMeta.NEXT,
                    "previous": HateosMeta.PREVIOUS,
                    "first": HateosMeta.FIRST,
                    "last": HateosMeta.LAST
                }

            body = {
                # success
                "success": success,
                "label": label,
                "code": code,
                "message": message,
                "params": self.params,
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

            # remove empty links (main used for list pages)
            # response.links = None
            # set_hateos_meta(request, response)
            if self.links is None:
                del body["links"]

            if self.meta is None:
                del body["meta"]

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

    def set_hateos_link(self, link: HateosLink, href):
        self.links.append({
            "href": href,
            "rel": link.rel,
            "method": link.method,
        })

    def set_meta(self, meta: HateosMeta, value):
        self.meta[meta.meta_name] = value
