from aiogram import types

from database.models import User
from keyboards import start_message_keyboard
from languages import Languages


async def start_handler(message: types.Message, user: User, language: Languages):
    await message.answer(language.format_value('start-message'), reply_markup=start_message_keyboard(language))
