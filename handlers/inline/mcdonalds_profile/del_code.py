from aiogram import types

from database.models import User
from languages import Languages


async def del_code_handler(query: types.CallbackQuery,
                           # op: str,
                           data: list,
                           user: User,
                           language: Languages):
    await query.answer(language.format_value('code-deleted'))
    await query.message.delete()
