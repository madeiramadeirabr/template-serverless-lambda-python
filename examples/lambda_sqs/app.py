"""This is the main file of the lambda application

This module contains the handler method
"""
import boot
from lambda_app.lambda_flask import LambdaFlask
from lambda_app import APP_NAME, APP_VERSION
from lambda_app.logging import get_logger, set_debug_mode
from lambda_app.services.v1.carrier_notifier_service import CarrierNotifierService
from lambda_app.config import get_config
from lambda_app import helper


# load env
ENV = helper.get_environment()
boot.load_dot_env(ENV)

# config
CONFIG = get_config()
# debug
DEBUG = helper.debug_mode()
# Logger
LOGGER = get_logger()

APP = LambdaFlask(APP_NAME)
# override the APP logger
APP.logger = LOGGER
# override the log configs
if DEBUG:
    # override to the level desired
    set_debug_mode(LOGGER)

# general vars
APP_QUEUE = CONFIG.APP_QUEUE


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
