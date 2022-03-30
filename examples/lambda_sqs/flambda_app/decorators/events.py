"""
Flambda Framework Events Module - Chalice Compatible
Version: 1.0.0
"""
from urllib.parse import unquote_plus

unquote_str = unquote_plus


class BaseLambdaEvent(object):
    def __init__(self, event_dict, context):
        self._event_dict = event_dict
        self.context = context
        self._extract_attributes(event_dict)

    def _extract_attributes(self, event_dict):
        raise NotImplementedError("_extract_attributes")

    def to_dict(self):
        return self._event_dict


class SQSEvent(BaseLambdaEvent):
    def _extract_attributes(self, event_dict):
        # We don't extract anything off the top level
        # event.
        pass

    def __iter__(self):
        for record in self._event_dict['Records']:
            yield SQSRecord(record, self.context)


class SNSEvent(BaseLambdaEvent):
    def _extract_attributes(self, event_dict):
        first_record = event_dict['Records'][0]
        self.message = first_record['Sns']['Message']
        self.subject = first_record['Sns']['Subject']


class S3Event(BaseLambdaEvent):
    def _extract_attributes(self, event_dict):
        s3 = event_dict['Records'][0]['s3']
        self.bucket = s3['bucket']['name']
        self.key = unquote_str(s3['object']['key'])


class SQSRecord(BaseLambdaEvent):
    def _extract_attributes(self, event_dict):
        self.body = event_dict['body']
        self.receipt_handle = event_dict['receiptHandle']
