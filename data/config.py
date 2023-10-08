from utils.db_api.sqlite import Database

db = Database(path_to_db="data/main.db")

# environs kutubxonasidan foydalanish


# # .env fayl ichidan quyidagilarni o'qiymiz
# BOT_TOKEN = env.str("BOT_TOKEN")  # Bot tokeni
# ADMINS = env.list("ADMINS")  # adminlar ro'yxati
# CHATS = db.select_must_sub_chat()
# # CHATS =
# # CHANNELS = env.list("CHANNELS")  # MAJBURIY OBUNA KANALLATRI
# GROUPS = env.list("GROUPS")  # GURUXLRGA XATOLARNI UZATISH YOKI BOSHQA MAQSADLAR UCN
# IP = env.str("ip")  # Xosting ip manzili
DEBUG = True
BOT_TOKEN = '1852243581:AAFqigo3CIpLPiSjNSNVZ7NqA48e-xCmq80'
ADMINS = [1559808421]
CHATS = []
# CHATS = db.select_must_sub_chat()
GROUPS = ['@gdfnjduy']  # GURUXLRGA XATOLARNI UZATISH YOKI BOSHQA MAQSADLAR UCHUN
IP = 'localhost'  # Xosting ip manzili
