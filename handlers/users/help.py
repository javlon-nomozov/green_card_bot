from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from filters.admins_filter import BotAdminFilter


@dp.message_handler(CommandHelp(), BotAdminFilter())
async def bot_help_for_admin(message: types.Message):
    await message.answer("$send_ad - reklama tarqatish"
                         "\n$count_user - foydalanuvchilar soni"
                         "\n$add_staff - Hodim tayinlash"
                         "\n$add_sub_chat - yangi majburiy azolik chat qo'shish"
                         "\n$del_chat - mavjud chatni o'chirish"
                         "\n$del_staff - mavjud hodimni bo'shatish")


@dp.message_handler(CommandHelp(), state=None)
async def bot_help_for_admin(message: types.Message):
    await message.answer("Green card /anketa sini to'ldiruvchi bot")