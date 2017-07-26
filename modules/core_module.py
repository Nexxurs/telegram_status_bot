

class CoreModule:
    def __init__(self, bot, config):
        self._bot = bot
        self._config = config

    def is_enabled(self):
        return False

    def get_chat_functions(self):
        return {}

    def get_debug_chat_functions(self):
        return {}

    def get_callback_functions(self):
        return {}


# For Copy-Paste!
class Module(CoreModule):
    def is_enabled(self):
        return False

    def get_chat_functions(self):
        return {}