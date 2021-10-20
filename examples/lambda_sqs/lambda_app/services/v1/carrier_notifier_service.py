import json

from lambda_app import APP_NAME, APP_VERSION, APP_ARCH_VERSION, helper
from lambda_app.decorators import SQSEvent
from lambda_app.decorators.events import SQSRecord
from lambda_app.events.tracker import EventTracker
from lambda_app.helper import generate_hash
from lambda_app.logging import get_logger
from lambda_app.repositories.mysql.ocoren_repository import OcorenRepository
from lambda_app.vos.ocoren import OcorenVO


class CarrierNotifierService:
    def __init__(self, logger=None, repository=None):
        # logger
        self.logger = logger if logger is not None else get_logger()

        self.repository = repository if repository is not None else OcorenRepository()
        self.repository.debug = True

    def process(self, sqs_event):
        result = True

        self.logger.info('---------------------------------------------------------------')
        self.logger.info('{} - {} - {}'.format(APP_NAME, APP_VERSION, APP_ARCH_VERSION))
        self.logger.info('---------------------------------------------------------------')
        self.logger.info('Starting...')

        event_tracker = EventTracker(self.logger)
        event_hash = None

        records = self.get_records_from_sqs_event(sqs_event)
        if records is not None:
            process_counter = 0
            for record in records:
                process_counter += 1
                event = self._read_event(record)
                if event is None:
                    raise Exception('Event is None')
                event_hash = event['hash'] if 'hash' in event else generate_hash(event)

                self.logger.info('Event: {}'.format(event))

                try:
                    event_tracker.track(event_hash, event)
                    # todo implementar lógica aqui
                    # aqui temos um simples exemplo de created
                    # TODO compatibilidade com a API (arrumar depois)
                    if 'data' in event:
                        event = event['data']
                    event_vo = OcorenVO(event)
                    self.logger.info('event_vo: {}'.format(event_vo.to_dict()))
                    created = self.repository.create(event_vo)
                    if not created:
                        result = False

                except Exception as err:
                    self.logger.error(err)
                    event_tracker.track_error(event_hash, event, err)
                    result = False

        event_tracker.track(event_hash, {'result': result})
        self.logger.info('Finishing the process')
        return result

    def _read_event(self, record):
        event_body = None
        try:
            if isinstance(record, dict):
                event_body = json.loads(record['body'])
            elif isinstance(record.body, str):
                event_body = json.loads(record.body)
            else:
                event_body = record.body
        except Exception as err:
            self.logger.error(err)
        return event_body

    def get_records_from_sqs_event(self, sqs_event):
        records = []
        try:
            if isinstance(sqs_event, SQSEvent):
                self.logger.info("SQSEvent instance")
                if not helper.empty(sqs_event.to_dict()):
                    try:
                        sqs_event_dict = sqs_event.to_dict()
                        if 'Records' in sqs_event_dict:
                            sqs_event_dict = sqs_event_dict['Records']
                        for record in sqs_event_dict:
                            records.append(record)
                    except Exception as err:
                        self.logger.error(err)
                        records.append(sqs_event.to_dict())
            elif isinstance(sqs_event, SQSRecord):
                self.logger.info("SQSRecord instance")
                if not helper.empty(sqs_event.to_dict()):
                    records.append(sqs_event)
        except Exception as err:
            self.logger.error(err)
            if isinstance(sqs_event, SQSEvent) or isinstance(sqs_event, SQSRecord):
                self.logger.error(sqs_event.__dict__)
            else:
                try:
                    self.logger.error(json.dumps(sqs_event))
                except Exception as err:
                    self.logger.error(err)
                    self.logger.error(str(sqs_event))
        return records
