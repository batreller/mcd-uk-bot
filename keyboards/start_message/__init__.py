from aiogram import types

from languages import Languages


def start_message_keyboard(language: Languages):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(types.KeyboardButton('McDonald\'s 🍔'),
                 # types.KeyboardButton('Burger King 👑'),
                 types.KeyboardButton('Subway 🌮')
                 )
    keyboard.add(types.KeyboardButton(language.format_value('settings-button')))
    return keyboard
