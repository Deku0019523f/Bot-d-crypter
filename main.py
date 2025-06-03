import json
import random
import string
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

ADMINS = [1299831974, 6848373878]

# Chargement ou initialisation
def load_data(file, default):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except:
        return default

users = load_data("users.json", {})
pending_codes = load_data("secrets.json", {})

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

def save_codes():
    with open("secrets.json", "w") as f:
        json.dump(pending_codes, f, indent=2)

def is_admin(user_id):
    return user_id in ADMINS

def generate_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

# 🔐 /add_user <user_id>
async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage : /add_user <user_id>")
        return

    user_id = context.args[0]
    code = generate_code()
    pending_codes[code] = user_id
    save_codes()

    msg = (
        f"Code généré pour {user_id} :\n\n"
        f"🔑 {code}\n\n"
        f"Transmets ce code à l'utilisateur. Il devra taper :\n"
        f"/code {code}"
    )
    await update.message.reply_text(msg)

# 🚀 /code <clé>
async def activate_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username = update.effective_user.full_name

    if len(context.args) != 1:
        await update.message.reply_text("Utilisation : /code <clé>")
        return

    code = context.args[0]

    if code not in pending_codes or str(pending_codes[code]) != user_id:
        await update.message.reply_text("❌ Code invalide ou non associé à ton ID.")
        return

    users[user_id] = {
        "id": user_id,
        "name": username,
        "code": code,
        "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_users()
    del pending_codes[code]
    save_codes()

    msg = (
        f"🔔 Nouvelle activation de code !\n\n"
        f"👤 Utilisateur :\n"
        f"ID : {user_id}\n"
        f"Nom : {username}\n"
        f"Code utilisé : {code}\n\n"
        f"⏰ Date : {users[user_id]['activated_at']}\n\n"
        f"Pour gérer cet utilisateur :\n"
        f"• Désactiver : /deactivate {user_id}\n"
        f"• Voir les détails : /list_users"
    )
    for admin_id in ADMINS:
        await context.bot.send_message(chat_id=admin_id, text=msg)

    await update.message.reply_text("✅ Accès activé avec succès !")

# ✅ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in users:
        await update.message.reply_text("⛔ Tu n'es pas autorisé à utiliser ce bot. Demande un code d'accès à un admin.")
        return
    await update.message.reply_text("Bienvenue ! Tu as accès au bot.")

# ❌ /deactivate <user_id>
async def deactivate_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage : /deactivate <user_id>")
        return

    user_id = context.args[0]
    if user_id in users:
        del users[user_id]
        save_users()
        await update.message.reply_text(f"Utilisateur {user_id} désactivé.")
    else:
        await update.message.reply_text("Utilisateur introuvable.")

# 📋 /list_users
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if not users:
        await update.message.reply_text("Aucun utilisateur activé.")
        return

    text = "👥 Utilisateurs activés :\n\n"
    for u in users.values():
        text += f"• {u['name']} ({u['id']}) – {u['code']} – {u['activated_at']}\n"
    await update.message.reply_text(text)

# 🚀 Lancer le bot
if __name__ == "__main__":
    import os
    from telegram.ext import CommandHandler

    TOKEN = os.getenv("BOT_TOKEN")  # À remplacer par ton token si tu ne veux pas utiliser dotenv
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_user", add_user))
    app.add_handler(CommandHandler("code", activate_code))
    app.add_handler(CommandHandler("deactivate", deactivate_user))
    app.add_handler(CommandHandler("list_users", list_users))

    app.run_polling()
