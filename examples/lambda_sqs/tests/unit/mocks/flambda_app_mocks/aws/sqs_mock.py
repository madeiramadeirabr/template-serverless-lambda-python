"""
AWS SQS Module Mock for test resources
Version: 1.0.0
"""
from unittest.mock import Mock

from flambda_app.aws.sqs import SQS

response_mock = {
    'MD5OfMessageBody': 'string',
    'MD5OfMessageAttributes': 'string',
    'MD5OfMessageSystemAttributes': 'string',
    'MessageId': 'string',
    'SequenceNumber': 'string'
}

sqs_mock = Mock(SQS)
sqs_mock.connect.side_effect = lambda retry=False: True
sqs_mock.send_message.side_effect = lambda message, queue_url: response_mock
