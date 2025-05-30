from fastapi import FastAPI
from predictor import predict_match

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API de prédiction de matchs"}

@app.get("/predict")
def get_prediction():
    result = predict_match()
    return {"prediction": result}