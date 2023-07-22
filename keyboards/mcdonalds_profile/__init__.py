from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from languages import Languages


def mcdonalds_profile_keyboard(language: Languages) -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(language.format_value('use-mcdonalds-code'), callback_data='MCD|GETCODE'),
                 types.InlineKeyboardButton(language.format_value('mcdonalds-logs'), callback_data='MCD|ARCHIVE|0|11')
                 )
    return keyboard
