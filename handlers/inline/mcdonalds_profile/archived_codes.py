from aiogram import types

from database.models import User
from languages import Languages


async def archived_codes_handler(query: types.CallbackQuery,
                           # op: str,
                           data: list,
                           user: User,
                           language: Languages):
    used_codes = [code for code in user.codes if code.used is True][int(data[1]):int(data[2])]
    if len(used_codes) == 0:
        await query.answer(language.format_value('mcdonalds-no-codes-ever-used'))
        return

    msg_to_send = language.format_value('mcdonalds-archive-start') + '\n\n'
    for index, code in enumerate(used_codes, start=1):
        msg_to_send += language.format_value('mcdonalds-archive-row', {'index': index, 'code': code.code}) + '\n'

    await query.answer()
    await query.message.answer(msg_to_send)
