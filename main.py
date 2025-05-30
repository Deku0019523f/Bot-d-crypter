
from fastapi import FastAPI
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from random import randint

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
BASE_URL = "https://api.football-data.org/v4"

LEAGUES = {
    "Ligue 1": "FL1",
    "Ligue 2": "FL2",
    "Serie A": "SA",
    "Premier League": "PL",
    "Championship": "ELC",
    "Bundesliga": "BL1",
    "Saudi Pro League": "SAU",
    "La Liga": "PD"
}

headers = {
    "X-Auth-Token": API_TOKEN
}

app = FastAPI()

def get_today_matches():
    today = datetime.now().strftime("%Y-%m-%d")
    matches = []
    for name, code in LEAGUES.items():
        url = f"{BASE_URL}/competitions/{code}/matches?dateFrom={today}&dateTo={today}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for match in data.get("matches", []):
                matches.append({
                    "competition": name,
                    "homeTeam": match["homeTeam"]["name"],
                    "awayTeam": match["awayTeam"]["name"],
                    "utcDate": match["utcDate"]
                })
    return matches

def make_dummy_prediction(home_team, away_team):
    home_goals = randint(0, 3)
    away_goals = randint(0, 3)
    winner = "Match nul"
    if home_goals > away_goals:
        winner = f"Victoire {home_team}"
    elif away_goals > home_goals:
        winner = f"Victoire {away_team}"
    return {
        "score": f"{home_goals}-{away_goals}",
        "winner": winner,
        "over_2_5": "Oui" if home_goals + away_goals > 2.5 else "Non"
    }

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de prédictions de matchs"}

@app.get("/predictions")
def run_predictions():
    matches = get_today_matches()
    results = []
    for match in matches:
        pred = make_dummy_prediction(match["homeTeam"], match["awayTeam"])
        results.append({
            "match": f"{match['homeTeam']} vs {match['awayTeam']}",
            "competition": match['competition'],
            "score_prevu": pred['score'],
            "gagnant": pred['winner'],
            "plus_de_2_5": pred['over_2_5']
        })
    return results
