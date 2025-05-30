def predict_match(team1, team2):
    # Ex. simplifié : on prédit match nul
    return {
        "winner": "Draw",
        "score": "1-1",
        "goals": {
            team1: 1,
            team2: 1
        }
    }
