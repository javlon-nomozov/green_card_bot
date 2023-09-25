import asyncio
import sqlite3
import os

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from filters.admins_filter import BotAdminFilter, BotStaffFilter
from loader import dp, bot, db
from states.main import NewSubChat

from keyboards.inline.main import chats_inline, staffs_inline

@dp.message_handler(BotAdminFilter(), commands='add_staff', commands_prefix='$')
async def send_ad(msg: Message):
    new_staff_id = msg.text.replace('$add_staff', '').replace(' ', '')
    if new_staff_id:
        db.update_user_role(role='staff', id=new_staff_id)
    else:
        await msg.answer('comand xato ishkatilgan bo\'lishi mumkin\nEx:$add_user 0123456')
    await msg.answer('Yangi xodim qo\'shildi')


@dp.message_handler(BotAdminFilter(), commands='count_user', commands_prefix='$')
async def send_ad(msg: Message):
    user_count = db.count_users()
    await msg.answer(f'Foydalanuvchilar soni:{user_count[0]}')


@dp.message_handler(BotAdminFilter(), commands='send_ad', commands_prefix='$')
async def send_ad(msg: Message):
    src_msg = msg.reply_to_message
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        try:
            audio = src_msg.audio.file_id
            caption = src_msg.caption
            await bot.send_audio(chat_id=user_id, audio=audio, caption=caption)
        except:
            pass
        try:
            video = src_msg.video.file_id
            caption = src_msg.caption
            await bot.send_video(chat_id=user_id, video=video, caption=caption)
        except:
            # await bot.send_message(chat_id=user_id, text=src_msg.video[-1])
            pass
        try:
            photo = src_msg.photo[-1].file_id
            caption = src_msg.caption
            await bot.send_photo(chat_id=user_id, photo=photo, caption=caption)
        except:
            pass
        try:
            voice = src_msg.voice.file_id
            caption = src_msg.caption
            await bot.send_voice(chat_id=user_id, voice=voice, caption=caption)
        except:
            pass
        try:
            document = src_msg.document.file_id
            caption = src_msg.caption
            await bot.send_document(chat_id=user_id, document=document, caption=caption)
        except:
            pass
        try:
            latitude = src_msg.location.latitude
            longitude = src_msg.location.longitude
            await bot.send_location(chat_id=user_id, latitude=latitude, longitude=longitude)
        except:
            pass
        try:
            await bot.send_message(chat_id=user_id, text=src_msg.text)
        except:
            pass
        await asyncio.sleep(0.05)
    await msg.reply(text='Xabar muvaffaqqiyatli tarqatildi🤩')


# yangi majburiy chat qo'shish uchun<<<<
@dp.message_handler(BotAdminFilter(), commands='add_sub_chat', commands_prefix='$')
async def add_video(msg: Message):
    await msg.answer("yangi chat IDsi yoki linkini kiriting \nEx: -12341341423537 // @example;")
    await NewSubChat.id_link.set()


@dp.message_handler(BotStaffFilter(), state=NewSubChat.id_link)
async def add_video(msg: Message,  state: FSMContext):
    await state.update_data(id_link=msg.text)
    # await state.update_data(message_id=('message:',))
    await msg.answer("Bu chatga izoh bering\n\neslatma:"
                     " izoh foydalanuvchilarni majburiy azoligini tekshirish xabarida ko'rinadi")
    await NewSubChat.next()

@dp.message_handler(BotStaffFilter(), state=NewSubChat.description)
async def add_video2(msg: Message, state: FSMContext):
    description = msg.text
    async with state.proxy() as data:
        id_link = data.get("id_link")
    await state.finish()
    try:
        db.add_chat(id_link, 'true', description)
        await msg.answer('Yangi chat qo\'shildi')
    except Exception as err:
        await msg.answer(f'Bu chat mavjud bo\'lishi mumkin\n{err}')
# >>>>

# <<<< chatlardan birini o'chirish
@dp.message_handler(BotAdminFilter(), commands='del_chat', commands_prefix='$')
async def add_video(msg: Message):
    await msg.answer("Chatni o'chirish uchun ustiga tanlang\nBarcha chat lar:", reply_markup=await chats_inline(call='del_chat', all=True))


@dp.callback_query_handler(text_contains="del_chat")
async def buy_books(call: CallbackQuery):
    await call.message.answer(call.data)
    db.delete_chat(call.data.replace('call_del_chat_', ''))
    try:
        os.system('shutdown -r -t 0')
    except Exception as err:
        await call.message.answer(f'<b>Xatolik:</b> \n{err}')
    await call.message.answer("O'chirildi")
# >>>>


@dp.message_handler(BotAdminFilter(), commands='del_staff', commands_prefix='$')
async def add_video(msg: Message):
    await msg.answer("Hodimni ro'yxatdan o'chirish uchun tanlang\nBarcha chat lar:",
                     reply_markup=await staffs_inline(call='del_staff'))


@dp.callback_query_handler(text_contains="call_del_staff")
async def buy_books(call: CallbackQuery):
    await call.message.answer(call.data)
    db.update_user_role('user' ,call.data.replace('call_del_staff_', ''))
    await call.message.answer("O'chirildi")
