import logging
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

_logger = logging.getLogger(__name__)

#Use them in system module too!

def createSingleChoice(text, callback_text):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=callback_text)]])

def createMultipleChoiceRows(textDict):
    buttons = []
    for key in textDict:
        bt = InlineKeyboardButton(text=key, callback_data=textDict[key])
        buttons.append([bt])
    return InlineKeyboardMarkup(inline_keyboard=bt)
