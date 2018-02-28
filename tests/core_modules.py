import unittest
from modules import core_module
from modules.Core import debug, external_ip, git, system


class DebugModuleTest(unittest.TestCase):
    def test_subclass(self):
        self.assertTrue(issubclass(debug.Module, core_module.CoreModule))


class ExternalIPTest(unittest.TestCase):
    def test_subclass(self):
        self.assertTrue(issubclass(external_ip.Module, core_module.CoreModule))


class GitTest(unittest.TestCase):
    def test_subclass(self):
        self.assertTrue(issubclass(git.Module, core_module.CoreModule))


class SystemTest(unittest.TestCase):
    def test_subclass(self):
        self.assertTrue(issubclass(system.Module, core_module.CoreModule))


if __name__ == '__main__':
    unittest.main()
