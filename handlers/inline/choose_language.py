from aiogram import types

from database.connector import session
from database.models import User
from handlers import start_handler
from languages import Languages


async def change_language_handler(query: types.CallbackQuery,
                                  # op: str,
                                  data: list,
                                  user: User,
                                  language: Languages):
    user.language = data[0]
    session.commit()
    language = language.swap_language(user.language)
    await query.answer(
        language.format_value('language-changed', {'new_language': language.format_value('language-name')}))
    await query.message.delete()

    if data[1] == '1':
        await start_handler(message=query.message, user=user, language=language)
