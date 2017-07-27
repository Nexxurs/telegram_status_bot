import helper
import logging
from modules.core_module import CoreModule
from os import path

_logger = logging.getLogger(__name__)


class Module(CoreModule):
    def __init__(self, bot):
        super().__init__(bot)
        self._filepath = helper.get_file_path()

    def is_enabled(self):
        return path.isdir(self._filepath+'/.git')

    def get_chat_functions(self):
        return {'/git_pull': self.pull}

    def pull(self, chat_id, args=None):
        # Define Branch! When None, Default pull!
        if self._filepath == '':
            print("Cannot pull without Filepath!")
            return
        if self._bot is None:
            raise ReferenceError("Cannot use Function without Bot Context!")

        if len(args) > 1:
            branch = args[1]
            _logger.info("Checkout new Branch %s from Git", branch)
            out, err = helper.execute("cd " + self._filepath + " && git checkout " + branch + " && git pull")
        else:
            _logger.info("Pulling updates from Git")
            out, err = helper.execute("cd " + self._filepath + " && git pull")

        if len(err) > 0:
            result = err + "\n\n" + out
        else:
            result = out
        self._bot.sendMessage(chat_id, result + "\nTask finished! Do you want to restart now?",
                              reply_markup=helper.restart_keyboard)

    def fetch(self, chat_id, args=None):
        out, err = helper.execute("cd " + self._filepath + " && git fetch")
        if len(err) > 0:
            result = err + "\n\n" + out
        else:
            result = out
        self._bot.sendMessage(chat_id, result + "\nTask finished!")

    def get_current_branch(self):
        _logger.info("Getting Current Git Branch")
        out, err = helper.execute("cd " + self._filepath + " && git symbolic-ref HEAD")
        if len(err) > 0:
            return "No Git!"
        l = out.split('/')
        return '/'.join(l[2:]).strip()
