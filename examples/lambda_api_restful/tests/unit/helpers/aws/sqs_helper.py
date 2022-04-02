"""
SQS Helper module for test resources
Version: 1.0.0
"""
import json
from os import path

from flambda_app.decorators.events import SQSRecord, SQSEvent
from tests import ROOT_DIR


def create_chalice_sqs_record(event_dict, context=None):
    event = event_dict
    if event_dict[0]:
        event = event_dict[0]
    else:
        if not 'body' in event_dict and not 'messageId' in event_dict:
            event = get_sqs_event_stub()
            event['body'] = event_dict
    sqs_record = SQSRecord(event, context)
    return sqs_record


def create_chalice_sqs_event(event_dict, context=None):
    sqs_event = event_dict
    if 'Records' not in event_dict:
        sqs_message_stub = get_sqs_message_stub()
        sqs_message_stub['body'] = json.dumps(event_dict)
        sqs_event = get_sqs_event_stub()
        records = sqs_event['Records']
        records.append(sqs_message_stub)

    return SQSEvent(sqs_event, context)


def get_sqs_event_stub():
    with open(path.join(ROOT_DIR, 'tests/datasources/events/sqs/sqs.event.stub.json')) as f:
        stub_str = f.read()
    try:
        return json.loads(stub_str)
    except:
        raise Exception('Invalid JSON')


def get_sqs_message_stub():
    with open(path.join(ROOT_DIR, 'tests/datasources/events/sqs/sqs.message.stub.json')) as f:
        stub_str = f.read()
    try:
        return json.loads(stub_str)
    except:
        raise Exception('Invalid JSON')


def get_sqs_event_sample():
    with open(path.join(ROOT_DIR, 'tests/datasources/events/sqs/delivery-time-simulator-row-sqs-event.json')) as f:
        event_str = f.read()
    try:
        return json.loads(event_str)
    except:
        raise Exception('Invalid JSON')
