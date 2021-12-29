import requests
from mock.mock import Mock, MagicMock
from requests.models import Response
from requests.api import request

# ******************
# GET - Response
# ******************
get_response_mock = MagicMock(Response)
get_response_mock.status_code = 200


# GET method
def get(url, params=None, **kwargs):
    r"""Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    # return request('get', url, params=params, **kwargs)
    return get_response_mock


# ********************************
# module mock
# ********************************
requests_mock = Mock(requests)

http_client_mock = requests_mock
http_client_mock.get.side_effect = get
