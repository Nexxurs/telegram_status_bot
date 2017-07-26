import importlib
import pkgutil
import logging

_logger = logging.getLogger(__name__)


class ModuleManager():
    def __init__(self, config, bot):
        self.bot = bot
        self.config = config

        self.module_list = []

        for importer, modname, ispkg in pkgutil.iter_modules([__package__]):
            logging.debug("Found submodule %s (is a package: %s)", (modname, ispkg))
            try:
                tmp_module = importlib.import_module(__package__ + '.' + modname)
                tmp_module.init(bot=self.bot, config=self.config)
                self.module_list.append(tmp_module)
            except AttributeError:
                # todo LOGGING
                pass

    def get_enabled(self):
        res = []
        bad_modules = []
        for m in self.module_list:
            try:
                if m.is_enabled():
                    res.append(m)
            except AttributeError:
                # todo logging
                bad_modules.append(m)

        for m in bad_modules:
            self.module_list.remove(m)
        return res

    def get_enabled_chat_functions(self):
        res = {}

        modules = self.get_enabled()

        for mod in modules:
            try:
                new_functions = mod.get_chat_functions()
                res = {**new_functions, **res}
            except AttributeError:
                # logging
                pass

        return res