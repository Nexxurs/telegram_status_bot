import config
import logging
import sys
import os
from time import sleep
import telepot
from telepot.loop import MessageLoop
import helper
import modules

_VERSION = '0.1.2'
_DEBUG = True

filePath = None
admins = None
bot = None


# Logger INIT
if _DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO

root = logging.getLogger('')
root.setLevel(logging.DEBUG)
for h in root.handlers:
    root.removeHandler(h)

log_dir = "log"
if not os.path.exists(log_dir):
        os.makedirs(log_dir)
file_handler = logging.FileHandler(log_dir+'/telegram.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
file_handler.setLevel(logging.INFO)
root.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter('%(levelname)s - %(name)s - %(message)s'))
stream_handler.setLevel(logging.DEBUG)
root.addHandler(stream_handler)

logger = logging.getLogger(__name__)


def createHeader():
    if bot is None:
        raise ReferenceError("Cannot create Header without Bot Context!")

    me = bot.getMe()
    string = "\n"
    string = string + "##############################################################\n"
    string = string + "   Name:     " + me['first_name'] + "\n"
    string = string + "   Username: " + me['username'] + "\n"
    string = string + "   ID:       " + str(me['id']) + "\n"
    string = string + "   Branch:   " + str(helper.get_git_branch()) + "\n"
    string = string + "   Version:  " + str(_VERSION) + "\n"
    string = string + "##############################################################\n"
    return string


def aboutme(chat_id, args=None):
    logger.info("Creating About Me")
    if bot is None:
        raise ReferenceError("Cannot create AboutMe without Bot Context!")
    bot.sendMessage(chat_id, createHeader())


def show_debug(chat_id, args=None):
    if _DEBUG:
        logger.info("Creating List of Debug Functions")
        methods = ''
        for key in debug_functions.keys():
            methods = methods + str(key) + '\n'
        bot.sendMessage(chat_id, "All current Debug Methods:\n\n" + methods)
    else:
        logger.info("Debug is disabled - No List will be created!")
        bot.sendMessage(chat_id, "Debug is not enabled!")


def get_functions(chat_id, args=None):
    res = 'Here are all available functions:\n\n'
    for f in functions.keys():
        res = res+f+'\n'
    if _DEBUG:
        res = res+"-----------\n"
        for f in debug_functions.keys():
            res = res+f+'\n'
    bot.sendMessage(chat_id, res)


def handle_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    logger.info("New Message! Content-Type: %s, Chat-Type: %s, Sender-ID: %i, Chat-ID: %i, Content: %s", content_type, chat_type, msg['from']['id'],
                 chat_id, msg['text'])

    # admins are strings and it seems to work sending messages to String IDs
    chat_id = str(chat_id)
    user_id = str(msg['from']['id'])

    if user_id not in admins:
        logger.warning("Message from unknown User!")
        bot.sendMessage(chat_id, "I'm sorry, but my Daddy says im not allowed to speak to Strangers!")
        return

    msg_args = msg['text'].split(' ')

    if msg_args[0] in functions:
        functions[msg_args[0]](chat_id, msg_args)
    elif _DEBUG and msg_args[0] in debug_functions:
        debug_functions[msg_args[0]](chat_id, msg_args)
    else:
        bot.sendMessage(chat_id, "Error 404: Function not found!")


def handle_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    from_id = str(from_id)

    logger.info("New Callback Query! Query-ID: %s, Sender-ID: %s, Data: %s", query_id, from_id, query_id)

    if from_id not in admins:
        logger.warning("Callback Query from unknown User!")
        bot.answerCallbackQuery(query_id, text="No Permission!")
        return

    if query_data in callback_functions:
        callback_functions[query_data](msg)
    else:
        bot.answerCallbackQuery(query_id, text="Error - Function not found!", show_alert=True)


functions = {'/aboutme': aboutme,
             '/debug': show_debug}
debug_functions = {'/functions': get_functions}
callback_functions = {}


if __name__ == '__main__':
    bot = telepot.Bot(config.get_telegram_config()['Token'])

    logger.debug("INIT Helper")
    manager = modules.ModuleManager(bot=bot)
    helper.init(bot=bot, module_manager=manager)
    admins = helper.get_admins()

    functions = {**manager.get_enabled_chat_functions(), **functions}
    debug_functions = {**manager.get_enabled_debug_chat_functions(), **debug_functions}
    callback_functions = {**manager.get_enabled_callback_functions(), **callback_functions}

    try:
        logger.info(createHeader())
    except Exception as e:
        logger.exception("Cannot start Bot, Connection Error!")
        exit()

    logger.debug("INIT MessageLoop")
    MessageLoop(bot, {'chat': handle_chat_message,
                      'callback_query': handle_callback_query}).run_as_thread()
    logger.info('Listening ...')

    # Say Hello to our Admins!
    helper.send_admins("I'm Back!", silent=True)

    # Keep the program running.
    while 1:
        sleep(10)
