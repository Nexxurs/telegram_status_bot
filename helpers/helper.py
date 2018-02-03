import logging
from pathlib import Path
import sys
import modules
from helpers import bot as bot_helper

_logger = logging.getLogger(__name__)

_botRootPath = (Path(__file__) / '..' / '..').resolve()
_logger.debug("Bot Root Path: {}".format(_botRootPath))

_module_manager = None

def config_logger(log_level=logging.INFO, to_File=True):
    root = logging.getLogger('')
    root.setLevel(log_level)
    for h in root.handlers:
        root.removeHandler(h)

    if to_File:
        log_dir = _botRootPath / 'log'
        log_dir.mkdir(exist_ok=True)

        file_handler = logging.FileHandler(str(log_dir / 'telegram.log'))
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        file_handler.setLevel(logging.INFO)
        root.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(levelname)s - %(name)s - %(message)s'))
    stream_handler.setLevel(logging.DEBUG)
    root.addHandler(stream_handler)

    _logger.debug('Logger Config Done')


def getBotRoot():
    return str(_botRootPath)


def getBotRootPath():
    return _botRootPath


def can_connect(hostname):
    import socket
    try:
        host = socket.gethostbyname(hostname)
        socket.create_connection((host, 80), 2)
        return True
    except socket.gaierror:
        return False


def get_module_manager():
    global _module_manager
    if _module_manager is None:
        _logger.debug('Creating new Module Manager')
        _module_manager = modules.ModuleManager(bot=bot_helper.get_bot())

    return _module_manager
