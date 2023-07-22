from aiogram import types


def choose_language_keyboard(send_hello_message: bool = False):
    send_hello_message = 1 if send_hello_message else 0
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Русский 🇷🇺', callback_data=f'LANG|rus|{send_hello_message}'),
                 types.InlineKeyboardButton('English 🇬🇧', callback_data=f'LANG|eng|{send_hello_message}'),
                 types.InlineKeyboardButton('Українська 🇺🇦', callback_data=f'LANG|ukr|{send_hello_message}')
                 )
    return keyboard
