from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("/anketa", "Yangi anketa to'ldirish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("setting", "Sozlamalar"),
            types.BotCommand("cancel", "Bekor qilish"),
            # types.BotCommand("donate", "Qo'llab quvvatlovchilar uchun"),
        ]
    )
