from aiogram import Bot, Dispatcher, types, executor
from handlers import decrypt
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dp.register_message_handler(decrypt, content_types=types.ContentType.DOCUMENT)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
