import os
import base64
import re
from aiogram import types
from loader import dp  # Assure-toi que 'loader.py' initialise bien 'dp' et 'bot'

# Ton lien de chaîne Telegram ici
FIXED_CHANNEL_LINK = "https://t.me/connexiontoutreseaus"  # 🔗 Remplace par ton lien

def extract_info(content: str, filename: str) -> str:
    # Remplacer l'extraction automatique par un lien personnalisé
    channel = FIXED_CHANNEL_LINK

    thanks_match = re.search(r"Thanks To\s*:(.+)", content)
    encoded_match = re.search(r"Contenu\s*:\s*([\s\S]+)", content)

    thanks = thanks_match.group(1).strip() if thanks_match else "Anonyme"
    encoded_text = encoded_match.group(1).strip() if encoded_match else None

    if encoded_text:
        try:
            decoded = base64.b64decode(encoded_text).decode("utf-8", errors="ignore")
        except Exception as e:
            decoded = f"Erreur de décryptage : {e}"
    else:
        decoded = "Aucun contenu encodé trouvé."

    return (
        f"🔐 <b>Deku Team</b>\n"
        f"├ 📁 <b>Fichier :</b> {filename}\n"
        f"├ 🔗 <b>Channel :</b> {channel}\n"
        f"├ 🙏 <b>Merci à :</b> {thanks}\n"
        f"├ 🧩 <b>Contenu décrypté :</b>\n"
        f"<code>{decoded[:4000]}</code>\n"
        f"\n🤖 <i>Décrypté par @deku_filesbot</i>"
    )

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message):
    document = message.document

    file_ext = os.path.splitext(document.file_name)[1].lower()
    allowed_exts = [".hat", ".vpnlite", ".vpnglobe", ".sksplus"]

    if file_ext not in allowed_exts:
        await message.reply("❌ Format de fichier non supporté.")
        return

    file = await document.download()
    with open(file.name, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    reply_text = extract_info(content, document.file_name)
    await message.reply(reply_text, parse_mode="HTML")
