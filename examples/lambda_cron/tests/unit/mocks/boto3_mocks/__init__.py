import os
from unittest.mock import Mock

import boto3
from botocore.session import Session

from tests.unit.mocks.boto3_mocks.resources import table_mock, queue_mock

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

    resource_mock = Mock()
    if service_name == 'sqs':

        resource_mock.get_queue_by_name.return_value = queue_mock

    elif service_name == 'dynamodb':
        resource_mock.Table.return_value = table_mock

    return resource_mock


botocore_session = Mock(Session)
botocore_session.profile = profile

session_mock = Mock(spec=boto3.session.Session)
session_mock._session = botocore_session
session_mock.resource.side_effect = resource
session_mock.profile = profile
