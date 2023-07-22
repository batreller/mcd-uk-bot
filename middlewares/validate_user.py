from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

import handlers
from database.queries import get_user
from languages import BaseLanguage

languages = BaseLanguage.languages


class UserMiddleware(BaseMiddleware):
    @staticmethod
    async def on_pre_process_message(message: types.Message, data: dict):
        user = await get_user(message)

        if user.language == 'no':
            await handlers.choose_language_handler(message, languages[user.language], send_hello_message=True)
            raise CancelHandler()

        data['user'] = user
        data['language'] = languages[user.language]

    @staticmethod
    async def on_pre_process_callback_query(query: types.CallbackQuery, data: dict):
        user = await get_user(query)

        query_data = query.data.split('|')
        print(query_data)
        data['op'] = (query_data[0])
        data['data'] = query_data[1:]
        data['user'] = user
        data['language'] = languages[user.language]
