import os
from dotenv import dotenv_values

if __package__:
    current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
else:
    current_path = os.path.abspath(os.path.dirname(__file__))

env_vars = {}
projectrc_file = current_path + '.projectrc'

PROJECT_NAME = os.path.basename(current_path).replace('_', '-')

if not current_path[-1] == '/':
    current_path += '/'

if os.path.exists(projectrc_file):
    env_vars = dotenv_values(projectrc_file)

APP_NAME = env_vars['APP_NAME'] if 'APP_NAME' in env_vars else PROJECT_NAME
APP_VERSION = env_vars['APP_VERSION'] if 'APP_VERSION' in env_vars else '1.0.0'
APP_ARCH_VERSION = env_vars['APP_ARCH_VERSION'] if 'APP_ARCH_VERSION' in env_vars else 'v1'
