from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from handlers.decrypt import decrypt  # ✅ Corrigé ici

from loader import dp

# Enregistrement du handler
dp.register_message_handler(decrypt, content_types=types.ContentType.DOCUMENT)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
