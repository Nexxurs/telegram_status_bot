from telepot.namedtuple import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

bot = None


def remove_keyboard(chat_id, args=None):
    bot.sendMessage(chat_id, "Removed Custom Keyboard!", reply_markup=ReplyKeyboardRemove())


def set_keyboard(chat_id, args=None):
    bot.sendMessage(chat_id, "Added Keyboard with Function to remove",
                    reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="/debug_remove_keyboard")]]))
