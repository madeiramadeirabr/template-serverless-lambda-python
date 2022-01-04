import json
from os import path

from tests import ROOT_DIR


def get_delivery_time_simulator_event_sample():
    with open(path.join(ROOT_DIR, 'tests/datasources/events/sqs/delivery-time-simulator-row-sqs-event.json')) as f:
        event_str = f.read()
    try:
        return json.loads(event_str)
    except:
        raise Exception('Invalid JSON')


def get_cancelamento_event():
    with open(path.join(ROOT_DIR, 'tests/datasources/events/sqs/ocorens/cancelamento.event.json')) as f:
        event_str = f.read()
    try:
        return json.loads(event_str)
    except:
        raise Exception('Invalid JSON')


def get_cancelamento_error_event():
    with open(path.join(ROOT_DIR, 'tests/datasources/events/sqs/ocorens/cancelamento.event.with.error.json')) as f:
        event_str = f.read()
    try:
        return json.loads(event_str)
    except:
        raise Exception('Invalid JSON')


def get_cancelamento_quote_error_event():
    with open(
            path.join(ROOT_DIR, 'tests/datasources/events/sqs/ocorens/cancelamento.event.with.error.quotes.json')) as f:
        event_str = f.read()
    try:
        return json.loads(event_str)
    except:
        raise Exception('Invalid JSON')
