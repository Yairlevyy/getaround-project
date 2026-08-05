import joblib
import pandas as pd
from fastapi import FastAPI
from pathlib import Path
from pydantic import BaseModel

app = FastAPI(title="GetAround Pricing API")

model = joblib.load(Path(__file__).parent / "model.joblib")


class PredictionInput(BaseModel):
    input: list[list]


@app.get("/")
def accueil():
    return {"message": "API de prediction de prix GetAround"}


@app.post("/predict")
def predict(data: PredictionInput):
    colonnes = [
        "model_key", "mileage", "engine_power", "fuel", "paint_color", "car_type",
        "private_parking_available", "has_gps", "has_air_conditioning",
        "automatic_car", "has_getaround_connect", "has_speed_regulator", "winter_tires",
    ]
    df = pd.DataFrame(data.input, columns=colonnes)
    predictions = model.predict(df)
    return {"prediction": [round(p, 2) for p in predictions]}