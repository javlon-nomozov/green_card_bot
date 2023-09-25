from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db
# from .callback_data import del_chat, del_staff


async def chats_inline(call, all):
    if all:
        chats = db.select_all_chat()
    else:
        chats = db.select_must_sub_chat()
    chats_key = InlineKeyboardMarkup(row_width=1)
    for chat in chats:
        chat_id = chat[0]
        btn = InlineKeyboardButton(text=f"❌ [{chat_id}]",#"call_del_chat"
                                      callback_data=f"call_{call}_{chat_id}")
        print(f"{call}_{chat_id}")
        chats_key.insert(btn)
    return chats_key

async def staffs_inline(call:str):
    staffs = db.select_users_by_role(role='staff')
    staffs_key = InlineKeyboardMarkup(row_width=1)
    for staff in staffs:
        print(staff)
        staff_id = staff[0]
        btn = InlineKeyboardButton(text=f"❌ [{staff_id}]",
                                      callback_data=f"call_{call}_{staff_id}")
        print(f"{call}_{staff_id}")
        staffs_key.insert(btn)
    return staffs_key

