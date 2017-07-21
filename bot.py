import configparser
import telepot
from telepot.loop import MessageLoop
import time


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id, msg['text'])

    if(msg['text'] == "pull"):
        bot.sendMessage(chat_id, "Pulling.. "+str(chat_id))
    else:
        bot.sendMessage("wat?")
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