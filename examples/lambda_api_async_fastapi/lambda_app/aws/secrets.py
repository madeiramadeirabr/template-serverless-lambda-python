import os

import boto3
import base64
import json
from lambda_app.logging import get_logger

class Secrets:
    def __init__(self, logger=None):
        """
        # This cant import get_config
        :param logger:
        """
        # logger
        self.logger = logger if logger is not None else get_logger()
        # last_exception
        self.exception = None

    def connect(self):
        connection = None
        try:
            profile = os.environ['AWS_PROFILE'] if 'AWS_PROFILE' in os.environ else None
            region_name = os.environ['AWS_REGION'] if 'AWS_REGION' in os.environ else None
            # region validation
            if region_name is None:
                region_name = os.environ['REGION_NAME'] if 'REGION_NAME' in os.environ else 'us-east-2'

            self.logger.info('profile: {}'.format(profile))
            if profile:
                session = boto3.session.Session(profile_name=profile)
                connection = session.client(
                    service_name='secretsmanager',
                    region_name=region_name
                )
            else:
                connection = boto3.client(
                    service_name='secretsmanager',
                    region_name=region_name
                )

            self.logger.info('Connected')
        except Exception as err:
            self.logger.error(err)
        return connection

    def get_secrets(self, secret_name):
        try:
            client = self.connect()
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            secret_data = json.loads(secret)
        except Exception as err:
            self.logger.error(err)
            self.exception = err
            secret_data = None
        return secret_data
