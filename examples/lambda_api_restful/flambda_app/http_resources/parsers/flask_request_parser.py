"""
HTTP Request Parser for Flambda APP
Version: 1.0.0
"""
import json

from werkzeug.datastructures import ImmutableMultiDict

from flambda_app import helper
from flambda_app.filter_helper import filter_fields, filter_sql_injection
from flambda_app.http_resources import _REQUEST_IGNORED_KEYS
from flambda_app.request_control import Pagination, Order, PaginationType


class FlaskRequestParser:
    def __init__(self, logger=None):
        self.fields = []
        self.limit = Pagination.LIMIT
        self.offset = Pagination.OFFSET
        self.sort_by = None
        self.order_by = Order.ASC
        self.where = dict()
        self.protocol = helper.get_protocol()
        self.host = None
        self.path = None
        self.method = None
        self.server_type = "Flask"
        self._request = None
        self._logger = logger
        self.json = None
        self.query_string = None
        self.query_string_args = None

    def set_request(self, request):
        self._request = request
        return self

    def parse(self, request=None):
        if not helper.empty(request):
            self._request = request

        request = self._request
        # Query string
        self.query_string = str(request.query_string.decode('ascii'))
        self.query_string_args = {k: v for k, v in request.args.items()}

        # Headers
        if not helper.empty(request.headers):
            if 'host' in request.headers:
                self.host = request.headers['host']
        # path
        if helper.has_attr(request, 'path'):
            self.path = request.path

        # method
        self.method = request.method

        # query params
        if not helper.empty(request.args):
            if 'sort_by' in request.args:
                self.sort_by = str(request.args['sort_by']).split(',')
                # Remove SQL injections
                self.sort_by = filter_fields(self.sort_by)
            if 'order_by' in request.args:
                self.order_by = Order.validate(request.args['order_by'])
            if 'fields' in request.args:
                self.fields = str(request.args['fields']).split(',')
                # Remove SQL injections
                self.fields = filter_fields(self.fields)

            self.offset = Pagination.validate(PaginationType.OFFSET,
                                              request.args.get('offset', Pagination.OFFSET))
            self.limit = Pagination.validate(PaginationType.LIMIT, request.args.get('limit', Pagination.LIMIT))

            # print(request.args['offset'])
            # print(request.args)
            # print(request.headers)
            # print(request.raw_body)
            # print(request.json_body)

        # ***********
        # Params
        # ***********
        # GET
        # print(request.args)
        if not helper.empty(request.args):
            for key in request.args:
                value = request.args.get(key)
                # print('GET k,v', key, value)

                # convert to list
                value = [v.strip() for v in value.split(',')]
                if len(value) == 1:
                    value = value[0]
                # print(value)

                if key not in _REQUEST_IGNORED_KEYS:
                    if key not in self.where:
                        self.where[key] = value
                    else:
                        if not isinstance(self.where[key], list):
                            wlist = [self.where[key]]
                        else:
                            wlist = self.where[key]

                        if isinstance(value, list):
                            wlist = wlist + value
                        else:
                            wlist.append(value)
                        self.where[key] = wlist

        if request.method in ['POST', 'PUT', 'PATCH']:
            # json
            if request.json is not None:
                self.where = request.json

                if self.where is None:
                    if self._logger:
                        self._logger.info('Empty JSON body')
                    self.where = {}
            # form-urlenconded or other
            else:
                request_form = request.form
                if helper.empty(request_form):
                    if not helper.empty(request.data):
                        try:
                            request_form = json.loads(request.data)
                        except Exception as err:
                            self._logger.error(err)

                if isinstance(request_form, dict) and not request_form == {}:
                    for k, v in request_form.items():
                        # if isinstance(v, list) and len(v) == 1:
                        #     self.where[k] = v[0]
                        # else:
                        #     self.where[k] = v
                        key = k.replace('[]', '')
                        if isinstance(request_form, ImmutableMultiDict):
                            value = request_form.getlist(k)
                        else:
                            value = v
                        if isinstance(value, list) and len(value) == 1:
                            value = value[0]
                        if key in self.where:
                            current = self.where[key]
                            if isinstance(current, list):
                                self.where[key] = current + value
                            else:
                                self.where[key] = value
                        else:
                            self.where[key] = value

        # **************************
        # SQL Injection validation
        # **************************
        # print('REQUEST WHERE: ', self.where)
        filtered_where = dict()
        for k, v in self.where.items():
            filtered_where[k] = filter_sql_injection(v)
        self.where = filtered_where
        # print(self.where)
        # print('REQUEST WHERE FILTERED: ', self.where)

        return self

    def request_to_dict(self, request=None):
        if not request:
            request = self._request

        dict_object = request.to_dict()
        return dict_object
