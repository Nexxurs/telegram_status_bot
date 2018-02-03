import importlib
import pkgutil
import logging
from pathlib import Path

_logger = logging.getLogger(__name__)

_module_path = Path(__file__).parent # Creates a new PurePath Object, which will be casted back into a Path Object
_module_path = Path(_module_path)


def getModuleDirs():
    module_dirs = []
    possible_dirs = ['Core', 'User']

    for d in possible_dirs:
        path = _module_path / d
        if path.exists():
            module_dirs.append(path._str)

    return module_dirs

class ModuleManager:
    def __init__(self, bot):
        _logger.debug('Initializing ModuleManager with Path {}'.format(_module_path))
        self.bot = bot

        self.module_list = []

        for importer, modname, ispkg in pkgutil.iter_modules(getModuleDirs()):
            _logger.debug("Found submodule %s (is a package: %s)", modname, ispkg)
            try:
                spec = importer.find_spec(modname)
                imported_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(imported_module)

                tmp_module = imported_module.Module(bot=bot)
                self.module_list.append(tmp_module)
                _logger.info("Imported Module %s", modname)
            except Exception as e:
                _logger.exception("Can't import %r. Exception: %r", modname, e)

    def get_enabled(self):
        res = []
        bad_modules = []
        for m in self.module_list:
            try:
                if m.is_enabled():
                    res.append(m)
            except Exception:
                _logger.exception("Found bad module: %r", m)
                bad_modules.append(m)

        for m in bad_modules:
            self.module_list.remove(m)
        return res

    def get_enabled_chat_functions(self):
        bad_modules = []
        res = {}
        modules = self.get_enabled()
        for mod in modules:
            try:
                new_functions = mod.get_chat_functions()
                res = {**new_functions, **res}
            except AttributeError:
                _logger.info("No chat functions for %r", mod.__module__)
            except Exception:
                _logger.exception("Something else happened to %r", mod.__module__)
                bad_modules.append(mod)
        for m in bad_modules:
            self.module_list.remove(m)
        return res

    def get_enabled_debug_chat_functions(self):
        res = {}
        bad_modules = []
        modules = self.get_enabled()
        for mod in modules:
            try:
                new_functions = mod.get_debug_chat_functions()
                res = {**new_functions, **res}
            except AttributeError:
                _logger.info("No chat functions for %r", mod)
            except Exception:
                _logger.exception("Something else happened to %r", mod.__module__)
                bad_modules.append(mod)
        for m in bad_modules:
            self.module_list.remove(m)
        return res

    def get_enabled_callback_functions(self):
        res = {}
        bad_modules = []
        modules = self.get_enabled()
        for mod in modules:
            try:
                new_functions = mod.get_callback_functions()
                res = {**new_functions, **res}
            except AttributeError:
                _logger.info("No chat functions for %r", mod)
            except Exception:
                _logger.exception("Something else happened to %r", mod.__module__)
                bad_modules.append(mod)
        for m in bad_modules:
            self.module_list.remove(m)
        return res

    def get_module_by_name(self, name):
        full_name = __package__+'.'+name
        for mod in self.module_list:
            if mod.__module__ == full_name:
                return mod
        return None
