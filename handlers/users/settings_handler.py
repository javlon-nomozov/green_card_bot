import logging

from aiogram.types import CallbackQuery, Message

from aiogram.dispatcher.filters import Text
from googletrans import Translator

from keyboards.inline import settings_keyboard
from loader import dp, db

translator = Translator


@dp.message_handler(commands='setting')
async def setting(msg: Message):
    user = db.select_user(id=msg.from_user.id)
    lang = user[3]
    text = f"<b>Settings ⚙</b>\n\nlanguage: {lang}"
    await msg.answer(text, reply_markup=await settings_keyboard(lang=lang))


@dp.callback_query_handler(Text(contains='lang:'))
async def setting(call: CallbackQuery):
    update_lang = call.data.replace('lang:', '')
    user = db.select_user(id=call.from_user.id)
    logging.info(user)
    lang = user[3]
    text = f"<b>Settings ⚙</b>\n\nlanguage: {update_lang}"
    await call.message.edit_text(text=text, reply_markup=await settings_keyboard(lang=update_lang))
    db.update_user_language(lang=update_lang, id=call.from_user.id)
    user = db.select_user(id=call.from_user.id)
    logging.info(user)



