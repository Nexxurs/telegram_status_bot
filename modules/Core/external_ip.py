from modules.core_module import CoreModule
import ipgetter
import logging

_logger = logging.getLogger(__name__)


class Module(CoreModule):
    def is_enabled(self):
        return True

    def get_chat_functions(self):
        return {"/ext_ip" : self.ext_ip}

    def ext_ip(self, chat_id, args=None):
        _logger.debug("Getting external IP...")
        ip = ipgetter.myip()
        self._bot.sendMessage(chat_id, "My external IP is {}".format(ip))
