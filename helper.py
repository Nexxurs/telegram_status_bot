import subprocess
import sys
import os
from threading import Thread
from time import sleep
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import telepot
import logging

filePath = os.path.dirname(os.path.realpath(__file__))
bot = None
admins = []

logger = logging.getLogger(__name__)

restart_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Restart now", callback_data="restart"),
     InlineKeyboardButton(text="Restart later", callback_data="None")]])


def _execute(cmd):
    logger.debug("Executing System Call %s",cmd)
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             shell=True)
    out = process.stdout.decode('utf-8')
    err = process.stderr.decode('utf-8')
    return out, err


def getFilePath():
    return filePath


def getGitBranch():
    logger.info("Getting Current Git Branch")
    out, err = _execute("cd " + filePath + " && git symbolic-ref HEAD")
    l = out.split('/')
    return '/'.join(l[2:]).strip()


def send_admins(msg, except_this='', silent=False):
    logger.info("Send to all Admins (silent? %r): %s", silent, msg)
    for admin in admins:
        if admin != except_this and len(admin) > 0:
            bot.sendMessage(admin, msg, disable_notification=silent)


def pull(chat_id, args=None):
    # Define Branch! When None, Default pull!
    if filePath == '':
        print("Cannot pull without Filepath!")
        return
    if bot is None:
        raise ReferenceError("Cannot use Function without Bot Context!")

    if len(args) > 1:
        branch = args[1]
        logger.info("Checkout new Branch %s from Git", branch)
        out, err = _execute("cd " + filePath + " && git checkout " + branch + " && git pull")
    else:
        logger.info("Pulling updates from Git")
        out, err = _execute("cd " + filePath + " && git pull")

    if len(err) > 0:
        result = err + "\n\n" + out
    else:
        result = out
    bot.sendMessage(chat_id, result + "\nTask finished! Do you want to restart now?", reply_markup=restart_keyboard)


def restart_soon():
    logger.info("Restarting...")
    sleep(1)
    os.execv(sys.executable, [sys.executable] + sys.argv)


def restart(chat_id, args=None):
    if bot is None:
        raise ReferenceError("Cannot use Function without Bot Context!")

    bot.sendMessage(chat_id, "Restarting... ")

    send_admins("Just fyi: Someone ordered me to restart!", except_this=chat_id)

    t = Thread(target=restart_soon)
    t.start()


def callback_restart(msg):
    if bot is None:
        raise ReferenceError("Cannot use Function without Bot Context!")

    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    from_id = str(from_id)

    bot.answerCallbackQuery(query_id, text="Restarting... ")
    send_admins("Just fyi: Someone ordered me to restart!", except_this=from_id)

    t = Thread(target=restart_soon)
    t.start()

def callback_None(msg):
    pass