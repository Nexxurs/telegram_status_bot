import logging
from modules.core_module import CoreModule
from time import sleep
import os
import sys
import helper
from threading import Thread
import telepot
import platform
from config import config

_logger = logging.getLogger(__name__)


class Module(CoreModule):
    def is_enabled(self):
        if not config.getboolean('Core_Modules_Enable', __name__, fallback=False):
            return False

        return True

    def get_chat_functions(self):
        _logger.info("Initializing System Module")
        osname = platform.system()

        result = {'/restart': self.restart}

        if osname == 'Linux':
            _logger.debug("Linux System found")
            linux_functions = {'/status': self.status,
                               '/system_restart': self.system_restart,
                               '/system_shutdown': self.system_shutdown}
            result = {**linux_functions, **result}
        else:
            _logger.debug("Another OS found: "+osname)

        return result

    def get_callback_functions(self):
        return {'restart': self.callback_restart}

    def system_shutdown(self, chat_id, args=None):
        def shutdown_soon():
            _logger.info("Shutdown System...")
            sleep(1)
            helper.execute("shutdown now")

        helper.send_admins("Shutting down System!")
        t = Thread(target=shutdown_soon)
        t.start()

    def system_restart(self, chat_id, args=None):
        def restart_soon():
            _logger.info("Restarting System...")
            sleep(1)
            helper.execute("shutdown -r now")

        helper.send_admins("Restarting System!")
        t = Thread(target=restart_soon)
        t.start()

    def status(self, chat_id, args=None):
        out, err = helper.execute('uptime')

        if len(err) > 0:
            self._bot.sendMessage(chat_id, "Error: " + err)
            return
        out = out.strip()
        out = out.replace(',', '')
        array = out.split(' ')

        uptime_endindex = -1
        for i in array:
            if str(i).startswith('user'):
                uptime_endindex = array.index(i) - 2
        if uptime_endindex < 0:
            self._bot.sendMessage(chat_id, 'A problem occured: uptime is faulty\n' + out)
            _logger.warning("Faulty uptime: " + out)
            return
        loads_startindex = uptime_endindex + 6

        uptime = array[2:uptime_endindex]
        loads = array[loads_startindex:]

        result = ''
        result = result + 'Uptime:   '
        for u in uptime:
            if len(u) > 0:
                result = result + u + ' '
        result = result + '\n'
        result = result + 'Loads:    '
        for l in loads:
            result = result + l + ' '
        result = result + '\n'

        tmp, _ = helper.execute('/opt/vc/bin/vcgencmd measure_temp')
        tmp = tmp.replace('temp=', '')
        result = result + 'Temperature: ' + tmp
        result = result + 'Disk Usage: ' + get_disk_usage() + '\n'
        result = result + 'Memory Usage: ' + get_memory_usage() + '\n'

        self._bot.sendMessage(chat_id, result)

    def restart(self, chat_id, args=None):
        self._bot.sendMessage(chat_id, "Restarting... ")

        helper.send_admins("Just fyi: Someone ordered me to restart!", except_this=chat_id)

        t = Thread(target=restart_program_soon)
        t.start()

    def callback_restart(self, msg):
        if self._bot is None:
            raise ReferenceError("Cannot use Function without Bot Context!")

        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        from_id = str(from_id)

        self._bot.answerCallbackQuery(query_id, text="Restarting... ")
        helper.send_admins("Just fyi: Someone ordered me to restart!", except_this=from_id)

        t = Thread(target=restart_program_soon)
        t.start()


def restart_program_soon():
    _logger.info("Restarting...")
    sleep(1)
    os.execv(sys.executable, [sys.executable] + sys.argv)


def get_disk_usage():
    out, err = helper.execute('df -h | awk \'$NF=="/"{printf "%d/%dGB (%s)", $3,$2,$5}\'')
    if err:
        return 'Err: '+err
    return out


def get_memory_usage():
    out, err = helper.execute('free -m | awk \'NR==2{printf "%s/%sMB (%.2f%%)", $3,$2,$3*100/$2 }\'')
    if err:
        return 'Err: ' + err
    return out
