import logging
from modules.core_module import CoreModule
from time import sleep
import os
import sys
import helper
from threading import Thread
import telepot
import socket
import platform

_logger = logging.getLogger(__name__)


class Module(CoreModule):
    def is_enabled(self):
        return True

    def get_chat_functions(self):
        osname = platform.system()

        result = {'/restart': self.restart}

        if osname == 'Linux':
            linux_functions = {'/status': self.status}
            result = {**linux_functions, **result}

        return result

    def get_callback_functions(self):
        return {'restart': self.callback_restart}

    def status(self, chat_id, args=None):
        hostname = socket.gethostname()
        out, err = helper.execute('uptime')

        out = out.strip()
        out.replace(',', '')
        array = out.split(' ')

        uptime = array[2]
        loads = array[9:]

        result = ''
        out, err = helper.execute('cd '+helper.get_file_path()+' & scripts/model.sh')
        if len(out > 0):
            result = result+out
        result = result + 'Hostname:' + hostname + '\n'
        result = result + 'Uptime:  ' + uptime + '\n'
        result = result + 'Loads:   '
        for l in loads:
            result = result + l + ' '
        result = result + '\n'

        self._bot.sendMessage(chat_id, result)

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
