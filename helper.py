import subprocess
import sys
import os
from threading import Thread
from pygit2 import Repository
from time import sleep

filePath = os.path.dirname(os.path.realpath(__file__))
bot = None
admins = []


def _execute(cmd):
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             shell=True)
    out = process.stdout.decode('utf-8')
    err = process.stderr.decode('utf-8')
    return out, err


def getFilePath():
    return filePath


def getGitBranch():
    try:
        repo = Repository(filePath + "/.git")
        return repo.head.shorthand
    except Exception as e:
        return None


def pull(chat_id, args=None):
    # Define Branch! When None, Default pull!
    if filePath == '':
        print("Cannot pull without Filepath!")
        return
    if bot is None:
        raise ReferenceError("Cannot use Function without Bot Context!")

    if len(args) > 1:
        # TODO Checkout new Branch!
        print("New Branch: "+args[1])
        out, err = _execute("cd " + filePath + " && git pull")
    else:
        out, err = _execute("cd " + filePath + " && git pull")

    if len(err)>0:
        result = "ERROR:\n"+err
    else:
        result = out
    bot.sendMessage(chat_id, result+"\nTask finished!")


def restart(chat_id, args=None):
    if bot is None:
        raise ReferenceError("Cannot use Function without Bot Context!")

    def restart_soon():
        sleep(1)
        os.execv(sys.executable, ['python'] + sys.argv)

    bot.sendMessage(chat_id, "Restarting... ")

    for admin in admins:
        if admin != chat_id:
            print("Debug: Admin ID: " + admin + ", chat_id: " + chat_id)
            bot.sendMessage(admin, "Just fyi: Someone ordered me to restart!")

    t = Thread(target=restart_soon)
    t.start()
