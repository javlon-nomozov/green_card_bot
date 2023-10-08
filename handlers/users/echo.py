import re
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from utils.main import id_gen
from states.main import Anketa
from keyboards.default import datekey, default_key 


@dp.message_handler(state=None, commands='anketa')
async def bot_echo(message: types.Message):
    await message.answer('Anketa toldirish jarayoni boshlandi')
    await message.answer('Doimo ishlovchi (va telegrami bor) telefon raqamingizni kiriting (bu raqamga natija elon qilinadi)', reply_markup=default_key.cancel_key) 
    await Anketa.phone.set()
    # print('phone')
    

@dp.message_handler(state=Anketa.phone)
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: phone')
    await state.update_data(ch_fname=["fname"])
    await state.update_data(ch_lname=["lname"])
    await state.update_data(ch_birth_year=["birth_year"])
    await state.update_data(ch_birth_month=["birth_month"])
    await state.update_data(ch_gender=["gender"])
    await state.update_data(ch_birth_day=["birth_day"])
    await state.update_data(ch_city=["birth_city"])
    await state.update_data(ch_country=["birth_country"])
    await state.update_data(ch_photo=["photo"])
    
    phone_num = message.text
    pattern = r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'

    if re.match(pattern, phone_num):
        await state.update_data(phone_num=phone_num)
        await Anketa.fname.set()
        # print('fname')
        await message.answer('Ism:', reply_markup=default_key.cancel_key)
    else:
        await message.answer('Kiritgan qiymatingiz telefon raqam bo\'lishi va ortiqcha belgilar bo\'lmasligi kerak: +998 99 1234567; +998991234567'
                             "\nEslatma: <u>Kiritgan telefon raqamingizga <b>Green card</b> javobi elon qilinadi</u>")


@dp.message_handler(state=Anketa.fname)
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: fname')
    await message.answer('Familiya:', reply_markup=default_key.cancel_key)
    await state.update_data(fname=message.text)
    await Anketa.lname.set()
    # print('lname')


@dp.message_handler(state=Anketa.lname)
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: lname')
    await message.answer('Jinsi:', reply_markup=default_key.gender)
    await state.update_data(lname=message.text)

    await Anketa.gender.set()
    # print('gender')


@dp.message_handler(state=Anketa.gender)
async def bot_echo(message: types.Message, state: FSMContext):
    if message.text in ['Erkak', 'Ayol']:
        # print('state: lname')
        await message.answer("Tug'ilgan yil:", reply_markup=default_key.cancel_key)
        await state.update_data(gender=message.text)

        await Anketa.birth_year.set()
        # print('year')
    else:
        await message.answer('Xato qiymat kiritdingiz. Tugmalardan birini tanlang, yoki bekor qiling:', reply_markup=default_key.gender)


@dp.message_handler(state=Anketa.birth_year)
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: year')
    try:
        year = int(message.text)
        if year < 2006 and year > 1075:
            await message.answer("Tug'ilgan oy:", reply_markup=datekey.months)
            await state.update_data(birth_year=year)
            await Anketa.birth_month.set()
            # print('month')
        else:
            await message.answer('Yosh chegarasiga to\'g\'ri kelmaydi')
    except:
        await message.answer('Siz kiritgan qiymat faqat sonlardan iborat bo\'lsin')


@dp.message_handler(state=Anketa.birth_month)
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: month')
    month = message.text
    if month in ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Avgust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"]:
        await message.answer("Tug'ilgan sana:", reply_markup=default_key.cancel_key)
        await state.update_data(birth_month=message.text)
        await Anketa.birth_day.set()
        # print('day')
    else:
        await message.answer("to'g'ri qiymat kiriting:", reply_markup=datekey.months)


@dp.message_handler(state=Anketa.birth_day)
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: day')
    day = message.text
    if day.isdigit() and int(day) <= 31 and int(day) > 0:
        await message.answer("Tug'ilgan mamlakat:",reply_markup=default_key.cancel_key)
        await state.update_data(birth_day=day)
        await Anketa.birth_country.set()
        # print('birth_city')
    else:
        await message.answer('Xato sana kiritdingiz: sana 1-31 atrofida bo\'lishi mumkin')


@dp.message_handler(state=Anketa.birth_country)
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: country')
    await message.answer("Tug'ilgan shaxar va to'liq manzil:",reply_markup=default_key.cancel_key)
    await state.update_data(birth_country=message.text)
    await Anketa.birth_city.set()
    # print('birth_country')


@dp.message_handler(state=Anketa.birth_city)
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: country')
    await message.answer("""Surat kiriting:\nAsosiy narsalarni yodda tuting: o'lcham, ifoda, boshning holati, fon va yuzni yashirishi mumkin bo'lgan barcha narsalar (sochlar, soyalar, ko'zoynak, ortiqcha yorug'lik va hk). Ko'pgina misollarda foydali "Foto maslahatlar" berilgan:""")
    await message.answer_photo('https://travel.state.gov/content/dam/passports/photo_examples/_MG_3425_GOOD.png/jcr:content/renditions/original', 
                               caption='✅ <b>Qoniqarli surat</b>\nQabul qilinadi— Surat tiniq va rangli, terining ohangini aniq aks ettiradi va soyalarsiz toʻgʻri koʻrsatiladi.')

    await message.answer_photo('https://travel.state.gov/content/dam/passports/photo_examples/Try%20underexposed%20(3).png/jcr:content/renditions/original', 
                               caption="❌ <b>Qoniqarsiz surat</b>\nQabul qilib bo'lmaydigan — Surat kam qo'yilgan"
                               "\nFotosurat bo'yicha maslahat: Surat haddan tashqari ko'p yoki kam bo'lmasligi kerak. Siz kameraning ekspozitsiyasini sozlashingiz yoki qo'shimcha yorug'likdan foydalanishingiz kerak. ")

    await message.answer_photo('https://travel.state.gov/content/dam/passports/photo_examples/_MG_3429_blue.png/jcr:content/renditions/original', 
                               caption="❌ <b>Qoniqarsiz surat</b>\nQabul qilib bo'lmaydigan — rang aniq emas\n"
                               "Fotosurat boʻyicha maslahat: Yorugʻlikka qarab kamerangizning oq balansi sozlamasini oʻzgartirishingiz kerak boʻlishi mumkin.")

    await message.answer_photo('https://travel.state.gov/content/dam/passports/photo_examples/CROPPED-DSC_0067.jpg/jcr:content/renditions/original', 
                               caption="❌ <b>Qoniqarsiz surat</b>\nQabul qilib bo'lmaydigan — yuz va fonda soyalar mavjud\n"
                               "Fotosurat uchun maslahat: yuz va fonda soyalar paydo bo'lishining oldini olish uchun siz bir xil (Kamera bilan bir tomondan qragan) yoritishni ishlatishingiz kerak.")

    await message.answer('Sifatli (600px x 600px yoki 51mm x 51mm) rasmingizni kiriting:',reply_markup=default_key.cancel_key)
    await state.update_data(birth_city=message.text)
    await Anketa.photo.set()
    # print('photo')


@dp.message_handler(state=Anketa.photo, content_types='photo')
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: photo')
    photo = message.photo[-1].file_id
    await message.answer("Talim darajasi:", reply_markup=default_key.edu_grade)
    await state.update_data(photo=photo)
    await Anketa.edu_grade.set()
    # print('edu_grade')

@dp.message_handler(state=Anketa.photo)
async def bot_echo(message: types.Message, state: FSMContext):
    await message.answer("Rasim fayl kiritishingiz kerak")


@dp.message_handler(state=Anketa.edu_grade)
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: edu_grade')
    if message.text in ["Maktab (9-10-sinf)", "Maktab(11-sinf)", "Magistratura", "Oliy malumot", "Tugalanmagan oliy", "Kollej", "Litsey"]:
        await message.answer("Oilaviy holatingizni kiriting.", reply_markup=default_key.marriage_state)
        await state.update_data(edu_grade=message.text)
        await Anketa.marriage_state.set()
        # print('marriage_state')
    else:
        await message.answer('Malumot hato!!!\nIltimos sizga berilgan tugmalardan birini bosing yoki\nAnketani bekor qiling:',reply=default_key.cancel_key)


@dp.message_handler(state=Anketa.marriage_state)
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: marriage_state')        
    if message.text in ["Beva/yolg'iz", "Ajrashgan/ajrashuvda", "Turmush qurgan", "Turmush qurmagan"]:
        await message.answer("Farzandlar soni (20 yoshgacha bo'lganlari)(agar yo'q bo'lsa 0 kiriting):",reply_markup=default_key.cancel_key)
        await state.update_data(marriage_state=message.text)
        if message.text == "Turmush qurgan":
            await state.update_data(session_num=0)
        else:
            await state.update_data(session_num=1)
        await Anketa.child_count.set()
        # print('child_count')
    else:
        await message.answer('Malumot hato!!!\nIltimos sizga berilgan tugmalardan birini bosing yoki', reply_markup=default_key.marriage_state)


@dp.message_handler(state=Anketa.child_count)
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: child_count')
    try:
        async with state.proxy() as data:
            # marriage_state = data.get("marriage_state")
            session_num = data.get("session_num")
            # print(session_num)
        child_count = int(message.text)
        # print(child_count)
        if session_num == 1 and child_count == 0:
            id = await id_gen()
            await state.update_data(id=id)
            price = 8000
            async with data:
                # print('data')
                phone_num = data.get("phone_num")
                fname = data.get("fname")
                lname = data.get("lname")
                gender = data.get("gender")
                birth_year = data.get("birth_year")
                birth_month = data.get("birth_month")
                birth_day = data.get("birth_day")
                birth_city = data.get("birth_city")
                birth_country = data.get("birth_country")
                edu_grade = data.get("edu_grade")
                marriage_state = data.get("marriage_state")
                photo = data.get("photo")
            text = f"ID: {id}\ntel: {phone_num};\nAkketa: Shaxsiy;\nIsm: {fname};\nFamilya: {lname};\nJinsi: {gender};\nTug'ilgan sanasi: {birth_year}-yil {birth_day}-{birth_month};\nTug'ilgan joyi: {birth_country}>{birth_city};\nTalim darajasi: {edu_grade};\nOilaviy holati: {marriage_state}"
            # print("Malumotlar toliq yig'ildi")
            # print(photo)
            # print(text)
            await message.reply_photo(photo=photo,caption=text+"\n\n\n<b>!!!Malumotlaringizni tekshirib oling!!!</b>\nAgar xatolik bo'lsa anketani bekor qiling:", reply_markup=default_key.cancel_key)
            # await bot.send_photo(chat_id=-1001896668985,photo=photo,caption=text)
            # await message.answer(text=f"<code>{data.as_dict()}</code>")[{'photo': photo, 'text': text}]
            await state.update_data(messages=[{'photo': photo, 'text': text}])
            await state.update_data(price=price)
            await Anketa.bill.set()
            
            await message.answer(text=f"<b>Raxmat</b>\nAnketa to'ldirilishi nixoyasiga yetdi \n!!!Iltimos malumotlaringizni tekshiring!!! \nva<b> keyin {price} so'm yoki {price* 0.017} rubl tlo'langanligi to'lov qog'ozini(chekni) yuboring</b>"
                                " va uni hodimlar ko'rib chiqib, agarda xatolik mavjud bo'lsa sizga bog'lanishadi",reply_markup=default_key.cancel_key)
        elif 9 > child_count >=0:
            if session_num >= 1:
                await message.answer(f"{session_num}-farzandingiz ismi:",reply=default_key.cancel_key)
            else:
                await message.answer("Turmush o'rtog'ingiz ismi:\nbekor qiling:",reply=default_key.cancel_key)
            await state.update_data(child_count=child_count)
            await Anketa.ch_fname.set()
            # print('ch_fname')
        else:
            await message.answer("Qiymat notog'ri!!! 0-8 bo'lishi mumkin")
    except:
        await message.answer('Malumot hato!!!  Iltimos farzandlaringiz sonini kiriting(faqat son)',reply=default_key.cancel_key)

@dp.message_handler(state=Anketa.ch_fname)
async def bot_echo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ch_fname = data.get("ch_fname")

    name = message.text
    ch_fname.append(name)
    await message.answer(f"{name} ning Familyasi:")
    await state.update_data(ch_fname=ch_fname)
    await Anketa.ch_lname.set()


@dp.message_handler(state=Anketa.ch_lname)
async def bot_echo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ch_lname = list(data.get("ch_lname"))
        ch_fname = list(data.get("ch_fname"))
        gender = data.get("gender")
        ch_gender = list(data.get("ch_gender"))
        session_num = data.get("session_num")
    lname = message.text
    ch_lname.append(lname)
    await state.update_data(ch_lname=ch_lname)
    if session_num == 0:
        # print('gender288:',gender)
        if gender == 'Erkak':
            ch_gender.append('Ayol')
        else:
            ch_gender.append('Erkak')
        await message.answer(f"{ch_fname[-1]} {lname}ning tug'ilgan yili:")
        await state.update_data(ch_gender=ch_gender)
        await Anketa.ch_birth_year.set()
    else:
        # print(ch_lname)
        await message.answer(f"{ch_fname[-1]} {lname} ning jinsi:", reply_markup=default_key.gender)
        await Anketa.ch_gender.set()
        

@dp.message_handler(state=Anketa.ch_gender)
async def bot_echo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ch_lname = list(data.get("ch_lname"))
        ch_gender = list(data.get("ch_gender"))
        ch_fname = list(data.get("ch_fname"))
    if message.text in ['Erkak', 'Ayol']:
        # print('state: lname')
        ch_gender.append(message.text)
        await message.answer(f'{ch_fname[-1]} {ch_lname[-1]}ning tug\'ilgan yilini kiriting:',reply=default_key.cancel_key)
        await state.update_data(ch_gender=ch_gender)

        await Anketa.ch_birth_year.set()
        # print('year')
    else:
        await message.answer('Xato qiymat kiritdingiz. Tugmalardan birini tanlang, yoki\nbekor qiling:', reply_markup=default_key.gender)


@dp.message_handler(state=Anketa.ch_birth_year)
async def bot_echo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ch_lname = list(data.get("ch_lname"))
        ch_fname = list(data.get("ch_fname"))
        ch_birth_year = list(data.get("ch_birth_year"))

    # print('state: year')
    try:
        year = int(message.text)
        if year < 2024 and year > 1970:
            ch_birth_year.append(year)
            await message.answer(f'{ch_fname[-1]} {ch_lname[-1]}ning tug\'ilgan oyi:', reply_markup=datekey.months)
            await state.update_data(ch_birth_year=ch_birth_year)
            await Anketa.ch_birth_month.set()
            # print('month')
        else:
            await message.answer('Yosh chegarasiga to\'g\'ri kelmaydi')
    except:
        await message.answer('Siz kiritgan qiymat faqat sonlardan iborat bo\'lsin')


@dp.message_handler(state=Anketa.ch_birth_month)
async def bot_echo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ch_birth_month = data.get("ch_birth_month")
        ch_lname = list(data.get("ch_lname"))
        ch_fname = list(data.get("ch_fname"))
    ch_birth_month.append(message.text)
    # print('state: month')
    month = message.text
    if month in ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Avgust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"]:
        await message.answer(f'{ch_fname[-1]} {ch_lname[-1]}ning tug\'ilgan sanasi (faqat sana (sonda)):'
                             '\nMasalan: 14 ; 20; 31;')
        await state.update_data(ch_birth_month=ch_birth_month)
        await Anketa.ch_birth_day.set()
        # print('day')
    else:
        await message.answer("to'g'ri qiymat kiriting:", reply_markup=datekey.months)


@dp.message_handler(state=Anketa.ch_birth_day)
async def bot_echo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ch_birth_day = data.get("ch_birth_day")
        ch_lname = list(data.get("ch_lname"))
        ch_fname = list(data.get("ch_fname"))
    ch_birth_day.append(message.text)
    # print('state: day')
    day = message.text
    if day.isdigit() and int(day) <= 31 and int(day) > 0:
        await message.answer(f"{ch_fname[-1]} {ch_lname[-1]}ning tug'ilgan davlati:\n",reply=default_key.cancel_key)
        await state.update_data(ch_birth_day=ch_birth_day)
        await Anketa.ch_country.set()
        # print('birth_city')
    else:
        await message.answer('Xato sana kiritdingiz: sana 1-31 atrofida bo\'lishi mumkin')


@dp.message_handler(state=Anketa.ch_country)
async def bot_echo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ch_country = list(data.get("ch_country"))
        ch_lname = list(data.get("ch_lname"))
        ch_fname = list(data.get("ch_fname"))
    ch_country.append(message.text)
    # print('state: country')
    await message.answer(f"{ch_fname[-1]} {ch_lname[-1]}ning tug'ilgan shaxri va to'liq manzili:\n",reply=default_key.cancel_key)
    await state.update_data(ch_country=ch_country)
    await Anketa.ch_city.set()
    # print('birth_country')


@dp.message_handler(state=Anketa.ch_city)
async def bot_echo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ch_city = data.get("ch_city")
        ch_lname = list(data.get("ch_lname"))
        ch_fname = list(data.get("ch_fname"))
    ch_city.append(message.text)
    # print('state: country')
    await message.answer(f"""{ch_fname[-1]} {ch_lname[-1]}ning surati:\nAsosiy narsalarni yodda tuting: o'lcham, ifoda, boshning holati, fon va yuzni yashirishi mumkin bo'lgan barcha narsalar (sochlar, soyalar, ko'zoynak, ortiqcha yorug'lik va hk). Ko'pgina misollarda foydali "Foto maslahatlar" berilgan:""")
    await message.answer_photo('https://travel.state.gov/content/dam/passports/photo_examples/_MG_3425_GOOD.png/jcr:content/renditions/original', 
                               caption='✅ <b>Qoniqarli surat</b>\nQabul qilinadi— Surat tiniq va rangli, terining ohangini aniq aks ettiradi va soyalarsiz toʻgʻri koʻrsatiladi.')

    await message.answer_photo('https://travel.state.gov/content/dam/passports/photo_examples/Try%20underexposed%20(3).png/jcr:content/renditions/original', 
                               caption="❌ <b>Qoniqarsiz surat</b>\nQabul qilib bo'lmaydigan — Surat kam qo'yilgan"
                               "\nFotosurat bo'yicha maslahat: Surat haddan tashqari ko'p yoki kam bo'lmasligi kerak. Siz kameraning ekspozitsiyasini sozlashingiz yoki qo'shimcha yorug'likdan foydalanishingiz kerak. ")

    await message.answer_photo('https://travel.state.gov/content/dam/passports/photo_examples/_MG_3429_blue.png/jcr:content/renditions/original', 
                               caption="❌ <b>Qoniqarsiz surat</b>\nQabul qilib bo'lmaydigan — rang aniq emas\n"
                               "Fotosurat boʻyicha maslahat: Yorugʻlikka qarab kamerangizning oq balansi sozlamasini oʻzgartirishingiz kerak boʻlishi mumkin.")

    await message.answer_photo('https://travel.state.gov/content/dam/passports/photo_examples/CROPPED-DSC_0067.jpg/jcr:content/renditions/original', 
                               caption="❌ <b>Qoniqarsiz surat</b>\nQabul qilib bo'lmaydigan — yuz va fonda soyalar mavjud\n"
                               "Fotosurat uchun maslahat: yuz va fonda soyalar paydo bo'lishining oldini olish uchun siz bir xil (Kamera bilan bir tomondan qragan) yoritishni ishlatishingiz kerak.")

    await message.answer('Sifatli (600px x 600px yoki 51mm x 51mm) rasmingizni kiriting:',reply=default_key.cancel_key)
    await state.update_data(ch_city=ch_city)
    await Anketa.ch_photo.set()
    # print('photo')


@dp.message_handler(state=Anketa.ch_photo, content_types='photo')
async def bot_echo(message: types.Message, state: FSMContext):
    # print('state: photo')
    async with state.proxy() as data:
        session_num = data.get("session_num")
        child_count = data.get("child_count")
        ch_photo = data.get("ch_photo")
    photo = message.photo[-1].file_id
    ch_photo.append(photo)
    # print('session_num',session_num, 'child_count',child_count )
    if session_num == child_count:
        photo = message.photo[-1].file_id
        await message.answer("Korib chiqishga topshirildi")
        id = await id_gen()
        await state.update_data(id=id)
        price = 8000
        async with state.proxy() as data:
            phone_num = data.get("phone_num")
            fname = data.get("fname")
            lname = data.get("lname")
            gender = data.get("gender")
            birth_year = data.get("birth_year")
            birth_month = data.get("birth_month")
            birth_day = data.get("birth_day")
            birth_city = data.get("birth_city")
            birth_country = data.get("birth_country")
            edu_grade = data.get("edu_grade")
            marriage_state = data.get("marriage_state")
            photo = data.get("photo")

            ch_fname = data.get('ch_fname')
            ch_lname = data.get('ch_lname')
            ch_gender = data.get('ch_gender')
            ch_birth_year = data.get('ch_birth_year')
            ch_birth_month = data.get('ch_birth_month')
            ch_birth_day = data.get('ch_birth_day')
            ch_city = data.get('ch_city')
            ch_country = data.get('ch_country')
            # ch_photo = data.get("ch_photo")
            # tepada photo chaqirilgan va yangi photo qo'shilgan
        # print(data.as_dict())
        text = f"ID: {id}\ntel: {phone_num};\nAkketa: Oilaviy;\nIsm: {fname};\nFamilya: {lname};\nJinsi: {gender};\nTug'ilgan sanasi: {birth_year}-yil {birth_day}-{birth_month};\nTug'ilgan joyi: {birth_country}>{birth_city};\nTalim darajasi: {edu_grade};\nOilaviy holati: {marriage_state}"
        messages = [{'photo': photo, 'text': text}]
        await message.answer_photo(photo=photo, caption=text)
        # await bot.send_photo(chat_id=-1001896668985, photo=photo, caption=text)
        for i in range(1,len(ch_fname)):
            price+=4000
            text = f"""
ID: {id};
Qarindoshligi: {"turmush o'rtog'i" if marriage_state == "Turmush qurgan" and i==1 else "farzandi"};
Ism: {ch_fname[i]};
Familya: {ch_lname[i]};
Jinsi: {ch_gender[i]};
Tug'ilgan sana: {ch_birth_year[i]}-yil {ch_birth_day[i]}-{ch_birth_month[i]};
Tug'ilgan joy: {ch_country[i]}>{ch_city[i]};
"""
            await message.answer_photo(photo=ch_photo[i],caption=text)
            # await bot.send_photo(chat_id=-1001896668985, photo=ch_photo[i],caption=text)
            messages.append({'photo': ch_photo[i], 'text': text})
            await state.update_data(price=price)
        await state.update_data(messages=messages)
        # print(messages)
        await message.answer(f"<b>Raxma</b>\nAnketa to'ldirish nixoyasiga yetdi \n!!!Iltimos malumotlaringizni tekshiring!!! \n"
                             "\nUmirzaqov Isomiddin Salohiddin Ugli:\nSberbank:\n<code>2202 2025 6604 2721</code>\n\nUzcard:<code>8600 1404 0792 0868</code>\n\n"
                             f"<b>{price} so'm yoki {price*0.017} rubl to'langanligi to'lov qog'ozini(chekni) yuboring</b>"
                             " keyin uni hodimlar ko'rib chiqib, agarda xatolik mavjud bo'lsa sizga bog'lanishadi")
        await Anketa.bill.set()
    else:
        session_num+=1
        await state.update_data(session_num=session_num)
        await state.update_data(ch_photo=ch_photo)
        await Anketa.ch_fname.set()
        await message.answer(f"{session_num}-farzandingiz ismi:\n",reply=default_key.cancel_key)

@dp.message_handler(state=Anketa.ch_photo)
async def bot_echo(message: types.Message, state: FSMContext):
    await message.answer("Rasim fayl kiritishingiz kerak")


@dp.message_handler(state=Anketa.bill, content_types='photo')
async def bot_echo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        messages = data.get('messages')
        price = data.get('price')
        id = data.get('id')
    # print('messages 511',messages)
    for el in messages:
        await bot.send_photo(chat_id=-1001896668985, photo=el['photo'], caption=el['text'])
    await bot.send_photo(chat_id=-1001896668985, photo=message.photo[-1].file_id ,caption=f"ID: {id} uchun to'lov cheki: summa: {price}so'm yoki {price*0.017} rubl")
    await state.finish()
    await message.answer("Anketa to'ldirish tugatildi. Bizning hizmatimizdan foydalanganingiz uchun raxmat", default_key.remove_key)
    
    # await message.answer_photo(photo=photo, caption=f"anketa kodi: #{id} {phone_num}, {fname}, {lname}, {birth_year}, {birth_month}, {birth_day}, {birth_city}, {birth_country}")


@dp.message_handler(state=Anketa.bill)
async def bot_echo(message: types.Message, state: FSMContext):
    await message.answer("Chek rasm formatida bo'lishi kerak:")


@dp.message_handler()
async def bot_echo(message: types.Message):
    await message.answer("/shartlar bilan tanishib chiqing va keyin /anketa to'ldiring")

