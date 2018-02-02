

class CoreModule:
    def __init__(self, bot):
        self._bot = bot

    def is_enabled(self):
        return False

    def get_chat_functions(self):
        return {}

    def get_debug_chat_functions(self):
        return {}

    def get_callback_functions(self):
        return {}

    def on_message(self, chat_id, args=None):
        pass


# For Copy-Paste!
class Module(CoreModule):
    def is_enabled(self):
        return False

    def get_chat_functions(self):
        return {}

    def on_message(self, chat_id, args=None):
        pass
