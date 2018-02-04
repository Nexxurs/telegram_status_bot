import unittest
from helpers import executor


class ExecutorTest(unittest.TestCase):
    def test_execute_help(self):
        proc = executor.execute("hostname")
        self.assertGreater(len(proc.stdout), 0)
        self.assertEqual(0, len(proc.stderr))
        self.assertEqual(0, proc.returncode)

    def test_execute_unkown(self):
        proc = executor.execute("nocommandasdfasdf")
        self.assertNotEqual(0, proc.returncode)
        self.assertEqual(0, len(proc.stdout))
        self.assertGreater(len(proc.stderr), 0)


if __name__ == '__main__':
    unittest.main()
