import json
import os
import sys

from lambda_app import APP_NAME

if __package__:
    current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
else:
    current_path = os.path.abspath(os.path.dirname(__file__))

if not current_path[-1] == '/':
    current_path += '/'

ROOT_DIR = current_path
_LOADED = False
_ENV_KEYS = []

try:
    import chalicelib

    APP_TYPE = 'Chalice'
except Exception as err:
    APP_TYPE = 'Flask'

_DEFAULT_ENV_CONFIGS = {
    "APP_ENV": "development",
    "DEBUG": "true",
    "LOG_LEVEL": "info",
    "APP_TYPE": APP_TYPE
}


def set_root_dir(root_dir):
    global ROOT_DIR
    ROOT_DIR = root_dir


def is_loaded():
    global _LOADED
    return _LOADED


def reset():
    global _LOADED, _ENV_KEYS
    _LOADED = False
    _ENV_KEYS = []


def get_env_keys():
    global _ENV_KEYS
    return _ENV_KEYS


def get_internal_logger():
    try:
        from lambda_app.logging import get_logger
        logger = get_logger()
    except Exception as err:
        print('load_env: Unable to load logger: {}'.format(err))
        import logging
        log_name = APP_NAME
        logger = logging.getLogger(log_name)
    return logger


def load_dot_env(env='development', force=False):
    from dotenv import dotenv_values
    # env default value
    if env is None:
        env = 'development'

    logger = get_internal_logger()

    global _LOADED, _ENV_KEYS
    if not _LOADED or force:
        logger.info('Boot - Loading env: {}'.format(env))

        # Default
        for k, v in _DEFAULT_ENV_CONFIGS.items():
            _ENV_KEYS.append(k)
            if k == 'APP_ENV':
                v = env
            os.environ[k] = v

        config_path = '{}env/{}.env'.format(current_path, env)
        if os.path.isfile(config_path):
            env_vars = dotenv_values(config_path)

            for k, v in env_vars.items():
                _ENV_KEYS.append(k)
                os.environ[k] = v
            _LOADED = True
        else:
            # try with development
            if env == 'dev':
                load_dot_env('development')
            else:
                # Try to load via secrets manager
                result = load_secrets(env=env)
                if result:
                    _LOADED = True
                else:
                    logger.error('Unable to load config')

    else:
        pass


def load_secrets(env='staging'):
    global _ENV_KEYS
    from lambda_app.aws.secrets import Secrets
    logger = get_internal_logger()
    result = False

    logger.info('Boot - Loading env by secret manager: {}'.format(env))
    app_name = os.environ["APP_NAME"] if "APP_NAME" in os.environ else APP_NAME
    secret_name = app_name + "-" + env
    try:
        logger.info('secret name: {}'.format(secret_name))
        secrets_dict = Secrets().get_secrets(secret_name=secret_name)
    except Exception as err:
        secrets_dict = None
        logger.error(err)

    if secrets_dict is not None:
        for k, v in secrets_dict.items():
            os.environ[k] = v
        result = True

    return result


def load_env(env='dev', force=False):
    # env default value
    if env is None:
        env = 'dev'

    logger = get_internal_logger()

    global _LOADED, _ENV_KEYS
    if not _LOADED or force:

        logger.info('Boot - Loading env: {}'.format(env))

        # Default
        for k, v in _DEFAULT_ENV_CONFIGS.items():
            _ENV_KEYS.append(k)
            if k == 'APP_ENV':
                v = env
            os.environ[k] = v

        chalice_config_path = '{}.chalice/config.json'.format(current_path)

        if os.path.isfile(chalice_config_path):
            file = open(chalice_config_path, 'r')
            data = file.read()
            configs = json.loads(data)

            # solution for projects with integration tests
            if env not in configs['stages'] and env == 'integration':
                env = 'staging'
            # solution for projects with dev flag instead of development
            if env not in configs['stages'] and env == 'development':
                env = 'dev'

            if env in configs['stages']:
                env_vars = configs['stages'][env]['environment_variables']
                for k, v in env_vars.items():
                    _ENV_KEYS.append(k)
                    os.environ[k] = v
                _LOADED = True
            else:
                # solution for projects with development flag instead of dev
                if env == 'dev':
                    load_env('development')
                else:
                    logger.error('Unable to load config')
                    _LOADED = False
            # close the file
            file.close()
        else:
            logger.error('Unable to load config')
            _LOADED = False
    else:
        pass


def register_vendor():
    vendor_path = current_path + "vendor"
    # print(vendor_path)
    if not os.path.isdir(vendor_path):
        vendor_path = current_path + "/vendor"
        # print(vendor_path)

    sys.path.insert(0, vendor_path)


def register_path(path):
    if os.path.isdir(path):
        sys.path.insert(0, path)


def print_env(app, logger):
    logger.info('Environment: %s' % os.getenv('APP_ENV'))
    # logger.info('Host: %s' % os.getenv('APP_HOST'))
    # logger.info('Port: %s' % os.getenv('APP_PORT'))
    # logger.info('Database: %s' % os.getenv('DB_HOST'))
    logger.info('Log Level: %s' % os.getenv('LOG_LEVEL'))
    logger.info('Debug: %s' % os.getenv('DEBUG'))


register_vendor()
