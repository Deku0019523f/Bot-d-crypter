# 🔐 Deku VPN Decrypt Bot

Bot Telegram pour décrypter des fichiers VPN : `.HAT`, `.VPNLITE`, `.SKSPLUS`, etc.

## 🚀 Fonctionnalités
- Lecture des fichiers `.HAT`, `.VPNLITE`, etc.
- Réponse formatée avec contenu du fichier
- Déploiement facile sur Railway

## 📦 Installation locale

```bash
git clone https://github.com/tonpseudo/vpn-decrypt-bot.git
cd vpn-decrypt-bot
pip install -r requirements.txt
touch .env  # puis ajoute BOT_TOKEN=...
python bot.py
```

## 🚀 Déploiement Railway

1. Crée un dépôt GitHub avec ce code.
2. Va sur [Railway](https://railway.app)
3. Clique sur « New Project » → « Deploy from GitHub ».
4. Ajoute `BOT_TOKEN` dans l’onglet **Variables**.
5. Railway lancera automatiquement `python bot.py`.

## ✅ Formats supportés
```
.HAT, .VPNLITE, .SKSPLUS, .EHIL, .TVT, .AIP, .KT, ...
```