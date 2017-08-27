import helper
import sys
import logging


if __name__ == '__main__':
    helper.config_logger()
    logger = logging.getLogger('Send_Admins')
    args = sys.argv[1:]
    msg = ' '.join(args)
    logger.info("Sending Message: "+msg)
    helper.send_admins(msg)

