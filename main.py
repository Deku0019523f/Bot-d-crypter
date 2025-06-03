import os
import json
import random
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

ADMIN_IDS = [1299831974, 6848373878]
DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"users": {}, "history": []}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    if user_id in data["users"] and data["users"][user_id]["active"]:
        if int(user_id) in ADMIN_IDS:
            await update.message.reply_text(
                "👋 Bienvenue administrateur !\n\n"
                "Vous avez un accès permanent à toutes les fonctionnalités.\n"
                "Tapez /help pour voir toutes les commandes disponibles."
            )
        else:
            await update.message.reply_text("✅ Vous êtes déjà activé.")
    else:
        await update.message.reply_text(
            "⛔ Vous n'êtes pas enregistré.\n"
            "Veuillez entrer votre code d'accès avec la commande :\n"
            "`/code VOTRECODE`\n\n"
            "Contactez l'admin : @Drissa310 ou @deku225",
            parse_mode="Markdown"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if int(user_id) in ADMIN_IDS:
        await update.message.reply_text(
            "📱 Commandes de base :\n"
            "/start - Démarrer le bot\n"
            "/help - Afficher l'aide\n"
            "/myid - Obtenir mon ID Telegram\n\n"
            "🎯 Prédiction :\n"
            "/predictions\n"
            "📊 Historique :\n"
            "/history\n\n"
            "👥 Gestion utilisateurs :\n"
            "/add_user ID NOMBRE_TOTAL\n"
        )
    else:
        await update.message.reply_text(
            "🔑 Accès au bot :\n"
            "1️⃣ Demande un code à l’admin\n"
            "2️⃣ Tape : /code VOTRECODE\n"
            "3️⃣ Si valide, tu auras accès.\n"
            "Contact : @Drissa310 ou @deku225"
        )

async def predictions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    user = data["users"].get(user_id)

    if not user or not user["active"]:
        await update.message.reply_text("⛔ Tu n'es pas autorisé à utiliser cette commande.")
        return

    if user["used"] >= user["limit"]:
        await update.message.reply_text("📉 Tu as atteint la limite de prédictions autorisées.")
        return

    team1 = random.choice(["PSG", "Barça", "Man City"])
    team2 = random.choice(["Real Madrid", "Liverpool", "Juventus"])
    score = f"{random.randint(0,3)} - {random.randint(0,3)}"
    fiability = random.choice(["🔴 Faible", "🟡 Moyenne", "🟢 Élevée"])

    response = (
        f"📊 Résultat simulé :\n"
        f"{team1} vs {team2}\n"
        f"Score prédit : {score}\n"
        f"Fiabilité : {fiability}"
    )
    await update.message.reply_text(response)

    # Enregistrer
    user["used"] += 1
    data["history"].append({
        "user_id": user_id,
        "teams": f"{team1} vs {team2}",
        "score": score,
        "fiability": fiability,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_data(data)

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if int(user_id) not in ADMIN_IDS:
        await update.message.reply_text("⛔ Tu n'es pas admin.")
        return

    try:
        target_id = context.args[0]
        limit = int(context.args[1])
        data = load_data()
        data["users"][target_id] = {
            "active": True,
            "limit": limit,
            "used": 0
        }
        save_data(data)
        await update.message.reply_text(f"✅ Utilisateur {target_id} activé avec {limit} prédictions.")
    except:
        await update.message.reply_text("❌ Utilisation : /add_user ID NOMBRE_TOTAL")

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    if not data["history"]:
        await update.message.reply_text("Aucune prédiction encore enregistrée.")
        return

    latest = data["history"][-5:]
    msg = "🕘 Dernières prédictions :\n\n"
    for h in latest:
        msg += f"{h['date']} - {h['teams']} => {h['score']} ({h['fiability']})\n"
    await update.message.reply_text(msg)

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Ton ID : {update.effective_user.id}")

if __name__ == "__main__":
    import asyncio
    import logging

    logging.basicConfig(level=logging.INFO)
    TOKEN = os.getenv("BOT_TOKEN")  # Railway gère ce token

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("add_user", add_user))
    app.add_handler(CommandHandler("predictions", predictions))
    app.add_handler(CommandHandler("history", history))

    print("🤖 Bot démarré.")
    asyncio.run(app.run_polling())
