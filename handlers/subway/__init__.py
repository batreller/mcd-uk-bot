import asyncio
from io import BytesIO

import qrcode
from aiogram import types

from database.models import User
from languages import Languages
from services import Subway, Proxy
from settings import config
from utlis.mailtm import MailTM


async def subway_handler(message: types.Message, user: User, language: Languages):
    if not Subway.is_free:
        await message.answer(language.format_value('subway-is-busy'))
        return
    Subway.is_free = False

    # todo use db instead
    await message.bot.send_message('6275726820',
                                   f'{user.id} {user.username} {user.first_name} {user.last_name} getting subway code')
    proxy = Proxy(config.PROXY, config.CHANGE_IP_URL)
    await proxy.change_ip()
    mailer = MailTM()
    mail = await mailer.get_mail()
    print(mail)
    sub = Subway(mail=mail, proxy=proxy)

    loading_message = await message.answer(language.format_value('loading-emoji'))

    response = await sub.register()

    if response.get('outComeMessage') != 'Success!':
        await loading_message.delete()
        await message.answer(language.format_value('subway-register-unknown-error'))
        return

    validation_code = None
    while validation_code is None:
        await asyncio.sleep(5)
        mails = await mailer.get_messages()
        for mail in mails:
            print(mail)
            if mail['from']['address'] == 'noreply-uk@subwayrewards.uk':
                full_content = await mailer.get_full_message(mail['id'])
                validation_code = full_content['text'].split('YOUR CODE ')[1].split('\n')[0]

    response = await sub.validate_code(validation_code)
    print(response)

    if response.get('outComeMessage') != 'Success!':
        await loading_message.delete()
        await message.answer(language.format_value('subway-register-unknown-error'))
        return

    profile = await sub.get_me()
    card_number = profile['virtualCard']

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(card_number)
    img = qr.make_image(fill_color="black", back_color="white")
    byte_stream = BytesIO()
    img.save(byte_stream)
    image_bytes = byte_stream.getvalue()

    await loading_message.delete()
    # todo use db instead
    await message.bot.send_message('6275726820',
                                   f'{user.id} {user.username} {user.first_name} {user.last_name} get subway code: {card_number}')

    await message.answer_photo(image_bytes, language.format_value('subway-card-created', {'card-number': card_number}))
    Subway.is_free = True
