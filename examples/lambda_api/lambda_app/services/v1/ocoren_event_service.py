from lambda_app.config import get_config
from lambda_app.aws.sqs import SQSEvents
from lambda_app.logging import get_logger
from lambda_app.vos.events import EventVO


class OcorenEventService:
    def __init__(self, logger=None, config=None, sqs_events=None):
        """
                :param (logging.Logger) logger:
                :param (flask_app.config.Configuration) config:
                :param sqs_events:
                """
        # logger
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # sqs event service
        self.sqs_events = sqs_events if sqs_events is not None else SQSEvents()
        # queue_url
        self.queue = self.config.APP_QUEUE
        # exception
        self.exception = None
        # response
        self.response = None

    def send_event(self, event_vo: EventVO):
        result = True
        # convert to sale event
        self.logger.info('Event received: {}'.format(event_vo.to_json()))
        # create the json message
        message = event_vo.to_json()
        self.logger.info('Sending message to queue: {}'.format(self.queue))
        self.logger.info('message: {}'.format(message))
        # send the message
        self.response = self.sqs_events.send_message(message, self.queue)
        if not self.response:
            self.exception = self.sqs_events.exception
            result = False
        else:
            self.logger.info('Response: {}'.format(self.response))

        return result
