"""
Boot module for Flambda App
Version: 1.0.5
"""
import json
import logging
import os
import sys

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
    from flambda_app import APP_NAME
    try:
        from flambda_app.logging import LoggerProfile, get_logger, get_log_level, reset as reset_logger
        logger = get_logger(LoggerProfile.CONSOLE)
        logger.setLevel(get_log_level())
        reset_logger()

    except Exception as err:
        import logging
        log_name = APP_NAME
        logger = logging.getLogger(log_name)
        logger.error('load_env: Unable to load logger: {}'.format(err))
    return logger


def load_dot_env(env='development', force=False, debug=False):
    result = False
    from dotenv import dotenv_values
    # env default value
    if env is None:
        env = 'development'

    logger = get_internal_logger()

    global _LOADED, _ENV_KEYS, _DEFAULT_ENV_CONFIGS
    if not _LOADED or force:
        if debug:
            logger.info('Boot - load_dot_env - Loading env: {}'.format(env))

        # Default
        for k, v in _DEFAULT_ENV_CONFIGS.items():
            _ENV_KEYS.append(k)
            if k == 'APP_ENV':
                v = env
            # se não estiver setado ainda no env, cria o valor default
            if k not in os.environ:
                os.environ[k] = v

        config_path = '{}env/{}.env'.format(current_path, env)
        if os.path.isfile(config_path):
            env_vars = dotenv_values(config_path)

            for k, v in env_vars.items():
                _ENV_KEYS.append(k)
                os.environ[k] = v
            _LOADED = True
            result = True
        else:
            # try with development
            if env == 'dev':
                result = load_dot_env('development')
            else:
                # Try to load via secrets manager
                result = load_secrets(env=env)
                if result:
                    _LOADED = True
                else:
                    if debug:
                        logger.error('Unable to load config - secrets scenario')

    else:
        result = True
    return result


def load_secrets(env='staging', debug=False):
    global _ENV_KEYS
    from flambda_app.aws.secrets import Secrets
    from flambda_app import APP_NAME
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
        if debug:
            logger.error(err)

    if secrets_dict is not None:
        for k, v in secrets_dict.items():
            os.environ[k] = v
        result = True

    return result


def load_env(env='dev', force=False, debug=False):
    result = False
    # env default value
    if env is None:
        env = 'dev'

    logger = get_internal_logger()
    # só para testes
    logger.level = logging.INFO

    global _LOADED, _ENV_KEYS, _DEFAULT_ENV_CONFIGS
    if not _LOADED or force:

        chalice_config_path = '{}.chalice/config.json'.format(current_path)

        if debug:
            logger.info('Boot - load_env - Loading env: {}'.format(env))
            logger.info('Boot - load_env - chalice_config_path: {}'.format(chalice_config_path))

        # todo tratar cenários novos que não serão baseado em arquivos
        if os.path.isfile(chalice_config_path):
            if debug:
                logger.info('Boot - load_env - Chalice retro compatibility')
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
                if isinstance(env_vars, dict):
                    for k, v in env_vars.items():
                        _ENV_KEYS.append(k)
                        # não remover, senão vai sobrescrever as variaveis pelo arquivo
                        # config.json, sabemos que em ambientes como de prod isso é ruim
                        if k not in os.environ:
                            os.environ[k] = v
                            if debug:
                                logger.info(
                                    'Boot - load_env - setting env configs.stages.env k = v {} = {}'.format(k, v))
                        else:
                            if debug:
                                logger.info(
                                    'Boot - load_env - ENV k = v {} = {}'.format(k, os.environ[k]))
                    _LOADED = True
                    result = True
                else:
                    if debug:
                        logger.error(
                            "Boot - load_env - Unable to load env_vars from chalice: {}".format(
                                env_vars))
            else:
                # solution for projects with development flag instead of dev
                if env == 'dev':
                    result = load_env('development')
                else:
                    if debug:
                        logger.error('Unable to load config - chalice scenario')
                    _LOADED = False
            # close the file
            file.close()

        else:
            if debug:
                logger.info('Boot - load_env - Flambda compatibility')
            # todo implementar uma logica melhor para identificar se as variáveis do projeto estão
            # print(os.environ['API_SERVER'])

            # registradas
            if 'APP_QUEUE' in os.environ or 'DB_HOST' in os.environ or 'APP_BUCKET' in os.environ:
                _LOADED = True
                if debug:
                    logger.info('Boot - load_env - Environment variables already defined')
                    # logger.info('APP_QUEUE = {}'.format('APP_QUEUE' in os.environ))
                    # logger.info('API_SERVER = {}'.format('API_SERVER' in os.environ))
                    # logger.info('DB_HOST = {}'.format('DB_HOST' in os.environ))
                    # logger.info('APP_BUCKET = {}'.format('APP_BUCKET' in os.environ))
                    # logger.info('FLASK_ENV = {}'.format('FLASK_ENV' in os.environ))
                    result = True
                # logger.info(os.environ)
            else:
                if debug:
                    logger.error('Boot - load_env - Unable to load config - environment scenario')
                _LOADED = False

        # Carrega as variaves default, só seta valores caso não tenham sido carregadas via
        # arquivo ou env (secrets)
        for k, v in _DEFAULT_ENV_CONFIGS.items():
            _ENV_KEYS.append(k)
            if k == 'APP_ENV':
                v = env
            # se não estiver setado ainda no env, cria o valor default
            if k not in os.environ:
                os.environ[k] = v
    else:
        result = True
    return result


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
    logger.info('Environment: %s' % get_environment())
    # logger.info('Host: %s' % os.getenv('APP_HOST'))
    # logger.info('Port: %s' % os.getenv('APP_PORT'))
    # logger.info('Database: %s' % os.getenv('DB_HOST'))
    logger.info('Log Level: %s' % os.getenv('LOG_LEVEL'))
    logger.info('Debug: %s' % os.getenv('DEBUG'))


def get_environment():
    environment = 'development'
    if 'ENVIRONMENT' in os.environ:
        environment = os.environ['ENVIRONMENT']
    elif 'ENVIRONMENT_NAME' in os.environ:
        environment = os.environ['ENVIRONMENT_NAME']
    elif 'APP_ENV' in os.environ:
        environment = os.environ['APP_ENV']

    if environment == "dev":
        environment = "development"

    return environment


# register the vendor folder
register_vendor()

# load env
loaded = load_env(get_environment(), debug=True)
if not loaded:
    loaded = load_dot_env(get_environment(), debug=True)
