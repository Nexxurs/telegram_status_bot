import helper
import debug
import configparser
import telepot
from telepot.loop import MessageLoop
from time import sleep
from sys import exit

_VERSION = '0.1.1'
_DEBUG = False

filePath = None
admins = None
bot = None


def createHeader():
    if bot is None:
        raise ReferenceError("Cannot create Header without Bot Context!")

    me = bot.getMe()
    string = "\n"
    string = string + "####################################################\n"
    string = string + "   Name: " + me['first_name'] + "\n"
    string = string + "   Username: " + me['username'] + "\n"
    string = string + "   ID: " + str(me['id']) + "\n"
    string = string + "   Branch: " + str(helper.getGitBranch()) + "\n"
    string = string + "   Version: " + str(_VERSION) + "\n"
    string = string + "####################################################\n"
    return string


def aboutme(chat_id, args=None):
    if bot is None:
        raise ReferenceError("Cannot create AboutMe without Bot Context!")
    bot.sendMessage(chat_id, createHeader())


def show_debug(chat_id, args=None):
    if _DEBUG:
        methods = ''
        for key in debug_functions.keys():
            methods = methods + str(key) + '\n'
        bot.sendMessage(chat_id, "All current Debug Methods:\n\n" + methods)
    else:
        bot.sendMessage(chat_id, "Debug is not enabled!")


functions = {'/pull': helper.pull,
             '/restart': helper.restart,
             '/aboutme': aboutme,
             '/debug': show_debug}

debug_functions = {'/debug_remove_keyboard': debug.remove_keyboard,
                   '/debug_set_keyboard': debug.set_keyboard}

callback_functions = {'restart': helper.callback_restart}
if _DEBUG:
    functions = {**functions, **debug_functions}


def handle_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print("Content:", content_type, ", Chat Type:", chat_type, ", From:", msg['from']['id'],
          ", Chat ID:", chat_id, ", Text:", msg['text'])

    # admins are strings and it seems to work sending messages to String IDs
    chat_id = str(chat_id)
    user_id = str(msg['from']['id'])

    if user_id not in admins:
        print("Message from unknown User!")
        bot.sendMessage(chat_id, "I'm sorry, but my Daddy says im not allowed to speak to Strangers!")
        return

    msg_args = msg['text'].split(' ')

    if msg_args[0] in functions:
        functions[msg_args[0]](chat_id, msg_args)
    else:
        bot.sendMessage(chat_id, "Error 404: Function not found!")


def handle_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    from_id = str(from_id)

    if from_id not in admins:
        print("Callback Query from unknown User!")
        bot.answerCallbackQuery(query_id, text="No Permission!")
        return

    if query_data in callback_functions:
        callback_functions[query_data](msg)
    else:
        bot.answerCallbackQuery(query_data, text="Error - Function not found!", show_alert=True)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(helper.getFilePath() + "/config.ini")

    token = config['Telegram']['Token']
    token = str(token)

    admins = config['Telegram']['Admins']
    admins = admins.split(',')

    bot = telepot.Bot(token)

    helper.bot = bot
    helper.admins = admins

    debug.bot = bot

    try:
        print(createHeader())
    except Exception as e:
        print("Cannot start Bot, Connection Error!")
        print(e)
        exit()

    MessageLoop(bot, {'chat': handle_chat_message,
                      'callback_query': handle_callback_query}).run_as_thread()
    print('Listening ...')

    # Say Hello to our Admins!
    helper.send_admins("I'm Back!", silent=True)

    # Keep the program running.
    while 1:
        sleep(10)
