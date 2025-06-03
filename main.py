import os
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Admins
ADMINS = [1299831974, 6848373878]

# Fichier des données
DATA_FILE = "data.json"

# Obtenir le token depuis Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Fonctions de gestion des données
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def is_admin(user_id):
    return user_id in ADMINS

def admin_only(func):
    def wrapper(update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        if not is_admin(user_id):
            update.message.reply_text("⛔ Tu n'es pas autorisé à utiliser cette commande.")
            return
        return func(update, context)
    return wrapper

# Commandes de base
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    data = load_data()
    uid = str(user.id)

    if is_admin(user.id):
        update.message.reply_text("""
Deku Prédiction:
👋 Bienvenue administrateur !

Vous avez un accès permanent à toutes les fonctionnalités.
Tapez /help pour voir toutes les commandes disponibles.
""")
        return

    if uid in data and data[uid].get("authorized"):
        update.message.reply_text("✅ Bienvenue de retour ! Utilise /predictions pour commencer.")
    else:
        update.message.reply_text("""
Vous n'êtes pas enregistré. Veuillez entrer votre code d'accès avec la commande :
/code VOTRECODE

Veuillez contacter l'administrateur pour obtenir un code d'accès :
Telegram : @Drissa310 ou @deku225
""")

def help_command(update: Update, context: CallbackContext):
    if is_admin(update.effective_user.id):
        update.message.reply_text("""
🔑 Accès au bot :
Pour utiliser ce bot, tu dois activer ton accès avec un code fourni par l'administrateur.

1️⃣ Demande un code à l'administrateur.
2️⃣ Tape la commande : /code VOTRECODE
3️⃣ Si le code est valide, tu pourras accéder à toutes les fonctionnalités.
4️⃣ Si tu rencontres un problème, contactes l'administrateur.

Menu d'aide Administrateur :

📱 Commandes de base :
/start - Démarrer le bot
/help - Afficher l'aide
/myid - Afficher mon identifiant Telegram

🎯 Prédictions :
/predictions - pour prédire

📊 Statistiques et recherche :
/history - Voir tout l'historique
/search motclé - Rechercher par ligue ou équipe
/stats - Statistiques des prédictions

👥 Gestion des utilisateurs (admin) :
/add_user ID nombre - Ajouter un utilisateur avec un nombre de prédictions
/deactivate id - Désactiver un utilisateur
/reactivate id - Réactiver un utilisateur
/list_users - Voir les utilisateurs actifs
""")
    else:
        update.message.reply_text("Utilise /code VOTRECODE pour activer l'accès si tu en as un.")

def myid(update: Update, context: CallbackContext):
    update.message.reply_text(f"🆔 Ton ID Telegram : {update.effective_user.id}")

# Ajout utilisateur
def code(update: Update, context: CallbackContext):
    update.message.reply_text("🔐 Fonction de code d'accès non encore implémentée.")

@admin_only
def add_user(update: Update, context: CallbackContext):
    if len(context.args) != 2:
        update.message.reply_text("Utilisation : /add_user ID nombre")
        return

    user_id = context.args[0]
    try:
        predictions = int(context.args[1])
    except ValueError:
        update.message.reply_text("Le nombre doit être un entier.")
        return

    data = load_data()
    if user_id not in data:
        data[user_id] = {
            "name": "Inconnu",
            "authorized": True,
            "predictions_left": predictions,
            "history": []
        }
    else:
        data[user_id]["authorized"] = True
        data[user_id]["predictions_left"] = predictions

    save_data(data)
    update.message.reply_text(f"✅ L'utilisateur {user_id} a été autorisé avec {predictions} prédictions.")

# Prédiction

def predictions(update: Update, context: CallbackContext):
    uid = str(update.effective_user.id)
    data = load_data()

    if uid not in data or not data[uid].get("authorized"):
        update.message.reply_text("⛔ Tu n'es pas autorisé. Entre un code avec /code.")
        return

    if data[uid].get("predictions_left", 0) <= 0:
        update.message.reply_text("🚫 Tu as atteint la limite de prédictions. Contacte l'administrateur.")
        return

    # Simuler une prédiction
    fake_result = {
        "team1": "Marseille",
        "team2": "PSG",
        "score": "2-1",
        "fiability": "Haute",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data[uid]["predictions_left"] -= 1
    data[uid].setdefault("history", []).append(fake_result)
    save_data(data)

    update.message.reply_text(
        f"🎯 Prédiction : {fake_result['team1']} vs {fake_result['team2']}\n"
        f"Score prédit : {fake_result['score']}\n"
        f"Fiabilité : {fake_result['fiability']}\n"
        f"Il te reste {data[uid]['predictions_left']} prédictions."
    )

# Historique
def history(update: Update, context: CallbackContext):
    uid = str(update.effective_user.id)
    data = load_data()

    if uid not in data or not data[uid].get("authorized"):
        update.message.reply_text("⛔ Tu n'es pas autorisé.")
        return

    history = data[uid].get("history", [])
    if not history:
        update.message.reply_text("📭 Aucun historique de prédiction.")
        return

    msg = "🕘 Historique de prédictions :\n\n"
    for h in history[-10:]:
        msg += f"{h['timestamp']} - {h['team1']} vs {h['team2']} → {h['score']} ({h['fiability']})\n"
    update.message.reply_text(msg)

# Config du bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("myid", myid))
    dispatcher.add_handler(CommandHandler("code", code))
    dispatcher.add_handler(CommandHandler("add_user", add_user))
    dispatcher.add_handler(CommandHandler("predictions", predictions))
    dispatcher.add_handler(CommandHandler("history", history))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
