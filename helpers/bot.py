import logging
import config
import telepot

_logger = logging.getLogger(__name__)
_bot = None

try:
    _admins = config.get_telegram_config()['Admins']
    _admins = _admins.split(',')
except KeyError as e:
    err_msg = "Cannot load Admins from Config! Key {} does not exist".format(e)
    _logger.error(err_msg)
    raise RuntimeError(err_msg)


def get_admins():
    return _admins


def get_bot():
    global _bot
    if _bot is None:
        _logger.debug('Creating new Bot')
        _bot = telepot.Bot(config.get_telegram_config()['Token'])
    return _bot


def send_admins(msg, except_this='', silent=False):
    _logger.info("Send to all Admins (silent? %r): %s", silent, msg)
    bot = get_bot()
    for admin in _admins:
        if admin != except_this and len(admin) > 0:
            bot.sendMessage(admin, msg, disable_notification=silent)
