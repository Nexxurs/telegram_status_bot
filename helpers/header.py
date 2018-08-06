import logging
import socket
from helpers import bot as bot_helper
from helpers import helper, executor as executor_helper

_logger = logging.getLogger(__name__)
_git_branch = None


def get_git_branch():
    global _git_branch
    if _git_branch is None:
        mod = helper.get_module_manager().get_module_by_name('git')
        if mod is None:
            _git_branch = "No Git!"
        else:
            _git_branch = mod.get_current_branch()
        _logger.debug('Created Git Branch: '+_git_branch)

    return _git_branch


def create_header(version='No Version'):
    me = bot_helper.get_bot().getMe()
    string = ""

    string = string + "##############################################################\n"

    model_proc = executor_helper.execute(str(helper.getBotRootPath() / 'scripts' / 'model.sh'))
    if model_proc.returncode == 0:
        string = string + "   " + model_proc.stdout
    else:
        _logger.warning("Model Error: %s", model_proc.stderr)
        string = string + '   Model not Found!\n'

    string = string + "   Hostname:  " + socket.gethostname() + "\n\n"

    string = string + "   Bot-Name:  " + me['first_name'] + "\n"
    string = string + "   Username:  " + me['username'] + "\n"
    string = string + "   ID:        " + str(me['id']) + "\n\n"

    string = string + "   Branch:    " + str(get_git_branch()) + "\n"
    string = string + "   Version:   " + str(version) + "\n"
    string = string + "##############################################################\n"
    return string