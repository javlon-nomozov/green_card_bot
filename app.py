from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Ma'lumotlar bazasini yaratamiz:
    try:
        db.create_table_users()
    except Exception as err:
        print(err)

    try:
        db.create_table_chat()
    except Exception as err:
        print(err)

    # Bot ishga tushgani haqida adminga xabar berish
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dispatcher)

    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)