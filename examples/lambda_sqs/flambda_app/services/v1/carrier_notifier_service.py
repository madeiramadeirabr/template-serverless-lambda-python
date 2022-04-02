"""
Carrier Notifier Service for Flambda APP
Version: 1.0.0
"""
from flambda_app import APP_NAME, APP_VERSION, APP_ARCH_VERSION
from flambda_app.events.tracker import EventTracker
from flambda_app.events_helper import get_records_from_sqs_event, read_event
from flambda_app.helper import generate_hash
from flambda_app.logging import get_logger
from flambda_app.repositories.v1.mysql.ocoren_repository import OcorenRepository
from flambda_app.repositories.v1.redis.product_repository import ProductRepository
from flambda_app.vos.ocoren import OcorenVO


class CarrierNotifierService:
    def __init__(self, logger=None, repository=None):
        # logger
        self.logger = logger if logger is not None else get_logger()

        self.repository = repository if repository is not None else OcorenRepository()
        self.redis_repository = ProductRepository()
        self.repository.debug = True

    def process(self, sqs_event):
        result = True

        self.logger.info('---------------------------------------------------------------')
        self.logger.info('{} - {} - {}'.format(APP_NAME, APP_VERSION, APP_ARCH_VERSION))
        self.logger.info('---------------------------------------------------------------')
        self.logger.info('Starting...')

        event_tracker = EventTracker(self.logger)
        event_hash = None

        records = get_records_from_sqs_event(sqs_event, self.logger)
        if records is not None:
            process_counter = 0
            for record in records:
                process_counter += 1
                event = read_event(record, self.logger)
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

                    try:
                        self.redis_repository.create("event_{}".format(event_hash), str(event_vo.to_dict()))
                    except Exception as err:
                        self.logger.error("Already in redis")
                        self.logger.error(err)
                    # self.redis_repository.list(where="*")

                    if not created:
                        result = False

                except Exception as err:
                    self.logger.error(err)
                    event_tracker.track_error(event_hash, event, err)
                    result = False

        event_tracker.track(event_hash, {'result': result})
        self.logger.info('Finishing the process')
        return result
