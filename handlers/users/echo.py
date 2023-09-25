from aiogram import types

from loader import dp


# eco bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.html_text)