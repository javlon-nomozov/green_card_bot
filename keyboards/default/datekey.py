from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

months = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yanvar"),
            KeyboardButton(text="Fevral")
        ],
        [
            KeyboardButton(text="Mart"),
            KeyboardButton(text="Aprel"),
        ],
        [
            KeyboardButton(text="May"),
            KeyboardButton(text="Iyun"),
        ],
        [
            KeyboardButton(text="Iyul"),
            KeyboardButton(text="Avgust"),
        ],
        [
            KeyboardButton(text="Sentyabr"),
            KeyboardButton(text="Oktyabr"),
        ],
        [
            KeyboardButton(text="Noyabr"),
            KeyboardButton(text="Dekabr"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
