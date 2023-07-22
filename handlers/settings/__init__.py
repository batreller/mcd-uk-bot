from aiogram import types

from database.connector import session
from database.models import User
from database.models.code import Code
from keyboards import mcdonalds_profile_keyboard, settings_menu_keyboard
from languages import Languages


async def settings_handler(message: types.Message, user: User, language: Languages):
    await message.answer(language.format_value('settings-menu'), reply_markup=settings_menu_keyboard(language))
