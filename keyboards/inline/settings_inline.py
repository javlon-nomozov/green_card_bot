from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def settings_keyboard(lang: str = 'en'):
    if lang.lower() == 'en':
        text = 'English'
        lan = 'ru'
    elif lang.lower() == 'ru':
        text = 'Russian'
        lan = 'uz'
    elif lang.lower() == 'uz':
        text = 'Uzbek'
        lan = 'en'
    else:
        text = 'Uzbek'
        lan = 'en'
    key = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=f"🔁  {text}  🔁", callback_data=f'lang:{lan}')
        ]]
    )
    return key

