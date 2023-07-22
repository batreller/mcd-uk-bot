from aiogram import types

from database.connector import session
from database.models import User
from database.models.code import Code
from keyboards import mcdonalds_profile_keyboard
from languages import Languages


async def mcdonalds_handler(message: types.Message, user: User, language: Languages):
    codes = session.query(Code).filter_by(user_id=user.id, used=False).all()

    with open('settings/photos/mcdonalds.jpg', 'rb') as f:
        await message.answer_photo(photo=f,
                                   caption=f"{language.format_value('mcdonalds-command')}\n\n{language.format_value('mcdonalds-balance', {'codes-amount': len(codes)})}",
                                   reply_markup=mcdonalds_profile_keyboard(language))
