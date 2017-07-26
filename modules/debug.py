from telepot.namedtuple import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import logging
from modules.core_module import CoreModule

_logger = logging.getLogger(__name__)


class Module(CoreModule):
    def is_enabled(self):
        return True

    def get_debug_chat_functions(self):
        return {'/debug_remove_keyboard': self.remove_keyboard,
                '/debug_set_keyboard': self.set_keyboard}

    def remove_keyboard(self, chat_id, args=None):
        _logger.info("Removing custom Keyboard at Chat %r", chat_id)
        self._bot.sendMessage(chat_id, "Removed Custom Keyboard!", reply_markup=ReplyKeyboardRemove())

    def set_keyboard(self, chat_id, args=None):
        _logger.info("Adding custom testing Keyboard at Chat %r", chat_id)
        self._bot.sendMessage(chat_id, "Added Keyboard with Function to remove",
                              reply_markup=ReplyKeyboardMarkup(
                                  keyboard=[[KeyboardButton(text="/debug_remove_keyboard")]]))
