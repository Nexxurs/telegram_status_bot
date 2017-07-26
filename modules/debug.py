from telepot.namedtuple import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import logging

_bot = None
_config = None
_logger = logging.getLogger(__name__)

def init(bot, config):
    global _bot
    global _config
    _bot = bot
    _config = config


def is_enabled():
    return True


def get_chat_functions():
    return {}


def get_debug_chat_functions():
    return {'/debug_remove_keyboard': remove_keyboard,
                       '/debug_set_keyboard': set_keyboard}


def remove_keyboard(chat_id, args=None):
    logger.info("Removing custom Keyboard at Chat %r", chat_id)
    bot.sendMessage(chat_id, "Removed Custom Keyboard!", reply_markup=ReplyKeyboardRemove())


def set_keyboard(chat_id, args=None):
    logger.info("Adding custom testing Keyboard at Chat %r",chat_id)
    bot.sendMessage(chat_id, "Added Keyboard with Function to remove",
                    reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="/debug_remove_keyboard")]]))
