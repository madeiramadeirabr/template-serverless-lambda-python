"""
DynamoDB Module for Flambda APP
Version: 1.0.0
"""
import os
from time import sleep

import boto3

from flambda_app.config import get_config
from flambda_app.logging import get_logger


_CONNECTION = False
_RETRY_COUNT = 0
_MAX_RETRY_ATTEMPTS = 3


def reset():
    global _CONNECTION
    _CONNECTION = False


class DynamodbConnector:
    def __init__(self, config=None, logger=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # logger
        self.config = config if config is not None else get_config()
        # last_exception
        self.exception = None

    def get_connection(self, connect=True, retry=False):
        global _CONNECTION, _RETRY_COUNT, _MAX_RETRY_ATTEMPTS
        if not _CONNECTION:
            connection = None
            try:
                profile = os.environ['AWS_PROFILE'] if 'AWS_PROFILE' in os.environ else None
                self.logger.info('profile: {}'.format(profile))
                if profile:
                    session = boto3.session.Session(profile_name=profile)
                    connection = session.resource(
                        'dynamodb',
                        region_name="sa-east-1"
                    )
                else:
                    connection = boto3.resource(
                        'dynamodb',
                        region_name="sa-east-1"
                    )

                _CONNECTION = connection
                _RETRY_COUNT = 0
                self.logger.info('Connected')

            except Exception as err:
                if _RETRY_COUNT == _MAX_RETRY_ATTEMPTS:
                    _RETRY_COUNT = 0
                    self.logger.error(err)
                    return connection
                else:
                    self.logger.error(err)
                    self.logger.info('Trying to reconnect... {}'.format(_RETRY_COUNT))

                    sleep(0.1)
                    # retry
                    if not retry:
                        _RETRY_COUNT += 1
                        return self.get_connection(True)
        else:
            connection = _CONNECTION

        return connection
