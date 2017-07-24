import configparser
import telepot
from telepot.loop import MessageLoop
from time import sleep
import helper
from sys import exit

_VERSION = 0.1

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


functions = {'/pull': helper.pull,
             '/restart': helper.restart,
             '/aboutme': aboutme}


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id, msg['text'])

    # admins are strings and it seems to work sending messages to String IDs
    chat_id = str(chat_id)

    if not chat_id in admins:
        print("Message from unknown User!")
        bot.sendMessage(chat_id, "I'm sorry, but my Daddy says im not allowed to speak to Strangers!")
        return

    msgArgs = msg['text'].split(' ')

    if msgArgs[0] in functions:
        functions[msgArgs[0]](chat_id, msgArgs)
    else:
        bot.sendMessage(chat_id, "Error 404: Function not found!")


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

    try:
        print(createHeader())
    except Exception as e:
        print("Cannot start Bot, Connection Error!")
        print(e)
        exit()

    MessageLoop(bot, handle).run_as_thread()
    print('Listening ...')

    # Say Hello to our Admins!
    helper.sendAdmins("I'm Back!")

    # Keep the program running.
    while 1:
        sleep(10)
