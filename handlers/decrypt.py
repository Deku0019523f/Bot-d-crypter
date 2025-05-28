import re
import base64
from aiogram import types
from loader import dp

WELCOME_MESSAGE = (
    "🔐 Deku Team 🔐\n"
    "┌───────────────\n"
    "├ • Channel : https://t.me/connexiontoutreseaus\n"
    "├ • Thanks To : Anonyme\n"
    "├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •\n"
)

def extract_info(content: str):
    """
    Extrait le contenu encodé base64 à partir du texte complet.
    """
    # Recherche souple du texte après "Contenu :"
    encoded_match = re.search(r"Contenu\s*:(.*)", content, re.DOTALL)
    if not encoded_match:
        return None
    
    encoded_text = encoded_match.group(1).strip()
    if not encoded_text:
        return None
    
    # Nettoyer pour garder uniquement base64 (optionnel)
    encoded_text = re.sub(r"[^A-Za-z0-9+/=]+", "", encoded_text)
    
    try:
        decoded_bytes = base64.b64decode(encoded_text)
        decoded_text = decoded_bytes.decode("utf-8", errors="ignore")
        return decoded_text if decoded_text else None
    except Exception:
        return None


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def decrypt(message: types.Message):
    file = await message.document.get_file()
    file_path = file.file_path

    downloaded_file = await message.bot.download_file(file_path)
    content = downloaded_file.read().decode("utf-8", errors="ignore")

    decrypted_content = extract_info(content)

    if decrypted_content:
        response = (
            f"{WELCOME_MESSAGE}"
            f"├ 📁 Fichier : {message.document.file_name}\n"
            f"├ 🧩 Contenu décrypté :\n{decrypted_content}\n"
            f"├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •\n"
            f"🤖 Décrypté par @{(await message.bot.get_me()).username}"
        )
    else:
        response = (
            f"{WELCOME_MESSAGE}"
            f"├ 📁 Fichier : {message.document.file_name}\n"
            f"├ 🧩 Contenu décrypté : Aucun contenu encodé trouvé.\n"
            f"🤖 Décrypté par @{(await message.bot.get_me()).username}"
        )

    await message.answer(response)
