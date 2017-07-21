import configparser
import telepot
from telepot.loop import MessageLoop
import time

from subprocess import call
import sys
import os


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id, msg['text'])

    if(msg['text'] == "/pull"):
        bot.sendMessage(chat_id, "Pulling..")
        call("cd ~/git/telegram_status_bot && git pull", shell=True)
        bot.sendMessage(chat_id, "Finished!")
    elif(msg['text'] == "/restart"):
        bot.sendMessage(chat_id, "Restarting... ")
        os.execv(sys.executable, ['python']+sys.argv)
    else:
        bot.sendMessage(chat_id, "wat?")
config = configparser.ConfigParser()
config.read("/home/pi/git/telegram_status_bot/config.ini")

token = config['Telegram']['Token']
token = str(token)

bot = telepot.Bot(token)

MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)