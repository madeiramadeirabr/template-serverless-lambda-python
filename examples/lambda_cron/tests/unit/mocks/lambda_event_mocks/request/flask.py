"""
Flask Request Mock for test resources
Version: 1.0.0
"""
from unittest.mock import Mock

from flask import request as Request
from werkzeug.datastructures import EnvironHeaders, ImmutableMultiDict, CombinedMultiDict
from werkzeug.routing import Rule

query_params = {}
headers = {}
request = Mock(spec=Request)

request.query_string = b''
request.args = Mock(spec=ImmutableMultiDict)
request.headers = Mock(spec=EnvironHeaders)
request.authorization = None
request.base_url = ''
request.charset = 'utf-8'
request.cookies = Mock(spec=ImmutableMultiDict)
request.data = b''
request.endpoint = ''
request.environ = dict()
request.host = 'localhost:5000'
request.host_url = 'http://localhost:5000/'
request.json = None
request.method = 'GET'
request.mimetype = ''
request.path = ''
request.remote_addr = '127.0.0.1'
request.root_url = 'http://localhost:5000/'
request.schema = 'http'
request.url = ''
request.url_charset = 'utf-8'
request.url_root = 'http://localhost:5000/'
request.url_rule = Rule('')
request.values = Mock(CombinedMultiDict)
request.view_args = {}
