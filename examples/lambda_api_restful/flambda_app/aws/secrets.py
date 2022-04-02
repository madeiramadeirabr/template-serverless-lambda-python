"""
AWS SecretsManager Module
Version: 1.0.0
"""
import os

import boto3
import base64
import json

from flambda_app.config import get_config
from flambda_app.logging import get_logger


class Secrets:
    def __init__(self, logger=None, config=None, profile=None, session=None):
        """
        # This cant import get_config
        :param logger:
        """
        # logger
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # last_exception
        self.exception = None
        # profile
        self.profile = profile if profile is not None else \
            os.environ['AWS_PROFILE'] if 'AWS_PROFILE' in os.environ else None
        # session
        self.session = session if session is not None else \
            boto3.session.Session(profile_name=self.profile)

    def connect(self):
        connection = None
        try:
            endpoint_url = self.config.get('LOCALSTACK_ENDPOINT', None)
            region_name = self.config.get('REGION_NAME', 'us-east-2')
            secrets_name = self.config.get('APP_SECRETS', None)

            self.logger.info('Secrets - profile: {}'.format(self.profile))
            self.logger.info('Secrets - endpoint_url: {}'.format(endpoint_url))
            self.logger.info('Secrets - region_name: {}'.format(region_name))
            self.logger.info('Secrets - secrets_name: {}'.format(secrets_name))

            if self.profile:
                session = self.session
                # todo avaliar troca para session.resource
                connection = session.client(
                    service_name='secretsmanager',
                    region_name=region_name
                )
            else:
                # todo avaliar troca para boto3.resource
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
