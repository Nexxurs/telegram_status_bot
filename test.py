import modules as mod


class TestBot:
    def sendMessage(self,chat_id, string):
        print("To {}: {}".format(chat_id, string))

tb = TestBot()
manager = mod.ModuleManager(tb)

# Test Modules with manager.get_module_by_name("Module-Name")
