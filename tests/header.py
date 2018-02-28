import unittest
from helpers import header


class HeaderTest(unittest.TestCase):
    def test_git_branch(self):
        self.assertIsNotNone(header.get_git_branch())
        self.assertIsInstance(header.get_git_branch(), str)

    def test_header(self):
        self.assertIsNotNone(header.create_header())
        self.assertIsInstance(header.create_header(), str)


if __name__ == '__main__':
    unittest.main()
