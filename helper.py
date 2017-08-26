import subprocess
import os
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import config
import modules
import socket
import sys

_filePath = os.path.dirname(os.path.realpath(__file__))
_bot = None
_module_manager = None
_git_branch = None

restart_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Restart now", callback_data="restart")]])

_admins = config.get_telegram_config()['Admins']
_admins = _admins.split(',')

_logger = logging.getLogger(__name__)


def init(module_manager):
    global _module_manager
    _module_manager = module_manager


def config_logger(log_level=logging.INFO):
    root = logging.getLogger('')
    root.setLevel(log_level)
    for h in root.handlers:
        root.removeHandler(h)

    log_dir = "log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    file_handler = logging.FileHandler(log_dir + '/telegram.log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
    file_handler.setLevel(logging.INFO)
    root.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(levelname)s - %(name)s - %(message)s'))
    stream_handler.setLevel(logging.DEBUG)
    root.addHandler(stream_handler)


def get_file_path():
    return _filePath


def get_admins():
    return _admins


def get_bot():
    global _bot
    if _bot is None:
        _bot = telepot.Bot(config.get_telegram_config()['Token'])
    return _bot


def get_module_manager():
    global _module_manager
    if _module_manager is None:
        _module_manager = modules.ModuleManager(bot=_bot)

    return _module_manager


def execute(cmd):
    _logger.debug("Executing System Call %s", cmd)
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             shell=True)
    out = process.stdout.decode('utf-8')
    err = process.stderr.decode('utf-8')
    return out, err


def get_git_branch():
    global _git_branch
    if _git_branch is None:
        mod = _module_manager.get_module_by_name('git')
        if mod is None:
            _git_branch = "No Git!"
        else:
            _git_branch = mod.get_current_branch()

    return _git_branch


def create_header(version='No Version'):
    if _bot is None:
        raise ReferenceError("Cannot create Header without Bot Context!")

    me = _bot.getMe()
    string = ""

    string = string + "##############################################################\n"
    string = string + "   Hostname:  " + socket.gethostname() + "\n"

    model, model_err = execute('cd ' + get_file_path() + ' & scripts/model.sh')
    if len(model) > 0:
        string = string + "   " + model
    else:
        _logger.warning("Model Error: %s", model_err)
        string = string + '   Model not Found!\n'

    string = string + "   Bot-Name:  " + me['first_name'] + "\n"
    string = string + "   Username:  " + me['username'] + "\n"
    string = string + "   ID:        " + str(me['id']) + "\n"
    string = string + "   Branch:    " + str(get_git_branch()) + "\n"
    string = string + "   Version:   " + str(version) + "\n"
    string = string + "##############################################################\n"
    return string


def send_admins(msg, except_this='', silent=False):
    _logger.info("Send to all Admins (silent? %r): %s", silent, msg)
    for admin in _admins:
        if admin != except_this and len(admin) > 0:
            _bot.sendMessage(admin, msg, disable_notification=silent)



