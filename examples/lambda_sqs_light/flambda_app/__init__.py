"""
Main module for Flambda APP
Version: 1.0.0
"""
import os


def load_projectrc(projectrc_filepath):
    """
    Load the values of .projectrc file
    """
    from dotenv import dotenv_values
    return dotenv_values(projectrc_filepath)


if __package__:
    current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
else:
    current_path = os.path.abspath(os.path.dirname(__file__))

env_vars = {}
projectrc_file = os.path.join(current_path, '.projectrc')

# inside of a docker the name of folder is app
PROJECT_NAME = os.path.basename(current_path).replace('_', '-')

if not current_path[-1] == '/':
    current_path += '/'

if os.path.exists(projectrc_file):
    env_vars = load_projectrc(projectrc_file)

APP_NAME = env_vars['APP_NAME'] if 'APP_NAME' in env_vars else PROJECT_NAME
APP_VERSION = env_vars['APP_VERSION'] if 'APP_VERSION' in env_vars else '1.0.0'
APP_ARCH_VERSION = env_vars['APP_ARCH_VERSION'] if 'APP_ARCH_VERSION' in env_vars else 'v1'
