from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from languages import Languages


def settings_menu_keyboard(language: Languages) -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(language.format_value('change-language'), callback_data='SETTINGS|CHANGE_LANG'))
    return keyboard
