from modules.core_module import CoreModule
from urllib import request
import json


class Module(CoreModule):

    def __init__(self, bot):
        super().__init__(bot)
        try:
            request.urlopen("http://localhost/admin/api.php")
            self._enabled = True
        except Exception:
            self._enabled = False

    def is_enabled(self):
        return self._enabled

    def get_chat_functions(self):
        return {'/pihole': self.get_status}

    def get_status(self, chat_id, args=None):
        req = request.urlopen("http://localhost/admin/api.php?summary")
        txt = req.read().decode()
        dic = json.loads(txt)
        msg = 'Pi-Hole Stats of the Day:\n\n'
        for key in dic.keys():
            msg = msg + str(key).ljust(25) + ': '+str(dic[key])+'\n'
        self._bot.sendMessage(chat_id, msg)
