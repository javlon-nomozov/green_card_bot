from aiogram.types import Message

from aiogram.dispatcher.filters import BoundFilter
from loader import db

# from data.config import ADMINS


class AdminFilter(BoundFilter):
    async def check(self, message: Message):

        member = await message.chat.get_member(message.from_user.id)

        return member.is_chat_admin()


class BotAdminFilter(BoundFilter):
    async def check(self, message: Message):
        ADMINS = db.select_users_by_role(role='admin')
        # print(ADMINS)
        result = False
        for admin in ADMINS:
            if message.from_user.id in admin:
                result = True
        return result

class BotStaffFilter(BoundFilter):
    async def check(self, message: Message):
        ADMINS = db.select_users_by_role(role='admin')
        STUFFS = db.select_users_by_role(role='staff')
        ADMINS=ADMINS+STUFFS
        print(ADMINS,'admins and stuffs')
        # print(STUFFS,'stuffs')
        result = False
        for admin in ADMINS:
            if message.from_user.id in admin:
                result = True
        return result


