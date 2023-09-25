from aiogram import types

from loader import dp, bot, db
from filters.group_filter import IsGroupFilter

# Ismlarga video topib berish uchun
@dp.message_handler(IsGroupFilter() ,state='*')
async def bot_echo(message: types.Message):
    pass