"""
HTTP Request Module for Flambda APP
Version: 1.0.0
"""
import copy
import json
import uuid

from flambda_app import helper
from flambda_app.request_control import Pagination, Order
from flambda_app.http_resources.parsers.flask_request_parser import FlaskRequestParser
from flask import request


class ApiRequest:
    """
    """

    def __init__(self, app=None):
        """
        :param app:
        """
        self.uuid = uuid.uuid1()
        self.server_type = None
        self.fields = []
        self.limit = Pagination.LIMIT
        self.offset = Pagination.OFFSET
        self.sort_by = None
        self.order_by = Order.ASC
        self.where = {}
        self.protocol = helper.get_protocol()
        self.host = None
        self.path = None
        self.method = None
        self.query_string = None
        self.query_string_args = None

        # Original chalice/flask request
        self._request = None

        if app is not None:
            self.parse_request(app)

    def get_where(self):
        return self.where

    def keys(self):
        data = self.to_dict()
        return list(data.keys())

    def __getitem__(self, item):
        try:
            value = getattr(self, item)
        except:
            value = None
        return value

    def __str__(self):
        return self.to_json()

    def to_dict(self, force_str=False):
        data = helper.to_dict(self, force_str)
        data['_request'] = None
        # solução para evitar erro:
        # UUID('…') is not JSON serializable
        data['uuid'] = self.uuid.hex
        return data

    def to_json(self):
        return json.dumps(self.to_dict())

    def deepcopy(self, logger=None):
        tmp_request = self._request

        # Remove objetos de buffer para fazer a copia
        self._request = None

        # BUGFIX: copy() Vai evitar a sobrescrita de valores na requisição original
        self_copy = copy.deepcopy(self)
        self_copy._request = tmp_request

        self._request = tmp_request

        return self_copy

    def parse_request(self, app):
        """
        :param (chalice.app.Chalice) app:
        :return:
        """
        request_parser = FlaskRequestParser()
        parsed_request = request_parser.parse(request)

        self.fields = parsed_request.fields
        self.limit = parsed_request.limit
        self.offset = parsed_request.offset
        self.sort_by = parsed_request.sort_by
        self.order_by = parsed_request.order_by
        self.where = parsed_request.where
        self.protocol = parsed_request.protocol
        self.host = parsed_request.host
        self.path = parsed_request.path
        self.method = parsed_request.method
        self.server_type = parsed_request.server_type
        self.query_string = parsed_request.query_string
        self.query_string_args = parsed_request.query_string_args
        self._request = request

        return self

    @staticmethod
    def factory(method, host, path):
        api_request = ApiRequest()
        api_request.method = method
        api_request.host = host
        api_request.path = path
        return api_request
