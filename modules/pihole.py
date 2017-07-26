from modules.core_module import CoreModule
from urllib import request, error
import json

class Module(CoreModule):

    def __init__(self, bot, config):
        super().__init__(bot, config)
        try:
            req = request.urlopen("http://localhost/admin/api.php")
            self._enabled = True
        except Exception:
            self._enabled = False

    def is_enabled(self):
        return self._enabled

    def get_chat_functions(self):
        return {'/pihole': self.get_status}

    def get_status(self, chat_id, args=None):
        req = request.urlopen("http://localhost/admin/api.php")
        txt = req.read().decode()
        dic = json.loads(txt)
        msg = 'Pi-Hole Stats of the Day:\n'
        for key in dic.keys():
            msg = msg + key + ': '+dic[key]+'\n'
        self._bot.sendMessage(chat_id, msg)
