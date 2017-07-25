from telepot.namedtuple import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import logging

bot = None

logger = logging.getLogger(__name__)


def remove_keyboard(chat_id, args=None):
    logger.info("Removing custom Keyboard at Chat %r", chat_id)
    bot.sendMessage(chat_id, "Removed Custom Keyboard!", reply_markup=ReplyKeyboardRemove())


def set_keyboard(chat_id, args=None):
    logger.info("Adding custom testing Keyboard at Chat %r",chat_id)
    bot.sendMessage(chat_id, "Added Keyboard with Function to remove",
                    reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="/debug_remove_keyboard")]]))
