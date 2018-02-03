from helpers import executor, helper
from helpers import keyboard as keyboard_helper
import logging
from modules.core_module import CoreModule
from os import path
from config import config

_logger = logging.getLogger(__name__)


class Module(CoreModule):
    def __init__(self, bot):
        super().__init__(bot)
        self._filepath = helper.getBotRoot()

    def is_enabled(self):
        if not config.getboolean('Core_Modules_Enable', __name__, fallback=False):
            return False

        if not path.isdir(self._filepath+'/.git'):
            return False

        process = executor.execute('git --version')
        return process.returncode == 0

    def get_chat_functions(self):
        return {'/git_pull': self.pull,
                '/git_fetch': self.fetch}

    def pull(self, chat_id, args=None):
        # Define Branch! When None, Default pull!
        if self._filepath == '':
            print("Cannot pull without Filepath!")
            self._bot.sendMessage(chat_id, "No Filepath for Git found! Check the Logs!")
            return
        if self._bot is None:
            raise ReferenceError("Cannot use Function without Bot Context!")

        if len(args) > 1:
            branch = args[1]
            _logger.info("Checkout new Branch %s from Git", branch)
            process = executor.execute("cd " + self._filepath + " && git checkout " + branch + " && git pull")
        else:
            _logger.info("Pulling updates from Git")
            process = executor.execute("cd " + self._filepath + " && git pull")

        if len(process.stderr) > 0:
            result = process.stderr + "\n\n" + process.stdout
        else:
            result = process.stdout

        markup_keyboard = keyboard_helper.createSingleChoice("Restart Now", "restart")
        self._bot.sendMessage(chat_id, result + "\nTask finished! Do you want to restart now?",
                              reply_markup=markup_keyboard)

    def fetch(self, chat_id, args=None):
        process = executor.execute("cd " + self._filepath + " && git fetch")
        if len(process.stderr) > 0:
            result = process.stderr + "\n\n" + process.stdout
        else:
            result = process.stdout
        self._bot.sendMessage(chat_id, result + "\nTask finished!")

    def get_current_branch(self):
        _logger.info("Getting Current Git Branch")
        process = executor.execute("cd " + self._filepath + " && git symbolic-ref HEAD")
        if process.returncode != 0:
            return "No Git!"
        l = process.stdout.split('/')
        return '/'.join(l[2:]).strip()
