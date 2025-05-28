from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from handlers.decrypt import handle_document
from loader import dp, bot

# Enregistrement du handler
dp.register_message_handler(handle_document, content_types=types.ContentType.DOCUMENT)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
