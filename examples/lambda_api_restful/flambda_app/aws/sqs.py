"""
AWS SQS Module
Version: 1.0.2
"""
import json
import os

from boot import get_environment
from flambda_app import helper
from flambda_app.aws import change_endpoint
from flambda_app.config import get_config
from flambda_app.logging import get_logger
import boto3

_RETRY_COUNT = 0
_MAX_RETRY_ATTEMPTS = 3


class SQS:

    def __init__(self, logger=None, config=None, profile=None, session=None):
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
        # endpoint_url (LOCALSTACK or None for AWS)
        endpoint_url = self.config.get('LOCALSTACK_ENDPOINT', None)
        self.endpoint_url = endpoint_url if endpoint_url != "" else None
        # region_name
        self.region_name = self.config.get('REGION_NAME', 'us-east-2')

        self.connection = None

    def connect(self, retry=False):
        global _RETRY_COUNT, _MAX_RETRY_ATTEMPTS
        connection = self.connection
        if connection is None:
            try:

                self.logger.info('SQS - profile: {}'.format(self.profile))
                self.logger.info('SQS - endpoint_url: {}'.format(self.endpoint_url))
                self.logger.info('SQS - region_name: {}'.format(self.region_name))

                if self.profile:
                    session = self.session
                    connection = session.resource(
                        'sqs',
                        endpoint_url=self.endpoint_url,
                        region_name=self.region_name
                    )
                else:
                    connection = boto3.resource(
                        'sqs',
                        endpoint_url=self.endpoint_url,
                        region_name=self.region_name
                    )

                try:
                    # only do this test for development because the docker/local diff
                    # avoid dummy connection
                    if get_environment() == "development" and connection:
                        connection.meta.client.list_queues()
                except Exception as err:
                    if helper.has_attr(err, "response") and err.response['Error']:
                        self.logger.error(err)
                    else:
                        connection = None
                        raise err

                _RETRY_COUNT = 0
                self.connection = connection
                if connection is None:
                    raise Exception('Unable to connect')
            except Exception as err:
                if _RETRY_COUNT == _MAX_RETRY_ATTEMPTS:
                    _RETRY_COUNT = 0
                    self.logger.error(err)
                    connection = None
                    self.connection = connection
                else:
                    self.logger.error(err)
                    self.logger.info('Trying to reconnect... {}'.format(_RETRY_COUNT))
                    # retry
                    if not retry:
                        _RETRY_COUNT += 1
                        change_endpoint(self)
                        connection = self.connect(retry=True)
                        self.connection = connection
        return connection

    def send_message(self, message, queue_url):
        if self.connection is None:
            self.connect()
        sqs = self.connection
        if queue_url is None:
            raise Exception('Queue name must be informed')
        queue_name = os.path.basename(queue_url)

        try:
            # Get the queue
            queue = sqs.get_queue_by_name(QueueName=queue_name)

            # Avoid double json encode
            if not isinstance(message, str):
                try:
                    message = json.dumps(message)
                except Exception as err:
                    self.logger.error(err)
                    message = str(message)
            # Create a new message
            response = queue.send_message(MessageBody=message)
        except Exception as err:
            self.logger.error(err)
            self.exception = err
            response = None

        return response

    def get_message(self, queue_url):
        if self.connection is None:
            self.connect()
        sqs = self.connection
        if queue_url is None:
            raise Exception('Queue name must be informed')
        queue_name = os.path.basename(queue_url)

        try:
            # Get the queue
            queue = sqs.get_queue_by_name(QueueName=queue_name)

            # Create a new message
            message = queue.receive_messages(
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                VisibilityTimeout=5,
                WaitTimeSeconds=1
            )

        except Exception as err:
            self.logger.error(err)
            self.exception = err
            message = None

        return message

    def create_queue(self, queue_name, attributes=None):
        if self.connection is None:
            self.connect()
        sqs = self.connection

        queue = None
        if not attributes:
            attributes = {'DelaySeconds': '5'}

        try:
            # Create the queue. This returns an SQS.Queue instance
            queue = sqs.create_queue(QueueName=queue_name, Attributes=attributes)
        except Exception as err:
            self.logger.error(err)
            self.exception = err

        return queue

    def delete_queue(self, queue_name):
        result = True

        if self.connection is None:
            self.connect()
        sqs = self.connection

        try:
            # Get the queue
            queue = sqs.get_queue_by_name(QueueName=queue_name)
            if queue is not None:
                queue_url = queue.url
                client = sqs.meta.client
                client.delete_queue(QueueUrl=queue_url)
            else:
                raise Exception('queue not exists')
            # QueueUrl

        except Exception as err:
            self.logger.error(err)
            self.exception = err
            result = False

        return result
