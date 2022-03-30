"""
Boto3 Module Mock for test resources
Version: 1.0.0
"""
import os

from mock.mock import MagicMock, Mock

region = os.getenv("REGION_NAME") if 'REGION_NAME' in os.environ else "sa-east-1"
# *****************************
# sqs
# *****************************
# boto3.resources.factory.sqs.Queue
queue_mock = Mock()
queue_mock.attributes.return_value = {
    "ApproximateNumberOfMessages": "0", "ApproximateNumberOfMessagesDelayed": "0",
    "ApproximateNumberOfMessagesNotVisible": "0", "CreatedTimestamp": "1640732822.369549", "DelaySeconds": "1",
    "LastModifiedTimestamp": "1640732822.369549", "MaximumMessageSize": "262144", "MessageRetentionPeriod": "345600",
    "QueueArn": "arn:aws:sqs:us-east-1:000000000000:test-queue",
    "ReceiveMessageWaitTimeSeconds": "0", "VisibilityTimeout": "30"}
# sqs.Queue.dead_letter_source_queuesCollectionManager(sqs.Queue(
# url='http://localstack:4566/000000000000/test-queue'), sqs.Queue)
queue_mock.dead_letter_source_queues = Mock()
queue_mock.meta.return_value = Mock()
queue_mock.url.return_value = 'http://localstack:4566/000000000000/test-queue'
queue_mock._url.return_value = 'http://localstack:4566/000000000000/test-queue'

# methods
queue_mock.add_permission.side_effect = lambda arg: None
queue_mock.change_message_visibility_batch.side_effect = lambda arg: None
queue_mock.delete.side_effect = lambda arg: None
queue_mock.delete_messages.side_effect = lambda arg: None
queue_mock.get_available_subresources.side_effect = lambda arg: None
queue_mock.load.side_effect = lambda arg: None
queue_mock.purge.side_effect = lambda arg: None
queue_mock.receive_messages.side_effect = lambda arg: None
queue_mock.reload.side_effect = lambda arg: None
queue_mock.remove_permission.side_effect = lambda arg: None
queue_mock.send_message.side_effect = lambda MessageBody: {
    'MD5OfMessageBody': '575fcb71f54080feeaad3b9b293519ca', 'MessageId': '62feb641-73b1-a640-063c-4cab06f0d319',
    'ResponseMetadata': {'RequestId': 'FQBWUDQFWULED7JUBV3682ZBLMX4OQZW1RJMNFEH9Y89QFMC0LG6', 'HTTPStatusCode': 200,
                         'HTTPHeaders': {
                             'content-type': 'text/html; charset=utf-8', 'content-length': '322',
                             'x-amzn-requestid': 'FQBWUDQFWULED7JUBV3682ZBLMX4OQZW1RJMNFEH9Y89QFMC0LG6',
                             'x-amz-crc32': '3181316234', 'access-control-allow-origin': '*',
                             'access-control-allow-methods': 'HEAD,GET,PUT,POST,DELETE,OPTIONS,PATCH',
                             'access-control-allow-headers': 'authorization,content-type,content-length,content-md5,'
                                                             'cache-control,x-amz-content-sha256,x-amz-date,'
                                                             'x-amz-security-token,x-amz-user-agent,x-amz-target,'
                                                             'x-amz-acl,x-amz-version-id,x-localstack-target,'
                                                             'x-amz-tagging', 'access-control-expose-headers':
                             'x-amz-version-id', 'connection': 'close', 'date': 'Tue, 28 Dec 2021 23:17:16 GMT',
                             'server': 'hypercorn-h11'}, 'RetryAttempts': 0}}
queue_mock.send_messages.side_effect = lambda arg: None
queue_mock.set_attributes.side_effect = lambda arg: None
# *****************************
# dynamodb
# *****************************
iterable = MagicMock(return_value=iter([MagicMock(return_value=1), MagicMock(return_value=2)]))
table_mock = Mock()
# table_mock.scan = Mock()
table_mock.scan.side_effect = lambda: {
    'Items': []
}
table_mock.item_count = 0
table_mock.put_item.side_effect = lambda: {"success": "true"}
