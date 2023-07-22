from aiogram import types
from aiogram.dispatcher.filters import Filter

from languages import Languages


class LangFilter(Filter):
    @staticmethod
    async def check(query: types.CallbackQuery) -> bool:
        data_parts = query.data.split('|')
        return len(data_parts) > 0 and data_parts[0] == 'LANG'


class SettingsFilter(Filter):
    @staticmethod
    async def check(message: types.Message) -> bool:
        languages = Languages.languages
        for language in languages:
            if languages[language].format_value('settings-button') == message.text:
                return True
        return False


class ChangeLanguage(Filter):
    @staticmethod
    async def check(query: types.CallbackQuery) -> bool:
        data_parts = query.data.split('|')
        return data_parts[0] == 'SETTINGS' and data_parts[1] == 'CHANGE_LANG'


class GetCodeFilter(Filter):
    @staticmethod
    async def check(query: types.CallbackQuery) -> bool:
        data_parts = query.data.split('|')
        return data_parts[0] == 'MCD' and data_parts[1] == 'GETCODE'


class ArchivedCodesFilter(Filter):
    @staticmethod
    async def check(query: types.CallbackQuery) -> bool:
        data_parts = query.data.split('|')
        return data_parts[0] == 'MCD' and data_parts[1] == 'ARCHIVE'


class DelCodeFilter(Filter):
    @staticmethod
    async def check(query: types.CallbackQuery) -> bool:
        data_parts = query.data.split('|')
        return data_parts[0] == 'MCD' and data_parts[1] == 'DELCODE'


class McDonaldsCodeFilter(Filter):
    @staticmethod
    async def check(message: types.Message) -> bool:
        return len(message.text.replace('-', '').replace(' ', '')) == 12
