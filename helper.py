import subprocess
import os
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import logging

_filePath = os.path.dirname(os.path.realpath(__file__))
_bot = None
_admins = []
_module_manager = None

_logger = logging.getLogger(__name__)

restart_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Restart now", callback_data="restart")]])


def init(bot, config, module_manager):
    global _bot
    global _module_manager
    global _admins

    _bot = bot
    _module_manager = module_manager

    _admins = config['Telegram']['Admins']
    _admins = _admins.split(',')


def get_file_path():
    return _filePath


def get_admins():
    return _admins


def execute(cmd):
    _logger.debug("Executing System Call %s",cmd)
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             shell=True)
    out = process.stdout.decode('utf-8')
    err = process.stderr.decode('utf-8')
    return out, err


def get_git_branch():
    mod = _module_manager.get_module_by_name('git')
    if mod is None:
        return "No Git!"
    else:
        return mod.get_current_branch()


def send_admins(msg, except_this='', silent=False):
    _logger.info("Send to all Admins (silent? %r): %s", silent, msg)
    for admin in _admins:
        if admin != except_this and len(admin) > 0:
            _bot.sendMessage(admin, msg, disable_notification=silent)
