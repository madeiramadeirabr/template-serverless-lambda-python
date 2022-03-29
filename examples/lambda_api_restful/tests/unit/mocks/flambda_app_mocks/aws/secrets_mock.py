"""
AWS Secrets Module Mock for test resources
Version: 1.0.0
"""
from os import path
from unittest.mock import Mock

from dotenv import dotenv_values

from flambda_app import APP_NAME
from flambda_app.aws.secrets import Secrets
from tests import ROOT_DIR


def get_secrets(secret_name):
    config_path = path.join(ROOT_DIR, 'env/development.env')
    env_vars = dotenv_values(config_path)
    env_data = {}
    for k, v in env_vars.items():
        env_data[k] = v
    # sobreescreve
    env_data['APP_ENV'] = str(secret_name).replace(APP_NAME + '-', '')
    return env_data


secrets_mock = Mock(Secrets)
secrets_mock.connect.side_effect = lambda retry=False: True
secrets_mock.get_secrets.side_effect = lambda secret_name: get_secrets(secret_name)


def secrets_mock_caller():
    return secrets_mock
