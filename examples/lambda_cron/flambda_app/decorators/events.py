"""
Flambda Framework Events Module - Chalice Compatible
Version: 1.0.0
"""
import base64
import datetime
from typing import Union, Dict, Any, Iterator, Optional
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


class CloudWatchEvent(BaseLambdaEvent):
    def _extract_attributes(self, event_dict):
        self.version: str = event_dict['version']
        self.account: str = event_dict['account']
        self.region: str = event_dict['region']
        self.detail: dict = event_dict['detail']
        self.detail_type: str = event_dict['detail-type']
        self.source: str = event_dict['source']
        self.time: str = event_dict['time']
        self.event_id: str = event_dict['id']
        self.resources: list = event_dict['resources']


class KinesisEvent(BaseLambdaEvent):
    def _extract_attributes(self, event_dict: Dict[str, Any]) -> None:
        pass

    def __iter__(self) -> Iterator['KinesisRecord']:
        for record in self._event_dict['Records']:
            yield KinesisRecord(record, self.context)


class KinesisRecord(BaseLambdaEvent):
    def _extract_attributes(self, event_dict: Dict[str, Any]) -> None:
        kinesis = event_dict['kinesis']
        encoded_payload = kinesis['data']
        self.data: bytes = base64.b64decode(encoded_payload)
        self.sequence_number: str = kinesis['sequenceNumber']
        self.partition_key: str = kinesis['partitionKey']
        self.schema_version: str = kinesis['kinesisSchemaVersion']
        self.timestamp: datetime.datetime = datetime.datetime.utcfromtimestamp(
            kinesis['approximateArrivalTimestamp'])


class ScheduleExpression(object):
    def to_string(self) -> str:
        raise NotImplementedError("to_string")


class Rate(ScheduleExpression):
    MINUTES: str = 'MINUTES'
    HOURS: str = 'HOURS'
    DAYS: str = 'DAYS'

    def __init__(self, value: int, unit: str) -> None:
        self.value: int = value
        self.unit: str = unit

    def to_string(self) -> str:
        unit = self.unit.lower()
        if self.value == 1:
            # Remove the 's' from the end if it's singular.
            # This is required by the cloudwatch events API.
            unit = unit[:-1]
        return 'rate(%s %s)' % (self.value, unit)


class Cron(ScheduleExpression):
    def __init__(self, minutes: Union[str, int], hours: Union[str, int],
                 day_of_month: Union[str, int], month: Union[str, int],
                 day_of_week: Union[str, int], year: Union[str, int]):
        self.minutes: Union[str, int] = minutes
        self.hours: Union[str, int] = hours
        self.day_of_month: Union[str, int] = day_of_month
        self.month: Union[str, int] = month
        self.day_of_week: Union[str, int] = day_of_week
        self.year: Union[str, int] = year

    def to_string(self) -> str:
        return 'cron(%s %s %s %s %s %s)' % (
            self.minutes,
            self.hours,
            self.day_of_month,
            self.month,
            self.day_of_week,
            self.year,
        )

class DynamoDBEvent(BaseLambdaEvent):
    def _extract_attributes(self, event_dict: Dict[str, Any]) -> None:
        pass

    def __iter__(self) -> Iterator['DynamoDBRecord']:
        for record in self._event_dict['Records']:
            yield DynamoDBRecord(record, self.context)


class DynamoDBRecord(BaseLambdaEvent):

    def _extract_attributes(self, event_dict: Dict[str, Any]) -> None:
        dynamodb = event_dict['dynamodb']
        self.timestamp: datetime.datetime = datetime.datetime.utcfromtimestamp(
            dynamodb['ApproximateCreationDateTime'])
        self.keys: Any = dynamodb.get('Keys')
        self.new_image: Any = dynamodb.get('NewImage')
        self.old_image: Any = dynamodb.get('OldImage')
        self.sequence_number: str = dynamodb['SequenceNumber']
        self.size_bytes: int = dynamodb['SizeBytes']
        self.stream_view_type: str = dynamodb['StreamViewType']
        # These are from the top level keys in a record.
        self.aws_region: str = event_dict['awsRegion']
        self.event_id: str = event_dict['eventID']
        self.event_name: str = event_dict['eventName']
        self.event_source_arn: str = event_dict['eventSourceARN']

    @property
    def table_name(self) -> str:
        # Converts:
        # "arn:aws:dynamodb:us-west-2:12345:table/MyTable/"
        # "stream/2020-09-28T16:49:14.209"
        #
        # into:
        # "MyTable"
        parts = self.event_source_arn.split(':', 5)
        if not len(parts) == 6:
            return ''
        full_name = parts[-1]
        name_parts = full_name.split('/')
        if len(name_parts) >= 2:
            return name_parts[1]
        return ''


# This class is only used for middleware handlers because
# we can't change the existing interface for @app.lambda_function().
# This could be a Chalice 2.0 thing where we make all the decorators
# have a consistent interface that takes a single event arg.
class LambdaFunctionEvent(BaseLambdaEvent):
    def __init__(self, event_dict: Dict[str, Any], context: Any) -> None:
        super().__init__(event_dict, context)
        self.event: Dict[str, Any] = event_dict
        self.context: Optional[Dict[str, Any]] = context

    def _extract_attributes(self, event_dict: Dict[str, Any]) -> None:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return self.event
