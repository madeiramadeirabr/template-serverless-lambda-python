from flambda_app.config import get_config
from flambda_app.database.redis import RedisConnector
from flambda_app.enums.events import EventType
from flambda_app.enums.messages import MessagesEnum
from flambda_app.events.tracker import EventTracker
from flambda_app.exceptions import ApiException
from flambda_app.helper import generate_hash
from flambda_app.logging import get_logger
from flambda_app.services.v1.ocoren_event_service import OcorenEventService
from flambda_app.vos.events import EventVO


def get_event_type(event_vo: EventVO):
    if isinstance(event_vo.type, EventType):
        return event_vo.type
    else:
        current_event = EventType.from_value(event_vo.type)
        if current_event == EventType.OCOREN_EVENT:
            return EventType.OCOREN_EVENT
        else:
            return EventType.UNKNOWN


class EventManager:
    def __init__(self, event_service=None, logger=None, config=None, redis_connector=None, event_tracker=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # database connection
        self.redis_connector = redis_connector if redis_connector is not None else RedisConnector()
        self.event_service = event_service if event_service is not None else OcorenEventService(self.logger)
        self.event_tracker = event_tracker if event_tracker is not None else EventTracker(self.logger)
        self.exception = None

    def process(self, event_vo: EventVO):
        if self.redis_connector is None:
            self.logger.error('Redis not connected')
            self.exception = Exception('Redis not connected')
            result = False
            return result

        if self.event_service is None:
            raise Exception("Service must be informed")

        event_type = get_event_type(event_vo)
        if event_vo.hash is None:
            event_vo.hash = generate_hash(event_vo)

        self.event_tracker.track(event_vo.hash, event_vo.to_dict())
        self.logger.info('---------------------------------------------------------------')
        self.logger.info('Event details')
        self.logger.info('---------------------------------------------------------------')
        self.logger.info('event_type informed: {}'.format(event_vo.type))
        self.logger.info('event_type: {}'.format(event_type))
        self.logger.info('event_hash: {}'.format(event_vo.hash))
        self.logger.info('event_date: {}'.format(event_vo.date))
        self.logger.info('event_data: {}'.format(event_vo.data))
        self.logger.info('---------------------------------------------------------------')

        response = self.search_event(event_type, event_vo)
        if response is None:
            self.logger.info('Event not registered')
            result = self.send_event(event_type, event_vo)
        else:
            self.logger.info('Event already registered')
            result = False
            self.exception = ApiException(MessagesEnum.EVENT_ALREADY_REGISTERED_ERROR)

        self.event_tracker.track(event_vo.hash, {'result': result})

        return result

    def send_event(self, event_type, event_vo):
        result = True

        self.logger.info('Service: {}'.format(str(self.event_service)))

        event_sent = self.event_service.send_event(event_vo)
        if not event_sent:
            self.logger.error(self.event_service.exception)
            self.exception = ApiException(MessagesEnum.EVENT_NOT_SENT_ERROR)
            result = False

        return result

    def search_event(self, event_type, event_vo):
        response = None
        # try:
        #     key = '%s:%s' % (event_type, event_vo.hash)
        #     response = self.event_repository.get(key)
        # except Exception as err:
        #     self.logger.error(err)
        return response

    def save_event(self, event_type, event_vo):
        response = None
        # key = '{}:{}'.format(event_type, event_vo.hash)
        # try:
        #     response = self.event_repository.create(key, event_vo.to_json())
        # except Exception as err:
        #     self.logger.error(err)
        #     if isinstance(err, DatabaseException):
        #         try:
        #             response = self.event_repository.update(key, event_vo.to_json())
        #         except Exception as err:
        #             self.logger.error(err)
        return response
