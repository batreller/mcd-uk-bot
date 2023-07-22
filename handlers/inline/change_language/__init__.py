from aiogram import types

from keyboards import choose_language_keyboard
from languages import Languages


async def settings_change_language_handler(query: types.CallbackQuery,
                                           # op: str,
                                           # data: list,
                                           # user: User,
                                           language: Languages):
    await query.message.edit_text(language.format_value('choose-language'),
                                  reply_markup=choose_language_keyboard(send_hello_message=True))
