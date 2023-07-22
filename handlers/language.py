from aiogram import types

from keyboards import choose_language_keyboard
from languages import Languages


async def choose_language_handler(message: types.Message, language: Languages, send_hello_message: bool = False):
    await message.answer(language.format_value('choose-language'), reply_markup=choose_language_keyboard(send_hello_message=send_hello_message))
