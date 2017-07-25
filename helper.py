import subprocess
import sys
import os
from threading import Thread
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
    out, err = _execute("cd " + filePath + " && git symbolic-ref HEAD")
    l = out.split('/')
    return '/'.join(l[2:])



def sendAdmins(msg, except_this=''):
    for admin in admins:
        if admin != except_this and len(admin) > 0:
            bot.sendMessage(admin, msg)


def pull(chat_id, args=None):
    # Define Branch! When None, Default pull!
    if filePath == '':
        print("Cannot pull without Filepath!")
        return
    if bot is None:
        raise ReferenceError("Cannot use Function without Bot Context!")

    if len(args) > 1:
        # TODO Checkout new Branch!
        branch = args[1]
        out, err = _execute("cd " + filePath + " && git checkout "+branch+" && git pull")
    else:
        out, err = _execute("cd " + filePath + " && git pull")

    if len(err) > 0:
        result = out+"\n\nERROR:\n" + err
    else:
        result = out
    bot.sendMessage(chat_id, result + "\nTask finished! Please /restart for the Changes to work!")


def restart_soon():
    sleep(1)
    os.execv(sys.executable, [sys.executable] + sys.argv)


def restart(chat_id, args=None):
    if bot is None:
        raise ReferenceError("Cannot use Function without Bot Context!")

    bot.sendMessage(chat_id, "Restarting... ")

    sendAdmins("Just fyi: Someone ordered me to restart!", chat_id)

    t = Thread(target=restart_soon)
    t.start()

