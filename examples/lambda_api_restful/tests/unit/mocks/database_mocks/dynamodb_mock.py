"""
DynamoDB Module Mock for test resources
Version: 1.0.0
"""
# prioriza a importação dos testes para funcionar as libs da vendor
import os

from flambda_app.logging import get_logger
from tests.unit.mocks.boto3_mocks import session_mock

logger = get_logger()


def get_connection(retry=False):
    # profile = os.environ['AWS_PROFILE'] if 'AWS_PROFILE' in os.environ else None
    # logger.info('profile: {}'.format(profile))

    session = session_mock
    connection = session.resource(
        'dynamodb',
        region_name="sa-east-1"
    )

    return connection
