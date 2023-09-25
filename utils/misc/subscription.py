from typing import Union

from aiogram import Bot


async def check(user_id, channel: Union[int, str]):
    try:
        bot = Bot.get_current()
    except:
        pass
    try:
        member = await bot.get_chat_member(user_id=user_id, chat_id=channel)
        result = member.is_chat_member()
    except:
        result = False
    return result