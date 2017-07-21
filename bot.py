import configparser
import telepot


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if(msg['text'] == "pull"):
        bot.sendMessage(chat_id, "Pulling.. "+chat_id)

config = configparser.ConfigParser()
config.read("/home/pi/git/telegram_status_bot/config.ini")

token = config['Telegram']['Token']
token = str(token)

bot = telepot.Bot(token)


