from collections import namedtuple
import logging
import subprocess

_logger = logging.getLogger(__name__)

Process = namedtuple('Process', ['returncode', 'stdout', 'stderr'])


def execute(cmd):
    _logger.debug("Executing System Call %s", cmd)
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             shell=True)
    out = process.stdout.decode('utf-8', errors='replace')
    err = process.stderr.decode('utf-8', errors='replace')
    returncode = process.returncode

    return Process(returncode, out, err)