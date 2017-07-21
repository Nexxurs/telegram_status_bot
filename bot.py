import configparser
import telepot
from telepot.loop import MessageLoop
import time

from subprocess import call
import sys
import os

from threading import Thread
from time import sleep

filePath = ''

def pull(args = None):
	if filePath == '':
		print("Cannot pull without Filepath!")
	else:
		bot.sendMessage(chat_id, "Pulling..")
		call("cd ~/git/telegram_status_bot && git pull", shell=True)
		bot.sendMessage(chat_id, "Finished!")
	
def restart(args = None):
    def restartSoon():
        sleep(1)
        os.execv(sys.executable, ['python'] + sys.argv)
    bot.sendMessage(chat_id, "Restarting... ")
    t = Thread(target = restartSoon)
    t.start()
	
	
	
functions = {'/pull' : pull, 
    '/restart' : restart}

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id, msg['text'])
	
    msgArgs = msg['text'].split(' ')
	
    if msgArgs[0] in functions:
        functions[msg['text']](msgArgs)	
    else:
        bot.sendMessage(chat_id, "wat?")






if __name__ == '__main__':

    filePath = os.path.dirname(os.path.realpath(__file__))

    config = configparser.ConfigParser()
    config.read(filePath+"/config.ini")

    token = config['Telegram']['Token']
    token = str(token)

    bot = telepot.Bot(token)

    MessageLoop(bot, handle).run_as_thread()
    print ('Listening ...')

    # Keep the program running.
    while 1:
        time.sleep(10)