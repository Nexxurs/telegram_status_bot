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
admins = []

def pull(chat_id, args = None):
    #Define Branch! When None, Default pull!
    if filePath == '':
        print("Cannot pull without Filepath!")
    else:
        bot.sendMessage(chat_id, "Pulling..")
        call("cd ~/git/telegram_status_bot && git pull", shell=True)
        bot.sendMessage(chat_id, "Finished!")
    
def restart(chat_id, args = None):
    def restartSoon():
        sleep(1)
        os.execv(sys.executable, ['python'] + sys.argv)
    
    bot.sendMessage(chat_id, "Restarting... ")
    
    for admin in admins:
        if admin != chat_id:
            print("Debug: Admin ID: "+admin+", chat_id: "+chat_id)
            bot.sendMessage(admin, "Just fyi: Someone ordered me to restart!")
    
    t = Thread(target = restartSoon)
    t.start()
    
    
    
functions = {'/pull' : pull, 
    '/restart' : restart}

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id, msg['text'])
    
    #admins are strings and it seems to work sending messages to String IDs
    chat_id = str(chat_id)
    
    if not str(chat_id) in admins:
        print("Message from unknown User!")
        bot.sendMessage("I'm sorry, but my Daddy says im not allowed to speak to strangers!")
        return
        
    msgArgs = msg['text'].split(' ')
    
    if msgArgs[0] in functions:
        functions[msg['text']](chat_id, msgArgs) 
    else:
        bot.sendMessage(chat_id, "wat?")



if __name__ == '__main__':

    filePath = os.path.dirname(os.path.realpath(__file__))

    config = configparser.ConfigParser()
    config.read(filePath+"/config.ini")

    token = config['Telegram']['Token']
    token = str(token)
    
    admins = config['Telegram']['Admins']
    admins = admins.split(',')

    bot = telepot.Bot(token)
    
    me = bot.getMe()
    print("Telegram Bot starting...")
    print("Name: "+me['first_name'])
    print("Username: "+me['username'])
    print("ID: "+me['id'])
    
    #TODO print Branch

    MessageLoop(bot, handle).run_as_thread()
    print ('Listening ...')
    
    #Say Hello to our Admins!
    for admin in admins:
        bot.sendMessage(admin, "Hello, im Back!")

    # Keep the program running.
    while 1:
        time.sleep(10)