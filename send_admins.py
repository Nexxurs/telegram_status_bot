import helper
import sys
import logging
import argparse


if __name__ == '__main__':
    helper.config_logger()
    parser = argparse.ArgumentParser(description="Send a Telegram Message to all Admins in the config File!")
    parser.add_argument("--silent", "-s", help="set to send message silently",
                        action='store_true')
    parser.add_argument("text", help="The text to send", nargs='*')

    logger = logging.getLogger('Send_Admins')

    args = parser.parse_args()

    msg = ' '.join(args.text)
    logger.info("Sending Message: "+msg)
    helper.send_admins(msg, silent=args.silent)

