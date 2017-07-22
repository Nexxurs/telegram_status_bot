from subprocess import call
import sys
import os
from threading import Thread
from pygit2 import Repository

filePath = os.path.dirname(os.path.realpath(__file__))
bot = None

def setBot(tel_bot):
    bot = tel_bot
    
def getFilePath():
    return filePath
    
def getGitBranch():
    repo = Repository(filePath+"/.git")
    return repo.head.shorthand
    
def pull(chat_id, args = None):
    #Define Branch! When None, Default pull!
    if filePath == '':
        print("Cannot pull without Filepath!")
    else:
        bot.sendMessage(chat_id, "Pulling..")
        call("cd "+filePath+" && git pull", shell=True)
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
    
