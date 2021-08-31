import os
from unittest.mock import Mock

import boto3
from boto3.dynamodb.table import TableResource
from boto3.resources.base import ServiceResource
from botocore.session import Session
from mock.mock import MagicMock

profile = os.environ['AWS_PROFILE'] if 'AWS_PROFILE' in os.environ else None


def resource(service_name, region_name=None, api_version=None,
             use_ssl=True, verify=None, endpoint_url=None,
             aws_access_key_id=None, aws_secret_access_key=None,
             aws_session_token=None, config=None):
    """

    :param self:
    :param service_name:
    :param region_name:
    :param api_version:
    :param use_ssl:
    :param verify:
    :param endpoint_url:
    :param aws_access_key_id:
    :param aws_secret_access_key:
    :param aws_session_token:
    :param config:
    :return: boto3.resources.base.ServiceResource
    """

    # resource_mock = Mock(ServiceResource)
    resource_mock = Mock()
    resource_mock.Table.return_value = table_mock

    return resource_mock




iterable = MagicMock(return_value=iter([MagicMock(return_value=1), MagicMock(return_value=2)]))
table_mock = Mock()
# table_mock.scan = Mock()
table_mock.scan.side_effect = lambda:  {
    'Items': []
}
table_mock.item_count = 0
table_mock.put_item.side_effect = lambda: {"success": "true"}

botocore_session = Mock(Session)
botocore_session.profile = profile

session_mock = Mock(spec=boto3.session.Session)
session_mock._session = botocore_session
session_mock.resource.side_effect = resource

connection_mock = session_mock.resource('dynamodb', region_name="sa-east-1")
