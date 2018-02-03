import configparser
import os
import logging

_CONFIG_URL = os.path.dirname(os.path.realpath(__file__))
_CONFIG_URL = os.path.join(_CONFIG_URL, "config.ini")

_logger = logging.getLogger(__name__)
_logger.info("INIT Config at Path " + _CONFIG_URL)

if not os.path.isfile(_CONFIG_URL):
    #TODO hier FirstStart anlegen!
    err_msg = "Config File does not exist at {}!".format(_CONFIG_URL)
    _logger.error(err_msg)
    raise RuntimeError(err_msg)

config = configparser.ConfigParser()
config.read(_CONFIG_URL)


def get_telegram_config():
    return config['Telegram']


def get_module_config():
    return config['Modules']
