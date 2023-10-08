from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


remove_key = ReplyKeyboardRemove
cancel_btn = KeyboardButton(text='Bekor qilish')
edu_grade = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Maktab (9-10-sinf)")
        ],
        [
            KeyboardButton(text="Maktab(11-sinf)")
        ],
        [
            KeyboardButton(text="Litsey")
        ],
        [
            KeyboardButton(text="Kollej")
        ],
        [
            KeyboardButton(text="Tugalanmagan oliy")
        ],
        [
            KeyboardButton(text="Oliy malumot")
        ],
        [
            KeyboardButton(text="Magistratura")
        ],
        [
            KeyboardButton(text="Aspirantura")
        ],
        [
            KeyboardButton(text="Doktorantura")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
edu_grade.add(cancel_btn)

gender = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Erkak"),
            KeyboardButton(text="Ayol")
        ]    
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
gender.add(cancel_btn)
cancel_key = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
cancel_key.add(cancel_btn)

marriage_state = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Turmush qurmagan")
        ],
        [
            KeyboardButton(text="Turmush qurgan")
        ],
        [
            KeyboardButton(text="Ajrashgan/ajrashuvda")
        ],
        [
            KeyboardButton(text="Beva/yolg'iz")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
marriage_state.add(cancel_btn)