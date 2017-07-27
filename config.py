import configparser
import helper
import logging

_CONFIG_URL = helper.get_file_path() + "/config.ini"

logging.info("INIT Config at Path " + _CONFIG_URL)

config = configparser.ConfigParser()
config.read(_CONFIG_URL)


def get_telegram_config():
    return config['Telegram']


def get_module_config():
    return config['Modules']
