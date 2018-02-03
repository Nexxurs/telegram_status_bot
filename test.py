import modules as mod
import helper
import logging

helper.config_logger(logging.DEBUG, to_File=False)

class TestBot:
    def sendMessage(self,chat_id, string):
        print("To {}: {}".format(chat_id, string))

tb = TestBot()
manager = mod.ModuleManager(tb)

# Test Modules with manager.get_module_by_name("Module-Name")
