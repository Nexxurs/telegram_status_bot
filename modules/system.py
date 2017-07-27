import logging
from modules.core_module import CoreModule
from time import sleep
import os
import sys
import helper
from threading import Thread
import telepot

_logger = logging.getLogger(__name__)


class Module(CoreModule):
    def is_enabled(self):
        return True

    def get_chat_functions(self):
        return {'/restart': self.restart}

    def get_callback_functions(self):
        return {'restart': self.callback_restart}

    def restart(self, chat_id, args=None):
        self._bot.sendMessage(chat_id, "Restarting... ")

        helper.send_admins("Just fyi: Someone ordered me to restart!", except_this=chat_id)

        t = Thread(target=restart_soon)
        t.start()

    def callback_restart(self, msg):
        if self._bot is None:
            raise ReferenceError("Cannot use Function without Bot Context!")

        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        from_id = str(from_id)

        self._bot.answerCallbackQuery(query_id, text="Restarting... ")
        helper.send_admins("Just fyi: Someone ordered me to restart!", except_this=from_id)

        t = Thread(target=restart_soon)
        t.start()


def restart_soon():
    _logger.info("Restarting...")
    sleep(1)
    os.execv(sys.executable, [sys.executable] + sys.argv)
