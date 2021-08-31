import os

from lambda_app.boot import load_dot_env,register_vendor
register_vendor()
# load env
from lambda_app.config import get_config
from lambda_app.services.v1.carrier_notifier_service import CarrierNotifierService

env = os.environ['ENVIRONMENT_NAME'] if 'ENVIRONMENT_NAME' in os.environ else None
load_dot_env(env)

from lambda_app.logging import get_logger
from lambda_app import APP_NAME, APP_VERSION, helper
from lambda_app.lambda_flask import LambdaFlask

# config
config = get_config()
# debug
debug = helper.debug_mode()
# logger
logger = get_logger()

app = LambdaFlask(APP_NAME)

# general vars
APP_QUEUE = config.APP_QUEUE


@app.on_sqs_message(queue=APP_QUEUE, batch_size=1)
def index(event):
    body = {"app": '%s:%s' % (APP_NAME, APP_VERSION)}
    logger.info('Env: {} App Info: {}'.format(env, body))
    logger.info('Handling event: {}'.format(event.to_dict()))

    service = CarrierNotifierService()
    result = service.process(event)

    return result
