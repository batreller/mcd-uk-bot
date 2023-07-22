from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import MemoryStorage
from aiogram.dispatcher.filters import Text

from database.connector import Base, engine
from handlers import start_handler, mcdonalds_code_handler, settings_handler
from handlers.inline import get_code_handler, del_code_handler, settings_change_language_handler
from handlers.inline.choose_language import change_language_handler
from handlers.inline.mcdonalds_profile.archived_codes import archived_codes_handler
from handlers.mcdonalds import mcdonalds_handler
from handlers.subway import subway_handler
from languages import BaseLanguage
from languages.import_languages import import_languages
from middlewares import UserMiddleware
from settings import config
from utlis.filters import LangFilter, McDonaldsCodeFilter, GetCodeFilter, DelCodeFilter, ArchivedCodesFilter, \
    SettingsFilter, ChangeLanguage

import_languages()

bot = Bot(token=config.BOT_TOKEN, parse_mode='html')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(UserMiddleware())

dp.register_message_handler(start_handler, commands=['start'])
dp.register_message_handler(mcdonalds_code_handler, McDonaldsCodeFilter())
dp.register_message_handler(mcdonalds_handler, Text(['McDonald\'s 🍔']))
dp.register_message_handler(subway_handler, Text(['Subway 🌮']))
dp.register_message_handler(settings_handler, SettingsFilter())

dp.register_callback_query_handler(settings_change_language_handler, ChangeLanguage())
dp.register_callback_query_handler(change_language_handler, LangFilter())
dp.register_callback_query_handler(get_code_handler, GetCodeFilter())
dp.register_callback_query_handler(archived_codes_handler, ArchivedCodesFilter())
dp.register_callback_query_handler(del_code_handler, DelCodeFilter())
Base.metadata.create_all(bind=engine)

print(BaseLanguage.languages)
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp)
