import helper
import logging

_logger = logging.getLogger(__name__)
_bot = None
_config = None
_filepath = helper.getFilePath()


def init(bot, config):
    global _bot
    global _config
    _bot = bot
    _config = config


def is_enabled():
    # todo check if git is possible!
    return True


def get_chat_functions():
    return {'/git_pull': pull}


def pull(chat_id, args=None):
    # Define Branch! When None, Default pull!
    if _filepath == '':
        print("Cannot pull without Filepath!")
        return
    if _bot is None:
        raise ReferenceError("Cannot use Function without Bot Context!")

    if len(args) > 1:
        branch = args[1]
        _logger.info("Checkout new Branch %s from Git", branch)
        out, err = helper.execute("cd " + _filepath + " && git checkout " + branch + " && git pull")
    else:
        _logger.info("Pulling updates from Git")
        out, err = helper.execute("cd " + _filepath + " && git pull")

    if len(err) > 0:
        result = err + "\n\n" + out
    else:
        result = out
    _bot.sendMessage(chat_id, result + "\nTask finished! Do you want to restart now?",
                     reply_markup=helper.restart_keyboard)
