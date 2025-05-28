
from aiogram import types
from aiogram.types import Message
from loader import dp
import os

def format_decrypt_response(filename: str, decrypted_content: str) -> str:
    return (
        "🔐 <b>Deku Team</b> 🔐\n"
        "┌───────────────\n"
        f"├ • <b>{filename}</b>\n"
        "├ • Channel : <a href='https://t.me/connexiontoutreseaus'>@connexiontoutreseaus</a>\n"
        "├ • Thanks To : <b>BOOS_TOOLS</b>\n"
        "├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •\n"
        "├ • 💠 <b>Décrypté avec succès !</b>\n"
        "├ • 💠 <b>Contenu :</b>\n"
        f"<pre>{decrypted_content}</pre>\n"
        "├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •\n"
        "├ • bot: <a href='https://t.me/deku_filesbot'>@deku_filesbot</a>\n"
        "├ • Channel : <a href='https://t.me/connexiontoutreseaus'>t.me/connexiontoutreseaus</a>"
    )

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_decrypt_file(message: Message):
    document = message.document
    file_path = await document.download(destination_dir="temp_files")
    filename = document.file_name

    try:
        with open(file_path.name, "r", encoding="utf-8") as f:
            decrypted_content = f.read()

        if len(decrypted_content) > 4000:
            decrypted_content = decrypted_content[:4000] + "\n... (tronqué)"

        response_text = format_decrypt_response(filename, decrypted_content)

        await message.reply(response_text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        await message.reply(f"❌ Erreur lors du décryptage : {e}")
