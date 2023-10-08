from googletrans import Translator

from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from data.config import GROUPS
from loader import dp, bot

translator = Translator()


# all commmands
# help - tushunmovchilik bo'lganida batafsil malumot
# /comunity - tushunmovchilik bo'lganida batafsil malumot
# /donate - qo'llab quvvatlovchilar uchun karta raqami


@dp.message_handler(text='Bekor qilish')
@dp.message_handler(commands='cancel')
async def cancel(message: Message):
    pass
    # await state.finish()
    # await msg.answer('Ism kiriting')

@dp.message_handler(commands='cancel', state="*")
@dp.message_handler(text='Bekor qilish', state="*")
async def cancel(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer('Anketa bekor qilindi\n\nYangi boshlash uchun: /anketa')


@dp.message_handler(commands='shartlar')
async def privacy(msg: Message):
    await msg.answer("!⚠️Diqqat⚠️!\n\nIshtirok etish shartlari:\n\n1️⃣Kodi sizga berilmaydi... (Agar yutadigan bo'lsangiz biz o'zimiz siz bilan bog'lanamiz va visa uchun hujjatlar tayyorlashda ham yordam beramiz.)\n\n2️⃣Botdan chiqib ketmaslikga harakat qiling... (agarda siz bergan tel nomer ish faoliyatidan toxtaydigan bolsa siz bilan boglana olmaymiz.)\n\n"
                     "3️⃣Telegram mavjud bolgan nomer kiritishingizni sorab qolamiz... (bu majburiy emas, lekin, sizdagi berilgan ma'lumotlarda royxatdan otgazishiga vaqtida qandaydir hatolik yuzaga kelsa siz bilan boglanishosonroq bo'ladi.)\n\n<b>Agar barcha shartlarga rozi bo'lsangiz /anketa to'ldirishingiz mumkin</b>")