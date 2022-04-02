from flambda_app.config import get_config
from flambda_app.aws.sqs import SQS
from flambda_app.logging import get_logger
from flambda_app.vos.events import EventVO


class OcorenEventService:
    def __init__(self, logger=None, config=None, sqs=None):
        """
                :param (logging.Logger) logger:
                :param (flask_app.config.Configuration) config:
                :param sqs:
                """
        # logger
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # sqs event service
        self.sqs = sqs if sqs is not None else SQS()
        # queue_url
        self.queue = self.config.get('APP_QUEUE', None)
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
        self.response = self.sqs.send_message(message, self.queue)
        if not self.response:
            self.exception = self.sqs.exception
            result = False
        else:
            self.logger.info('Response: {}'.format(self.response))

        return result
