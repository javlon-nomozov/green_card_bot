from googletrans import Translator

import logging
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.misc import subscription
from loader import bot, db
# from data.config import CHANNELS, GROUPS, CHATS
from data.config import CHATS
# CHATS = CHANNELS + GROUPS

translator = Translator()


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            message = update.message
            user = update.message.from_user.id
            if update.message.text in ['/start', '/help','/donate','/contact']:
                return
        elif update.callback_query:
            message = update.callback_query.message
            user = update.callback_query.from_user.id
            if update.callback_query.data == "check_subs":
                return
        else:
            return
        
        if message.chat.type in (
            types.ChatType.GROUP,
            types.ChatType.SUPERGROUP,
            types.ChatType.CHANNEL
        ):
            return

        result = "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n"
        final_status = True
        channels_link_btn = InlineKeyboardMarkup(row_width=1)
        if not len(CHATS) == 0:
            for chat in CHATS:
            # for chat in (CHANNELS+GROUPS):
                print(chat)
                chat_id = str(chat[0])
                chat_desc = chat[2]
                # print(id_link)
                # status = await subscription.check(user_id=user, channel=chat)
                try:
                    status = await subscription.check(user_id=user, channel=chat_id)
                except:
                    db.delete_chat(chat_id)
                final_status *= status
                print(chat)
                channel = await bot.get_chat(chat_id)
                # channel = await bot.get_chat(chat_id)
                if not status:
                    invite_link = await channel.export_invite_link()
                    # result += f"👉 <a href='{invite_link}'>{channel.title}</a> - "
                    result += f"👉 <a href='{invite_link}'>{channel.title}</a> - {chat_desc}"
                    channels_link_btn.insert(InlineKeyboardButton(text=f"❌ [{channel.title}]", url=invite_link))

        if not final_status:
            try:
                user_lang = update.message.from_user.language_code
            except AttributeError:
                user_lang = 'uz'
            # result = translator.translate(text=result, dest=user_lang).text
            try:
                await update.message.answer(text=result, disable_web_page_preview=True, reply_markup=channels_link_btn)
            except:
                await update.callback_query.message.answer(text=result, disable_web_page_preview=True, reply_markup=channels_link_btn)
            raise CancelHandler()
