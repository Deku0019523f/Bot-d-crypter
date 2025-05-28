import os
import base64
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔐 Bienvenue sur Deku Team 🔐\nEnvoyez un fichier VPN (.hat, .vpnlite, .sksplus) pour le décrypter.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file_name = document.file_name
    ext = file_name.split('.')[-1].lower()
    file = await document.get_file()
    file_path = f"/tmp/{file_name}"
    await file.download_to_drive(file_path)

    decrypted = decrypt_file(file_path, ext)
    await update.message.reply_text(decrypted[:4000], parse_mode='HTML')  # Limite de Telegram

def decrypt_file(path, ext):
    try:
        with open(path, 'rb') as f:
            data = f.read()

        if ext in ["hat", "vpnlite", "sksplus"]:
            decoded = base64.b64decode(data).decode('utf-8', errors='ignore')
            return format_output(decoded, ext)
        else:
            return f"❌ Extension .{ext} non supportée."
    except Exception as e:
        return f"⚠️ Erreur lors du traitement : {e}"

def format_output(decoded_text, ext):
    lines = decoded_text.splitlines()
    payload = next((line for line in lines if "CONNECT" in line), "N/A")
    host = next((line for line in lines if "Host:" in line), "N/A")
    sni = next((line for line in lines if "SNI" in line), "N/A")
    ip = next((line for line in lines if "172." in line or "204." in line), "N/A")
    port = "80"
    pays = "Game | EU 🎮"
    expiration = next((line for line in lines if "Expire le" in line), "N/A")

    return f"""🔐 <b>Deku Team</b> 🔐
┌───────────────
├ • <b>ha Tunnel</b> (.{ext})
├ •Channel : <a href="t.me/connexiontoutreseaus">t.me/connexiontoutreseaus</a>
├ •Thanks To : BOOS_TOOLS
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • 💠  <b>Connection Method:</b> 1
├ • 💠  <b>Payload:</b> {payload}
├ • 💠  <b>Custom Host:</b> {host}
├ • 💠  <b>SSL/SNI:</b> {sni}
├ • 💠  <b>Primary host address:</b> {ip}
├ • 💠  <b>Server Port:</b> {port}
├ • 💠  <b>Server Node/Country:</b> {pays}
├ • 💠  <b>Expiration:</b> {expiration}
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • bot: @deku_filesbot
├ • Channel : t.me/connexiontoutreseaus
"""
    
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    print("🤖 Bot démarré...")
    app.run_polling()