"""This is the main file of the lambda application

This module contains the handler method
"""
import boot
from flambda_app.flambda import Flambda
from flambda_app import APP_NAME, APP_VERSION
from flambda_app.logging import get_logger, set_debug_mode
from flambda_app.services.v1.carrier_notifier_service import CarrierNotifierService
from flambda_app.config import get_config
from flambda_app import helper


# load directly by boot
ENV = boot.get_environment()
# boot.load_dot_env(ENV)


# config
CONFIG = get_config()
# debug
DEBUG = helper.debug_mode()

# keep in this order, the app generic stream handler will be removed
APP = Flambda(APP_NAME)
# Logger
LOGGER = get_logger(force=True)
# override the APP logger
APP.logger = LOGGER
# override the log configs
if DEBUG:
    # override to the level desired
    set_debug_mode(LOGGER)

# general vars
APP_QUEUE = CONFIG.get('APP_QUEUE')


@APP.on_sqs_message(queue=APP_QUEUE, batch_size=1)
def index(event):
    """
    Lambda handler
    :param event:
    :return:
    :rtype: str
    """
    body = {"app": '%s:%s' % (APP_NAME, APP_VERSION)}
    LOGGER.info('Env: {} App Info: {}'.format(ENV, body))
    LOGGER.info('Handling event: {}'.format(event.to_dict()))

    service = CarrierNotifierService()
    result = service.process(event)

    return result
