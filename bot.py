import configparser
import telepot
from telepot.loop import MessageLoop
import time

from subprocess import call
import sys
import os

from threading import Thread
from time import sleep

def restartSoon():
    sleep(1)
    os.execv(sys.executable, ['python'] + sys.argv)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id, msg['text'])

    if(msg['text'] == "/pull"):
        bot.sendMessage(chat_id, "Pulling..")
        call("cd ~/git/telegram_status_bot && git pull", shell=True)
        bot.sendMessage(chat_id, "Finished!")
    elif(msg['text'] == "/restart"):
        bot.sendMessage(chat_id, "Restarting... ")
        t = Thread(restartSoon)
        t.start()
    else:
        bot.sendMessage(chat_id, "wat?")

        

config = configparser.ConfigParser()
config.read("/home/pi/git/telegram_status_bot/config.ini")

token = config['Telegram']['Token']
token = str(token)

bot = telepot.Bot(token)

MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')
print(sys.executable)

# Keep the program running.
while 1:
    time.sleep(10)