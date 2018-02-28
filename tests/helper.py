import unittest
from helpers import helper
from pathlib import Path
import logging

class HelperTest(unittest.TestCase):

    def test_bot_root(self):
        self.assertIsInstance(helper.getBotRoot(), str)
        self.assertIsInstance(helper.getBotRootPath(), Path)

    def test_config_logger(self):
        root = logging.getLogger()

        helper.config_logger(logging.INFO, to_File=True)
        countWithFile = len(root.handlers)
        self.assertGreater(countWithFile, 0)

        helper.config_logger(logging.INFO, to_File=False)
        countWithoutFile = len(root.handlers)
        self.assertGreater(countWithoutFile, 0)

        self.assertGreater(countWithFile, countWithoutFile)

    def test_can_connect(self):
        self.assertFalse(helper.can_connect("doesnt_exist"))
        self.assertTrue(helper.can_connect("www.google.com"))



if __name__ == '__main__':
    unittest.main()