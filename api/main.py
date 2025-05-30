from fastapi import FastAPI
from predictor import predict_match

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API Prédiction OK"}

@app.get("/predict")
def predict(team1: str, team2: str):
    return predict_match(team1, team2)
