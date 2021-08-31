import os

from lambda_app.events.aws.sqs import SQSEvents


class SQSHelper:

    @classmethod
    def get_message(cls, queue_url):
        sqs = SQSEvents()
        message_array = sqs.get_message(queue_url)
        return message_array

    @classmethod
    def create_message(cls, message, queue_url):
        sqs = SQSEvents()
        return sqs.send_message(message, queue_url)

    @classmethod
    def event_to_dict(cls, event):
        """
        :param sqs.Message event:
        :return:
        """
        event_dict = {
            "messageId": event.message_id,
            "receiptHandle": event.receipt_handle,
            "attributes": event.attributes if event.attributes is not None else {},
            "messageAttributes": event.message_attributes if event.message_attributes is not None else {},
            "md5OfBody": event.md5_of_body,
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-east-2:123456789:queuename",
            "awsRegion": "us-east-2",
            "field_data": "body",
            "body": event.body
        }

        return event_dict

    @classmethod
    def delete_queue(cls, queue_url):
        queue_name = cls.get_queue_name(queue_url)
        sqs = SQSEvents()
        return sqs.delete_queue(queue_name)

    @classmethod
    def create_queue(cls, queue_url, attributes=None):
        queue_name = cls.get_queue_name(queue_url)
        sqs = SQSEvents()
        return sqs.create_queue(queue_name, attributes)

    @classmethod
    def get_queue_name(cls, queue_url):
        return os.path.basename(queue_url)
