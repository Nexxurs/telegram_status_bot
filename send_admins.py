#!/usr/bin/env python3

from helpers import helper, bot as bot_helper
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
    msg = msg.replace('\\n', '\n')
    logger.info("Sending Message: "+msg)
    bot_helper.send_admins(msg, silent=args.silent)

