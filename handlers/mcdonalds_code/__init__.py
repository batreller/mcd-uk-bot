import asyncio

from aiogram import types

from database.connector import session
from database.models import User
from database.models.code import Code
from keyboards import mcdonalds_profile_keyboard
from languages import Languages
from services import McDonalds
from settings import config


async def mcdonalds_code_handler(message: types.Message, user: User, language: Languages):
    receipt_code = message.text.replace(' ', '').replace('-', '').upper()
    waiting_message = await message.answer(language.format_value('loading-emoji'))
    text_message = await message.answer(language.format_value('code-validating'))

    mcds = [McDonalds(code=receipt_code) for _ in range(config.AMOUNT_OF_CODES)]
    valids = await asyncio.gather(*[mcd.validate_code() for mcd in mcds])

    print(valids)
    if valids[0]:
        await text_message.edit_text(language.format_value('code-valid'))
        codes = await asyncio.gather(*[mcd.activate_code() for mcd in mcds])

        no_repeatative_codes = set(codes)
        not_unique_codes_ = session.query(Code).filter(Code.code.in_(list(no_repeatative_codes))).all()
        not_unique_codes = set()
        for code in not_unique_codes_:
            not_unique_codes.add(code.code)

        print('-=-=-=-')
        print(len(codes))
        print(codes)
        print(len(no_repeatative_codes))
        print(no_repeatative_codes)
        unique_codes = set()
        for code in codes:
            if code in not_unique_codes:
                continue
            unique_codes.add(code)
            not_unique_codes.add(code)
            new_code = Code(user_id=user.id, code=code, receipt_code=receipt_code)
            session.add(new_code)
        session.commit()

        codes = session.query(Code).filter_by(user_id=user.id, used=False).all()
        # await message.answer(language.format_value('codes-added-successfully', {'amount': len(no_repeatative_codes)}))
        await text_message.edit_text(
            f"{language.format_value('codes-added-successfully', {'amount': len(unique_codes)})}\n\n{language.format_value('mcdonalds-balance', {'codes-amount': len(codes)})}",
            reply_markup=mcdonalds_profile_keyboard(language))
        # await message.answer(language.format_value('codes-added-successfully', {'amount': len(unique_codes)}))


    else:
        # await message.answer(language.format_value('code-invalid'))
        await text_message.edit_text(language.format_value('code-invalid'))

    await waiting_message.delete()
