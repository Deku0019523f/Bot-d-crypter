import os
from telegram import Update, Document
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

WELCOME_MESSAGE = """
🎉 Welcome to @Deku225! 🎉
━━━━━━━━━━━━━━━━━━━━━━━  
👤 Your User ID: {user_id}
━━━━━━━━━━━━━━━━━━━━━━━  
🤖 About this Bot:
This bot is designed to decrypt and process various VPN configuration files.
━━━━━━━━━━━━━━━━━━━━━━━
Click the button below to view supported files and protocols.
📅 Last Update: 4 December 2025
"""

SUPPORTED_FORMATS = [
    ".HAT", ".VPNLITE", ".SKSPLUS", ".EHIL", ".SBR", ".TVT", ".MINA", ".AIP", ".JVC",
    ".KT", ".XSCKS", ".ARO", ".EUG", ".IPT", ".ZIV", ".TNL", ".PCX", ".PB", ".PHC",
    ".FNNETWORK", ".JVI", ".MIJ", ".MRC", ".UWU", ".SKSRV.PNG", ".HBD", ".REZ", ".ROY",
    ".SUT", ".NM", ".DVD", ".REZL", ".STK", ".SKS", ".SSH", ".AGN", ".OST", ".FN",
    ".BN", ".V2I", ".CLY", ".ACM", ".EPRO", ".NXP", ".MAYA"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(WELCOME_MESSAGE.format(user_id=user_id))

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document: Document = update.message.document
    file_name = document.file_name
    extension = os.path.splitext(file_name)[-1].upper()

    if extension not in SUPPORTED_FORMATS:
        await update.message.reply_text(f"❌ Format non supporté : {extension}")
        return

    file = await document.get_file()
    file_path = f"/tmp/{file_name}"
    await file.download_to_drive(file_path)

    # Simuler la "décryption" (remplacer par ton vrai code ici)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    response = f"""
🔐 Deku Team 🔐
┌───────────────
├ • {file_name}
├ •Channel : https://t.me/connexiontoutreseaus
├ •Thanks To :BOOS_TOOLS
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • 💠 Décrypté avec succès !
├ • 💠 Contenu :\n{content[:1500]}...
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • bot:@deku_filesbot
├ • Channel : t.me/connexiontoutreseaus
"""
    await update.message.reply_text(response)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("Bot running...")
    app.run_polling()

if __name__ == '__main__':
    main()