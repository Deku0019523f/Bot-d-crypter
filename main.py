
import json
import os
from datetime import datetime, timedelta
import secrets

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [1299831974, 6848373878]

USERS_FILE = "users.json"
CODES_FILE = "codes.json"

def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def is_admin(user_id):
    return user_id in ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username = update.effective_user.full_name
    users = load_json(USERS_FILE)

    if is_admin(update.effective_user.id):
        await update.message.reply_text(
            "👋 Bienvenue administrateur !\n\n"
            "Vous avez un accès permanent à toutes les fonctionnalités.\n"
            "Tapez /help pour voir toutes les commandes disponibles."
        )
        return

    if user_id in users and users[user_id]["active"]:
        await update.message.reply_text(f"✅ Bienvenue {username} ! Tapez /help pour voir les commandes.")
    else:
        await update.message.reply_text(
            "⛔ Vous n'êtes pas enregistré. Veuillez entrer votre code d'accès avec la commande /code VOTRECODE\n\n"
            "Veuillez contacter l'administrateur pour obtenir un code d'accès :\n"
            "Telegram : @Drissa310 ou @deku225"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update.effective_user.id):
        await update.message.reply_text(
            "🔑 Accès au bot :\n"
            "Pour utiliser ce bot, tu dois activer ton accès avec un code fourni par l’administrateur.\n"
            "1️⃣ Demande un code à l’administrateur.\n"
            "2️⃣ Tape la commande : /code VOTRECODE\n"
            "3️⃣ Si le code est valide, tu pourras accéder à toutes les fonctionnalités.\n"
            "4️⃣ Si tu rencontres un problème, contactes l’administrateur.\n\n"
            "Menu d’aide Administrateur :\n\n"
            "📱 Commandes de base :\n"
            "/start - Démarrer le bot\n"
            "/help - Afficher l’aide\n"
            "/myid - Afficher mon identifiant Telegram\n\n"
            "🎯 Prédictions :\n"
            "/predictions - pour prédis\n\n"
            "📊 Statistiques et recherche :\n"
            "/history - Voir tout l’historique\n"
            "/search motclé - Rechercher par ligue ou équipe\n"
            "/stats - Statistiques des prédictions\n\n"
            "👥 Gestion des utilisateurs (admin) :\n"
            "/gen_code id [jours] [max] - Générer un code d’accès\n"
            "/deactivate id - Désactiver un utilisateur\n"
            "/reactivate id - Réactiver un utilisateur\n"
            "/set_limit id [jours] [max] - Limiter un utilisateur\n"
            "/list_users - Voir les utilisateurs actifs\n"
            "/delete_code code - Supprimer un code d’accès"
        )
    else:
        await update.message.reply_text("Tape /start pour commencer ou /code pour entrer ton code.")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Ton ID Telegram : {update.effective_user.id}")

async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("❌ Utilisation : /code VOTRECODE")
        return

    code_input = args[0]
    user_id = str(update.effective_user.id)
    username = update.effective_user.full_name

    codes = load_json(CODES_FILE)
    users = load_json(USERS_FILE)

    if code_input not in codes:
        await update.message.reply_text("❌ Code invalide.")
        return

    info = codes[code_input]
    if info["max"] is not None and info["used"] >= info["max"]:
        await update.message.reply_text("⚠️ Ce code a déjà été utilisé trop de fois.")
        return

    expiration_date = None
    if info["days"] is not None:
        expiration_date = (datetime.now() + timedelta(days=info["days"])).isoformat()

    users[user_id] = {
        "username": username,
        "active": True,
        "code_used": code_input,
        "activated_at": datetime.now().isoformat(),
        "expires_at": expiration_date
    }

    codes[code_input]["used"] += 1
    save_json(USERS_FILE, users)
    save_json(CODES_FILE, codes)

    await update.message.reply_text("✅ Accès activé avec succès ! Vous pouvez maintenant utiliser le bot.")

async def gen_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Utilisation : /gen_code id [jours] [max]")
        return

    target_id = args[0]
    days = int(args[1]) if len(args) > 1 else None
    max_uses = int(args[2]) if len(args) > 2 else 1

    code = secrets.token_hex(4)
    codes = load_json(CODES_FILE)

    codes[code] = {
        "user_id": target_id,
        "days": days,
        "max": max_uses,
        "used": 0
    }

    save_json(CODES_FILE, codes)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(
        f"Code généré pour {target_id} :\n\n"
        f"🔑 {code}\n\n"
        f"Transmets ce code à l'utilisateur. Il devra taper :\n"
        f"/code {code}\n\n"
        f"🔔 Nouvelle activation de code !\n\n"
        f"👤 Utilisateur :\nID : {target_id}\nNom : {update.effective_user.full_name}\n"
        f"Code utilisé : {code}\n⏰ Date : {now}\n\n"
        f"Pour gérer cet utilisateur :\n• Désactiver : /deactivate {target_id}\n"
        f"• Voir les détails : /list_users"
    )

async def deactivate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    user_id = context.args[0]
    users = load_json(USERS_FILE)
    if user_id in users:
        users[user_id]["active"] = False
        save_json(USERS_FILE, users)
        await update.message.reply_text("✅ Utilisateur désactivé.")
    else:
        await update.message.reply_text("Utilisateur introuvable.")

async def reactivate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    user_id = context.args[0]
    users = load_json(USERS_FILE)
    if user_id in users:
        users[user_id]["active"] = True
        save_json(USERS_FILE, users)
        await update.message.reply_text("✅ Utilisateur réactivé.")
    else:
        await update.message.reply_text("Utilisateur introuvable.")

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    users = load_json(USERS_FILE)
    msg = "👥 Utilisateurs actifs :\n\n"
    for uid, data in users.items():
        status = "✅" if data.get("active", False) else "⛔"
        msg += f"{status} {uid} - {data.get('username', '')}\n"
    await update.message.reply_text(msg)

async def delete_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    code = context.args[0]
    codes = load_json(CODES_FILE)
    if code in codes:
        del codes[code]
        save_json(CODES_FILE, codes)
        await update.message.reply_text("✅ Code supprimé.")
    else:
        await update.message.reply_text("❌ Code introuvable.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("code", code))
    app.add_handler(CommandHandler("gen_code", gen_code))
    app.add_handler(CommandHandler("deactivate", deactivate))
    app.add_handler(CommandHandler("reactivate", reactivate))
    app.add_handler(CommandHandler("list_users", list_users))
    app.add_handler(CommandHandler("delete_code", delete_code))

    print("Bot lancé...")
    app.run_polling()

if __name__ == "__main__":
    main()
