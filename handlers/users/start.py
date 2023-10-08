from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart


from keyboards.inline import settings_keyboard
from loader import dp, db



@dp.message_handler(CommandStart(), state=None)
async def start(msg: types.Message):
    user = db.select_user(id=msg.from_user.id)

    if user:
        user_lang = user[3]
    else:
        lang = msg.from_user.language_code
        if not lang in ['en', 'uz', 'ru']:
            lang = 'en'
        db.add_user(name=msg.from_user.full_name,
                    id=msg.from_user.id,
                    language=lang)
    
    
    await msg.answer(f"Salom hurmatli {msg.from_user.full_name}\n\n"
                    f"!⚠️Diqqat⚠️! bot orqali Green Card anketasini to`ldirishdan oldin foydalanish /shartlar bilan tanishing.\n"
                    "Anketa to'ldirish pulli.\n\nYakka bo`ydoq 8 000 so`m, yoki 68 rubl "
                    "Oilaviy anketaga qolgan har bir odam uchun 4 000 so'm yoki 34 rubl dan\n\n"
                    "To'lov anketa to'ldirilgandan keyin amalga oshirilishi shart.\n"
                    "To`lovni amalga oshirilmagan anketalar ro'yxatdan o'tkazilmaydi.\n\n"
                    "Agar /shartlar ga rozi bo'lsangiz /anketa to'ldirishni boshlashingiz mumkin")
    
@dp.message_handler(CommandStart(), state="*")
async def start(msg: types.Message):
    await msg.answer(f"Salom hurmatli {msg.from_user.full_name}, sizdan so'ralgan malumotni kiriting")