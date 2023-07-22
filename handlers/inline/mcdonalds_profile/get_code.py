from io import BytesIO

import qrcode
from aiogram import types

from database.connector import session
from database.models import User
from database.models.code import Code
from keyboards import mcdonalds_profile_keyboard
from keyboards.delete_code import mcdonalds_delete_code
from languages import Languages


async def get_code_handler(query: types.CallbackQuery,
                           # op: str,
                           data: list,
                           user: User,
                           language: Languages):
    codes = session.query(Code).filter_by(user_id=user.id, used=False).all()
    if len(codes) <= 0:
        await query.answer(language.format_value('no-codes-available'))
    else:
        mcd_code = codes[0].code
        codes[0].used = True
        session.commit()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(mcd_code)
        img = qr.make_image(fill_color="black", back_color="white")
        byte_stream = BytesIO()
        img.save(byte_stream)
        image_bytes = byte_stream.getvalue()

        await query.message.answer_photo(image_bytes, caption=language.format_value('mcd-code', {'code': mcd_code}), reply_markup=mcdonalds_delete_code(language))
        await query.answer()
        await query.message.edit_caption(f"{language.format_value('mcdonalds-command')}\n\n{language.format_value('mcdonalds-balance', {'codes-amount': len(codes)-1})}", reply_markup=mcdonalds_profile_keyboard(language))
