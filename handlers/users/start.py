from googletrans import Translator

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

# from data.config import CHANNELS, GROUPS
# from keyboards.inline import check_button
# from utils.misc import subscription
from keyboards.inline import settings_keyboard
from loader import dp, db

translator = Translator()


@dp.message_handler(CommandStart(), state="*")
async def start(msg: types.Message):
    user = db.select_user(id=msg.from_user.id)

    if user:
        user_lang = user[3]
    #     text = translator.translate(text=f'Qadirli XXXX siz allaqachon botdan foydalanib boshlagansiz', src='uz',
    #                                 dest=user_lang).text.replace('XXXX', msg.from_user.mention)
    #     await msg.answer(text=text)
    else:
        lang = msg.from_user.language_code
        if not lang in ['en', 'uz', 'ru']:
            lang = 'en'
        db.add_user(name=msg.from_user.full_name,
                    id=msg.from_user.id,
                    language=lang)
    #     text = translator.translate(text=f'Salom hurmatli XXXX{msg.from_user.mention}', dest=lang, src='uz').text.replace('XXXX', msg.from_user.mention)
    #     await msg.answer(text=text, reply_markup=await settings_keyboard(lang=lang))

    await msg.answer(f"Salom hurmatli {msg.from_user.mention}")