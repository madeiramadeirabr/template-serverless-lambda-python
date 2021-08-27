import json
import os

from flask_app.config import get_config
from flask_app.logging import get_logger
import boto3


class SQSEvents:

    def __init__(self, logger=None, config=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # last_exception
        self.exception = None

    def connect(self):
        connection = None
        try:
            endpoint_url = self.config.SQS_ENDPOINT
            profile = os.environ['AWS_PROFILE'] if 'AWS_PROFILE' in os.environ else None
            self.logger.info('SQSEvents - profile: {}'.format(profile))
            self.logger.info('SQSEvents - endpoint_url: {}'.format(endpoint_url))
            self.logger.info('SQSEvents - self.config.REGION_NAME: {}'.format(self.config.REGION_NAME))
            if profile:
                session = boto3.session.Session(profile_name=profile)
                connection = session.resource(
                    'sqs',
                    endpoint_url=endpoint_url,
                    region_name=self.config.REGION_NAME
                )
            else:
                connection = boto3.resource(
                    'sqs',
                    endpoint_url=endpoint_url,
                    region_name=self.config.REGION_NAME
                )

            self.logger.info('SQSEvents - Connected')

        except Exception as err:
            self.logger.error(err)

        return connection

    def send_message(self, message, queue_url):
        sqs = self.connect()
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
        sqs = self.connect()
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
        queue = None
        if not attributes:
            attributes = {'DelaySeconds': '5'}

        sqs = self.connect()
        try:
            # Create the queue. This returns an SQS.Queue instance
            queue = sqs.create_queue(QueueName=queue_name, Attributes=attributes)
        except Exception as err:
            self.logger.error(err)
            self.exception = err

        return queue

    def delete_queue(self, queue_name):
        result = True

        sqs = self.connect()
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




