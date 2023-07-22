from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from languages import Languages


def mcdonalds_delete_code(language: Languages) -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(language.format_value('close-code'), callback_data='MCD|DELCODE'))
    return keyboard
