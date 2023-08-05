import os
from functools import partial
import configparser
from contextlib import contextmanager
from jarvis_cli.exceptions import JarvisCliConfigError

JARVIS_CLI_CONFIG_DIR = os.path.join(os.environ["HOME"], ".jarvis")
JARVIS_CLI_CONFIG_PATH = os.path.join(JARVIS_CLI_CONFIG_DIR, "cli_config.ini")
JARVIS_CLI_DEFAULT_SNAPSHOTS_DIR = os.path.join(JARVIS_CLI_CONFIG_DIR, "snapshots")


@contextmanager
def create_config(environment, config_path):
    config = configparser.ConfigParser()
    config.add_section(environment)

    yield config[environment]

    with open(config_path, 'w') as f:
        config.write(f)

def get_config_map(environment, config_path):
    config = configparser.ConfigParser()

    if config.read(config_path):
        return config[environment]
    else:
        raise JarvisCliConfigError("Configuration not setup: {0}".format(config_path))

def _get_config_param(key, config_map, expected_type=str):
    return expected_type(config_map[key])

get_api_url = partial(_get_config_param, "api_url")
get_jarvis_data_directory = partial(_get_config_param, "data_directory")
get_jarvis_snapshots_directory = partial(_get_config_param, "snapshots_directory")
get_author = partial(_get_config_param, "author")

def get_client_connection(config_map):
    return get_api_url(config_map).strip("/")

def _set_config_param(key, config_map, value, expected_type=str):
    if expected_type != type(value):
        raise TypeError("Expecting {0} to be an {1}".format(key, expected_type))
    # ConfigParser only allows setting string values. The expected_type is used
    # as a value validation.
    config_map[key] = str(value)

set_host = partial(_set_config_param, "host")
set_port = partial(_set_config_param, "port", expected_type=int)
set_jarvis_data_directory = partial(_set_config_param, "data_directory")
set_jarvis_snapshots_directory = partial(_set_config_param, "snapshots_directory")
set_author = partial(_set_config_param, "author")
