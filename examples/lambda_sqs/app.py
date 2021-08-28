import os

from flask_app.boot import load_dot_env
# load env
from flask_app.config import get_config

env = os.environ['ENVIRONMENT_NAME'] if 'ENVIRONMENT_NAME' in os.environ else None
load_dot_env(env)

from flask_app.logging import get_logger
from flask_app import APP_NAME, APP_VERSION, helper
from flask_app.lambda_app import LambdaApp

# config
config = get_config()
# debug
debug = helper.debug_mode()
# logger
logger = get_logger()

app = LambdaApp(__name__)

# general vars
APP_QUEUE = config.APP_QUEUE


@app.on_sqs_message(queue=APP_QUEUE, batch_size=1)
def sqs_handler(event):
    body = {"app": '%s:%s' % (APP_NAME, APP_VERSION)}
    logger.info('Env: {} App Info: {}'.format(env, body))
    logger.info('Handling event: {}'.format(event.to_dict()))

    result = True

    return result
