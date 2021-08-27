import json
from os import path

from tests import ROOT_DIR


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