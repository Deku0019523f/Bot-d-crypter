from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from handlers import decrypt  # ⬅️ ça importe ton handler automatiquement

import logging
import os

API_TOKEN = os.getenv("BOT_TOKEN")  # 🔐 Met ton token ici ou en variable d'env

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Tu peux aussi ajouter une commande de test
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("👋 Bienvenue ! Envoie un fichier VPN pour le décrypter.")

# Ici, on appelle ton handler
# Pas besoin de faire autre chose si tu l'importes comme ci-dessus.
# Les handlers déclarés dans decrypt.py seront enregistrés grâce à l'import.

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
